from __future__ import annotations

import ctypes
import hashlib
import shutil
import subprocess
import sys
import tempfile
import time
import wave
from array import array
from pathlib import Path
from threading import RLock


class _WindowsWaveOutPlayer:
    """Persistent Windows PCM/WAV playback using the legacy waveOut API.

    Keeping one waveOut device open avoids the endpoint wake/open latency that
    can swallow very short terminal cues on some desktop audio devices.
    """

    WAVE_MAPPER = 0xFFFFFFFF
    CALLBACK_NULL = 0x00000000
    WAVE_FORMAT_PCM = 0x0001
    WHDR_DONE = 0x00000001
    MMSYSERR_NOERROR = 0

    class WAVEFORMATEX(ctypes.Structure):
        _fields_ = [
            ("wFormatTag", ctypes.c_ushort),
            ("nChannels", ctypes.c_ushort),
            ("nSamplesPerSec", ctypes.c_uint32),
            ("nAvgBytesPerSec", ctypes.c_uint32),
            ("nBlockAlign", ctypes.c_ushort),
            ("wBitsPerSample", ctypes.c_ushort),
            ("cbSize", ctypes.c_ushort),
        ]

    class WAVEHDR(ctypes.Structure):
        pass

    WAVEHDR._fields_ = [
        ("lpData", ctypes.c_void_p),
        ("dwBufferLength", ctypes.c_uint32),
        ("dwBytesRecorded", ctypes.c_uint32),
        ("dwUser", ctypes.c_size_t),
        ("dwFlags", ctypes.c_uint32),
        ("dwLoops", ctypes.c_uint32),
        ("lpNext", ctypes.POINTER(WAVEHDR)),
        ("reserved", ctypes.c_size_t),
    ]

    def __init__(self):
        self._lock = RLock()
        self._winmm = ctypes.WinDLL("winmm")
        self._configure_api()
        self._handle = ctypes.c_void_p()
        self._format_key = None
        self._current = None

    def _configure_api(self):
        fmt_ptr = ctypes.POINTER(self.WAVEFORMATEX)
        hdr_ptr = ctypes.POINTER(self.WAVEHDR)

        self._winmm.waveOutOpen.argtypes = [
            ctypes.POINTER(ctypes.c_void_p),
            ctypes.c_uint,
            fmt_ptr,
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_uint,
        ]
        self._winmm.waveOutOpen.restype = ctypes.c_uint

        self._winmm.waveOutPrepareHeader.argtypes = [
            ctypes.c_void_p,
            hdr_ptr,
            ctypes.c_uint,
        ]
        self._winmm.waveOutPrepareHeader.restype = ctypes.c_uint

        self._winmm.waveOutWrite.argtypes = [
            ctypes.c_void_p,
            hdr_ptr,
            ctypes.c_uint,
        ]
        self._winmm.waveOutWrite.restype = ctypes.c_uint

        self._winmm.waveOutUnprepareHeader.argtypes = [
            ctypes.c_void_p,
            hdr_ptr,
            ctypes.c_uint,
        ]
        self._winmm.waveOutUnprepareHeader.restype = ctypes.c_uint

        self._winmm.waveOutReset.argtypes = [ctypes.c_void_p]
        self._winmm.waveOutReset.restype = ctypes.c_uint

        self._winmm.waveOutClose.argtypes = [ctypes.c_void_p]
        self._winmm.waveOutClose.restype = ctypes.c_uint

    @staticmethod
    def _read_pcm_wav(path):
        with wave.open(str(path), "rb") as source:
            if source.getcomptype() != "NONE":
                raise ValueError("compressed WAV is not supported")
            channels = source.getnchannels()
            sample_rate = source.getframerate()
            sample_width = source.getsampwidth()
            frames = source.readframes(source.getnframes())

        if channels < 1 or sample_rate < 1 or sample_width not in (1, 2, 3, 4):
            raise ValueError("unsupported PCM WAV format")

        bits = sample_width * 8
        block_align = channels * sample_width
        avg_bytes = sample_rate * block_align
        format_key = (channels, sample_rate, bits)
        return format_key, block_align, avg_bytes, frames

    def _open_for(self, format_key, block_align, avg_bytes):
        if self._handle.value and self._format_key == format_key:
            return True

        self._close_locked()

        channels, sample_rate, bits = format_key
        fmt = self.WAVEFORMATEX(
            self.WAVE_FORMAT_PCM,
            channels,
            sample_rate,
            avg_bytes,
            block_align,
            bits,
            0,
        )
        handle = ctypes.c_void_p()
        result = self._winmm.waveOutOpen(
            ctypes.byref(handle),
            self.WAVE_MAPPER,
            ctypes.byref(fmt),
            0,
            0,
            self.CALLBACK_NULL,
        )
        if result != self.MMSYSERR_NOERROR:
            return False

        self._handle = handle
        self._format_key = format_key
        return True

    def _current_is_playing(self):
        if not self._current:
            return False
        _buffer, header = self._current
        return not bool(header.dwFlags & self.WHDR_DONE)

    def is_playing(self):
        with self._lock:
            return self._current_is_playing()

    def _release_current(self, force=False):
        if not self._current or not self._handle.value:
            self._current = None
            return

        _buffer, header = self._current
        if force and not (header.dwFlags & self.WHDR_DONE):
            self._winmm.waveOutReset(self._handle)

        # waveOutReset marks queued buffers complete before it returns.
        if header.dwFlags & self.WHDR_DONE or force:
            self._winmm.waveOutUnprepareHeader(
                self._handle,
                ctypes.byref(header),
                ctypes.sizeof(self.WAVEHDR),
            )
            self._current = None

    def play(self, path, no_interrupt=False):
        with self._lock:
            format_key, block_align, avg_bytes, frames = self._read_pcm_wav(path)

            if no_interrupt and self._current_is_playing():
                return False

            if self._current:
                self._release_current(force=True)

            if not self._open_for(format_key, block_align, avg_bytes):
                return False

            if not frames:
                return False

            audio_buffer = ctypes.create_string_buffer(frames)
            header = self.WAVEHDR()
            header.lpData = ctypes.cast(audio_buffer, ctypes.c_void_p)
            header.dwBufferLength = len(frames)
            header.dwBytesRecorded = 0
            header.dwUser = 0
            header.dwFlags = 0
            header.dwLoops = 0
            header.lpNext = None
            header.reserved = 0

            result = self._winmm.waveOutPrepareHeader(
                self._handle,
                ctypes.byref(header),
                ctypes.sizeof(self.WAVEHDR),
            )
            if result != self.MMSYSERR_NOERROR:
                return False

            self._current = (audio_buffer, header)
            result = self._winmm.waveOutWrite(
                self._handle,
                ctypes.byref(header),
                ctypes.sizeof(self.WAVEHDR),
            )
            if result != self.MMSYSERR_NOERROR:
                self._release_current(force=True)
                return False
            return True

    def stop(self):
        with self._lock:
            self._release_current(force=True)

    def close(self):
        with self._lock:
            self._close_locked()

    def _close_locked(self):
        if self._handle.value:
            self._release_current(force=True)
            self._winmm.waveOutClose(self._handle)
        self._handle = ctypes.c_void_p()
        self._format_key = None
        self._current = None


