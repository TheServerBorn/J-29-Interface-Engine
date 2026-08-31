from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
import time
import wave
from array import array
from pathlib import Path


class AudioManager:
    """Small, failure-safe audio service for J-29 UI feedback.

    The manager intentionally has no third-party dependency. WAV files are the
    reference format. Playback is asynchronous on supported platforms and every
    failure degrades to silence rather than interrupting the terminal.
    """

    def __init__(self, settings=None, theme=None):
        settings = settings or {}
        theme = theme or {}

        self.enabled = bool(settings.get("audio_enabled", True))
        self.master_volume = self._clamp_volume(
            settings.get("master_volume", 70)
        )
        self.theme_dir = Path(theme.get("_theme_dir", "."))
        self.sounds = dict(theme.get("sounds", {}))
        self._cache_dir = Path(tempfile.gettempdir()) / "j29_audio_cache"

        # High-rate UI events must never flood the host audio backend.
        # Holding an arrow key can generate dozens of KeyPress events per
        # second; without throttling that produces ugly restarts/overlap and
        # can leave audible ticks after the user releases the key.
        self._event_cooldowns = {
            "menu_move": 0.055,
        }
        self._last_event_time = {}

    @staticmethod
    def _clamp_volume(value):
        try:
            return max(0, min(100, int(value)))
        except (TypeError, ValueError):
            return 70

    def configure(self, settings=None, theme=None):
        """Reload runtime audio settings without rebuilding the engine."""
        settings = settings or {}
        theme = theme or {}

        self.enabled = bool(settings.get("audio_enabled", self.enabled))
        self.master_volume = self._clamp_volume(
            settings.get("master_volume", self.master_volume)
        )
        self.theme_dir = Path(theme.get("_theme_dir", self.theme_dir))
        self.sounds = dict(theme.get("sounds", self.sounds))

    def resolve_sound(self, event_name):
        relative = str(self.sounds.get(event_name, "")).strip()
        if not relative:
            return None

        path = Path(relative)
        if not path.is_absolute():
            path = self.theme_dir / path

        return path

    def play(self, event_name):
        """Play a configured UI event asynchronously.

        Returns True only when a playback backend accepted the request.
        Missing files, unsupported formats, or unavailable host audio tools are
        intentionally nonfatal and return False.
        """
        if not self.enabled or self.master_volume <= 0:
            return False

        # Coalesce high-frequency feedback instead of queueing/restarting it.
        now = time.monotonic()
        cooldown = self._event_cooldowns.get(event_name, 0.0)
        if cooldown:
            previous = self._last_event_time.get(event_name, 0.0)
            if now - previous < cooldown:
                return False

        path = self.resolve_sound(event_name)
        if not path or not path.is_file():
            return False

        try:
            playable = self._volume_adjusted_path(path)
            if sys.platform.startswith("win"):
                accepted = self._play_windows(
                    playable,
                    no_interrupt=(event_name == "menu_move"),
                )
            elif sys.platform == "darwin":
                accepted = self._play_macos(playable)
            else:
                accepted = self._play_linux(playable)

            if accepted and cooldown:
                self._last_event_time[event_name] = now
            return accepted
        except Exception:
            # Audio is personality, never a dependency for terminal operation.
            return False

    def stop(self):
        """Best-effort stop for the native Windows async WAV backend."""
        if not sys.platform.startswith("win"):
            return
        try:
            import winsound
            winsound.PlaySound(None, winsound.SND_PURGE)
        except Exception:
            pass

    def _volume_adjusted_path(self, path):
        """Create/cache a volume-scaled PCM WAV without external libraries."""
        if self.master_volume >= 100 or path.suffix.lower() != ".wav":
            return path

        try:
            stat = path.stat()
            cache_key = (
                f"{path.resolve()}|{stat.st_mtime_ns}|{stat.st_size}|"
                f"{self.master_volume}"
            )
            digest = hashlib.sha1(cache_key.encode("utf-8")).hexdigest()[:16]
            self._cache_dir.mkdir(parents=True, exist_ok=True)
            target = self._cache_dir / f"{path.stem}-{digest}.wav"
            if target.exists():
                return target

            with wave.open(str(path), "rb") as source:
                params = source.getparams()
                sample_width = source.getsampwidth()
                frames = source.readframes(source.getnframes())

            scaled = self._scale_pcm(frames, sample_width)
            if scaled is None:
                return path

            with wave.open(str(target), "wb") as output:
                output.setparams(params)
                output.writeframes(scaled)

            return target
        except Exception:
            return path

    def _scale_pcm(self, frames, sample_width):
        factor = self.master_volume / 100.0

        if sample_width == 1:
            # 8-bit PCM WAV samples are unsigned and centered at 128.
            return bytes(
                max(0, min(255, round((sample - 128) * factor + 128)))
                for sample in frames
            )

        type_map = {2: "h", 4: "i"}
        typecode = type_map.get(sample_width)
        if not typecode:
            # 24-bit/custom encodings are left untouched rather than risking
            # corruption of a user-supplied theme sound.
            return None

        samples = array(typecode)
        samples.frombytes(frames)
        if sys.byteorder != "little":
            samples.byteswap()

        if sample_width == 2:
            minimum, maximum = -32768, 32767
        else:
            minimum, maximum = -2147483648, 2147483647

        for index, sample in enumerate(samples):
            samples[index] = max(
                minimum,
                min(maximum, int(sample * factor)),
            )

        if sys.byteorder != "little":
            samples.byteswap()
        return samples.tobytes()

    @staticmethod
    def _play_windows(path, no_interrupt=False):
        if path.suffix.lower() != ".wav":
            return False
        try:
            import winsound
            flags = (
                winsound.SND_FILENAME
                | winsound.SND_ASYNC
                | winsound.SND_NODEFAULT
            )
            # Menu-repeat feedback is disposable. If another sound is already
            # playing, drop this tick rather than interrupting/restarting audio.
            if no_interrupt:
                flags |= winsound.SND_NOSTOP

            winsound.PlaySound(str(path), flags)
            return True
        except Exception:
            return False

    @staticmethod
    def _spawn(command):
        try:
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
            )
            return True
        except (OSError, ValueError):
            return False

    def _play_macos(self, path):
        player = shutil.which("afplay")
        if not player:
            return False
        return self._spawn([player, str(path)])

    def _play_linux(self, path):
        # Prefer PipeWire/PulseAudio when available, then ALSA.
        candidates = (
            ("pw-play", [str(path)]),
            ("paplay", [str(path)]),
            ("aplay", ["-q", str(path)]),
        )
        for executable, args in candidates:
            player = shutil.which(executable)
            if player:
                return self._spawn([player, *args])
        return False