class AudioManager:
    """Small, failure-safe audio service for J-29 UI feedback.

    WAV files are the reference format. On Windows, PCM WAV playback uses one
    persistent waveOut device so very short terminal cues are not lost to audio
    endpoint startup latency. Other platforms keep the existing native-tool
    fallbacks. Every failure degrades to silence rather than interrupting J-29.
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

        self._event_cooldowns = {
            "menu_move": 0.055,
        }
        self._last_event_time = {}

        self._windows_player = None
        if sys.platform.startswith("win"):
            try:
                self._windows_player = _WindowsWaveOutPlayer()
            except Exception:
                # Fall back to winsound below if waveOut is unavailable.
                self._windows_player = None

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
            return False

    def stop(self):
        """Best-effort stop of current audio without breaking J-29."""
        if not sys.platform.startswith("win"):
            return

        if self._windows_player is not None:
            try:
                self._windows_player.stop()
                return
            except Exception:
                pass

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
            return bytes(
                max(0, min(255, round((sample - 128) * factor + 128)))
                for sample in frames
            )

        type_map = {2: "h", 4: "i"}
        typecode = type_map.get(sample_width)
        if not typecode:
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

    def _play_windows(self, path, no_interrupt=False):
        if path.suffix.lower() != ".wav":
            return False

        if self._windows_player is not None:
            try:
                return self._windows_player.play(
                    path,
                    no_interrupt=no_interrupt,
                )
            except Exception:
                # Preserve compatibility by falling through to winsound.
                pass

        try:
            import winsound
            flags = (
                winsound.SND_FILENAME
                | winsound.SND_ASYNC
                | winsound.SND_NODEFAULT
            )
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
