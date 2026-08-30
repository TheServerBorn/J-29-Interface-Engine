## v0.26 — Physical Media System — COMPLETE

### Added
- Cross-platform physical-media detection foundation for removable media.
- Automatic single-ROM recognition and `MEDIA DETECTED` launch prompt.
- Runtime insertion/removal events with sequential event handling.
- Safe hot-removal behavior while the media prompt is open.
- Duplicate insertion protection and fresh detection after reinsertion.
- Windows mounted-volume identity tracking so SD cards work correctly through
  readers that retain the same drive letter.
- Terminal startup now correctly begins the recurring physical-media poll loop.

### Real Hardware Validation
- SD card insertion into an already-connected USB reader: PASS.
- Full USB reader removal: PASS.
- `MEDIA REMOVED` status: PASS.
- Full reader reinsertion and fresh `MEDIA DETECTED` prompt: PASS.
- Removal while `LOAD GAME?` prompt is open: PASS.
- Physical-media ROM launch through the existing emulator pipeline: PASS.
- Repeated remove / insert / load / launch cycles: PASS.

### Status
- v0.26 Physical Media System is COMPLETE.
- Temporary diagnostic logging used during hardware validation has been removed.

## v0.26 — Physical Media Poll Startup Fix

### Fixed
- The Terminal UI now schedules the first physical-media poll when `run()`
  starts.
- The existing two-second recurring polling chain can now actually begin.
- This fixes the condition where the media engine initialized correctly but
  USB/SD insertions never produced a Terminal event or `MEDIA DETECTED` prompt.

### Validation
- Compile check passed.
- Real removable-media insertion validation pending.

## v0.26 — Windows Media Identity Fix

### Fixed
- Windows physical-media snapshots now identify mounted media using the volume
  serial/name/filesystem in addition to the drive letter.
- SD-card insertion can generate a fresh event even when the USB reader remains
  mounted at the same drive letter before and after insertion.
- Empty/inaccessible reader slots are ignored when Windows cannot return valid
  volume information.

### Validation
- Compile check passed.
- Real SD-reader validation required on Windows.

## v0.26 — Windows Empty Card Reader Fix

### Fixed
- Windows drive letters that exist only because an empty USB/SD reader is
  connected are no longer counted as mounted physical media.
- Inserting an SD card into an already-connected reader can now generate a new
  `MEDIA DETECTED` event even when Windows keeps the same drive letter.
- Windows media discovery verifies that the drive has an accessible filesystem
  before adding it to the media snapshot.

## v0.26 — Physical Media Safety Pass

### Fixed
- Removing media while the `MEDIA DETECTED` prompt is open now safely cancels
  the prompt and returns to the previous J-29 screen.
- Removing queued media removes its pending prompt from the queue.
- Pressing Load after media has disappeared is rejected before emulator launch.
- Duplicate insertion events for the same mounted volume are ignored.
- Reinserting a previously removed device can generate a fresh insertion event.
- Removal events remain non-fatal and cannot crash the terminal UI.

### Validation
- Compile checks passed.
- Media state transitions are synthetic-tested.
- Real USB insertion/removal validation remains on the release-candidate check.

## v0.26 — Physical Media Runtime Events

### Added
- Persistent media monitor that tracks both insertions and removals.
- Non-blocking `MEDIA REMOVED` terminal status.
- Queueing for multiple media insertions detected in the same polling cycle.
- Backward-compatible insertion polling API.
- OS/device polling remains isolated from shell code.

### Validation
- Runtime event state is synthetic-tested.
- Real removable-media insertion/removal validation remains pending until a
  physical USB/removable device is available.

## v0.26 — Physical Media System — INITIAL CHECKPOINT

### Added
- Cross-platform physical-media volume detection foundation.
- Background polling for newly mounted media.
- Windows detection supports newly appearing non-system drive letters, including
  USB flash drives and many USB SSD/HDD devices that report as fixed disks.
- Linux mounted-media discovery under common `/media`, `/run/media`, and `/mnt`
  locations.
- macOS mounted-media discovery under `/Volumes`.
- Conservative single-game ROM inspection for inserted media.
- In-character `MEDIA DETECTED / LOAD GAME? [Y/N]` terminal prompt.
- Y/Enter launches the detected game through the existing v0.25 emulator layer.
- N/Esc dismisses the inserted media.
- Media detection failures are isolated so they cannot crash the terminal UI.

### Scope Boundary
- v0.26 initial validation uses ordinary removable storage containing one
  recognizable ROM.
- Multi-game physical collections and formal J-29 media metadata are deferred to
  v0.27.

## v0.25.1 — Centered Long-List Scrolling Fix

### Fixed
- Long lists now scroll around the selected cursor instead of waiting for the
  cursor to reach the bottom of the visible page.
- The selected game remains approximately centered vertically whenever possible.
- Increased footer safety margin prevents list entries from rendering beneath
  the navigation/help bar.
- Beginning and end of a list clamp naturally while still keeping the selected
  item visible.

## v0.25.1 — Long List Scrolling

### Fixed
- Long Game Library folders now automatically scroll as the selection moves.
- The selected item always remains visible when navigating with Up/Down.
- Favorites and Recent Games use the same scrolling behavior.
- Visible range indicators show the current portion of a long list.
- List capacity adapts to the current terminal window height.

# Changelog

## v0.25 — Emulator Support — COMPLETE

### Added
- Automatic ROM library discovery from configured ROM roots.
- Platform inference from common ROM folder names.
- Stable generated ROM IDs and normal J-29 metadata records.
- Manual ROM entries override auto-discovered records with the same ROM path.
- Conservative game-file filtering to avoid artwork/save-file noise.
- Automatic RetroArch core selection by platform.
- Installed-core detection with ordered fallback candidates.
- Expanded fallback coverage across supported classic systems.
- Visible diagnostics for missing cores, missing emulators, and unsupported profiles.
- Standalone emulator auto-detection foundation for PCSX2, RPCS3, Dolphin, and PPSSPP.
- Common Windows, Linux, and macOS executable lookup paths plus PATH lookup.

### Real-World Validation
- Automatic ROM discovery validated against the active ROM library.
- SNES launch validated.
- NES launch validated.
- Nintendo 64 launch validated.
- GBA launch validated.
- GBC launch validated.
- Sega Genesis launch validated.
- Return-to-J-29 state retention validated after emulator exit.
- Multiple SNES titles validated.
- Manual DOOM entry removed from `games.ini`; DOOM continued to appear and launch through automatic discovery.

### Deferred Release-Candidate Revalidation
- PCSX2 / PS2
- RPCS3 / PS3
- Dolphin / GameCube and Wii
- PPSSPP / PSP

These standalone paths are implemented and synthetic-tested but were not field-tested during v0.25 because matching emulator/ROM test assets were not available. They must be included in the final release-candidate regression where supported test media is available. Any remaining unsupported platform must be documented explicitly.



## v0.23 — Recent Games (validation build)

- Added persistent recent-game history to `config/game_state.json`.
- Added engine methods to record and retrieve recent games by stable game ID.
- Recent history updates only after a successful program launch.
- Re-launching a game moves it to the top without creating duplicates.
- Limited the recent list to the five most recently launched games.
- Added RECENT GAMES to the Terminal Shell main menu.
- Added `RECENT` and `RECENTS` commands.
- Recent entries open the existing v0.21 Program Information screen before launch.
- Returning from Program Information preserves the selected recent game after the list reorders.
- Preserved v0.22 Favorites data in the shared persistent game-state file.

## v0.22 — Favorites

- Added persistent favorite state in `config/game_state.json`.
- Added engine methods to list, inspect, add, and remove favorites by stable game ID.
- Added FAVORITES to the Terminal Shell main menu.
- Added `FAVORITES` and `FAV` commands.
- Added `F` favorite toggle on the Program Information screen.
- Added direct `F` removal from the Favorites view.
- Favorites use the existing v0.21 Program Information screen before launch.
- Returning from Program Information preserves the Favorites selection.
- Kept Recent Games out of v0.22 so roadmap milestones remain isolated.

## v0.21 — Game Metadata

- Added structured game metadata records in `engine/games.py`.
- Preserved backwards compatibility with existing `name`, `path`, and `folder` entries.
- Added platform, year, genre, developer, publisher, launch type, executable path, ROM path, emulator, Steam ID, and favorite fields.
- Added simple boolean/year normalization and sensible metadata fallbacks.
- Expanded `games.ini` and `games.example.ini` with v0.21 metadata examples.
- Added a Terminal Shell program-information screen for selected games.
- Game entries now open metadata details before launch.
- Added explicit `ENTER RUN` / `ESC BACK` controls on the metadata screen.
- Returning from metadata preserves the previous library folder and selection.

All notable development milestones for the J29 Terminal Engine will be documented here.

The project currently uses small development versions so each stable milestone can be tested, preserved, and documented before moving forward.

---

## [0.20] - 2026-08-27

### Added
- Filesystem-style Game Library browser
- Virtual `GAMES/` root directory
- Virtual game folders using the `folder=` field in `games.ini`
- Default `PROGRAMS` folder for game entries without a specified folder
- Visible current library path
- `DIR` command
- `LS` command
- `CD <DIRECTORY>` command
- `CD ..` parent-directory navigation
- `CD /` root-directory navigation
- Context-sensitive Game Library footer guidance

### Changed
- Game Library now organizes programs into virtual directories instead of displaying a single flat list
- Enter opens directories from `GAMES/`
- Enter launches programs from inside a library directory
- Escape moves up one directory before leaving the Game Library
- `BACK` moves up one directory before leaving the Game Library
- Game Library footer displays `ENTER OPEN` at the directory level and `ENTER RUN` inside a game folder
- Library directories and programs are displayed in predictable alphabetical order
- Existing `games.ini` entries without a `folder=` value remain compatible and are placed under `PROGRAMS`

### Verified
- `GAMES/` displays available virtual directories
- Multiple library directories display correctly
- Enter opens the selected directory
- Programs display correctly inside their assigned directory
- Enter launches a valid program from inside a library directory
- Programs with unavailable paths display `PROGRAM NOT AVAILABLE`
- Escape returns from a library directory to `GAMES/`
- Escape returns from `GAMES/` to the previous screen
- `DIR` opens or displays the Game Library
- `LS` opens or displays the Game Library
- `CD <DIRECTORY>` opens a valid library directory
- `CD ..` returns to `GAMES/`
- `CD /` returns to the `GAMES/` root
- Invalid directory names display `DIRECTORY NOT FOUND`
- `BACK` returns from a library directory to `GAMES/`
- `BACK` returns from `GAMES/` to the previous screen
- Context-sensitive footer guidance updates correctly between directory and program views
- Existing System Info and Help Escape navigation remain functional
- Existing v0.19 command navigation remains functional
- Multi-directory library navigation tested successfully with DOS, SNES, and WINDOWS folders

---

## [0.19] - 2026-08-23

### Added
- Terminal command input mode
- Dynamic command prompt positioning
- Context-sensitive command mode footer guidance
- Previous-screen navigation history
- `HELP` command
- `GAMES` command
- `SYSINFO` command
- `BACK` command
- `CLEAR` command
- `REBOOT` command
- `SHUTDOWN` command
- Unknown command handling

### Changed
- Typed commands now provide an alternate navigation path alongside menu controls
- Command prompt position now follows the current screen content dynamically
- Escape and `BACK` return to the previous screen when history is available
- `REBOOT` restarts the J29 boot sequence without restarting the host system
- `SHUTDOWN` exits J29 without shutting down the host system

### Verified
- HELP opens the command reference screen
- GAMES opens the Game Library
- SYSINFO opens System Info
- BACK returns to the previous screen
- CLEAR resets command/status state without changing screens
- REBOOT clears command/history state and reruns the boot sequence
- SHUTDOWN exits J29 cleanly
- Invalid commands display `UNKNOWN COMMAND`
- Temporary command status messages restore the correct footer
- Command prompt and blinking cursor remain correctly positioned across screens
- Menu and command navigation coexist correctly
- Screen history works across menu and command navigation
- Full v0.19 regression test passed

---

## [0.18] - 2026-08-23

### Added
- Context-sensitive dynamic footer
- Screen-specific control hints
- Temporary footer status messages
- Automatic status-message timeout and footer restoration
- Responsive footer positioning near the bottom of the window

### Changed
- Main Menu now displays navigation controls in the footer
- Game Library controls moved from inline menu text to the footer
- System Info navigation hint moved to the footer
- Existing `show_footer` setting now controls footer visibility
- Program launch errors now temporarily replace the control footer

### Verified
- Main Menu, Game Library, and System Info display the correct contextual footer
- `show_footer=false` hides the footer across screens
- `show_footer=true` restores normal footer behavior
- `PROGRAM NOT AVAILABLE` automatically returns to the Game Library controls after 5 seconds
- Footer remains correctly positioned in fullscreen and windowed modes
- Temporary status recovery works correctly after resizing
- Full v0.18 regression test passed

---

## [0.17] - 2026-08-23

### Added
- First-run configuration bootstrap
- Automatic creation of `config/identity.ini` from `identity.example.ini`
- Automatic creation of `config/settings.ini` from `settings.example.ini`

### Changed
- Identity and settings loaders now ensure their local configuration files exist before loading

### Verified
- Missing identity config is recreated automatically
- Missing settings config is recreated automatically
- Both configs can be recreated together during a fresh-install simulation
- Existing user configuration files are preserved and not overwritten
- J29 boots normally after first-run configuration creation

---

## [0.16] - 2026-08-22

### Added
- Theme configuration system
- `engine/theme.py` theme loader
- Configurable theme selection through `settings.ini`
- Callisto Green reference theme
- Amber Terminal alternate theme
- Configurable primary and secondary colors
- Configurable background color
- Configurable font family and font sizes
- Configurable scanline enable/disable and spacing
- Configurable cursor style

### Changed
- Terminal Shell visual settings now load from theme configuration instead of hardcoded values
- Theme selection is exposed through the core engine

### Verified
- Callisto Green and Amber Terminal can be switched without Python code changes
- Amber theme colors and underscore cursor load correctly
- Callisto Green restores correctly after theme switching
- Scanlines can be enabled or disabled through theme configuration
- Full v0.16 regression test passed

---

## [0.15] - 2026-08-22

### Added
- Added configurable machine identity system.
- Added `identity.ini` and public `identity.example.ini` configuration structure.
- Added configurable manufacturer name.
- Added configurable system / OS name.
- Added configurable model name.
- Added configurable unit ID.
- Added optional owner and location fields.
- Added shared settings configuration system.
- Added `settings.ini` and public `settings.example.ini`.
- Added configurable startup fullscreen behavior.
- Added configurable boot-sequence behavior.
- Added configurable development fullscreen and windowed-mode keys.
- Added configuration fallbacks when identity or settings files are missing.
- Added safe handling for an empty or missing game library.

### Changed
- Boot branding now uses the configured machine identity.
- Window title now uses the configured system name.
- Terminal title now uses the configured system name and version.
- System Information now displays fictional machine identity alongside real host hardware information.
- Game configuration moved into the `config/` directory.
- Public configuration templates are separated from local user configuration.
- Local identity, settings, and game configuration files remain excluded from Git.

### Configuration
Public templates:

    config/identity.example.ini
    config/settings.example.ini
    config/games.example.ini

Local configuration:

    config/identity.ini
    config/settings.ini
    config/games.ini

Local configuration files are ignored by Git.

### Testing
Full regression test passed:

- Boot sequence
- Main menu navigation
- Dynamic machine branding
- System Information
- Game Library
- External program launching
- Missing-program handling
- Empty-library handling
- Fullscreen startup setting
- Boot-sequence enable/disable
- Configurable development keys
- Escape/back navigation
- Missing identity fallback
- Missing settings fallback

### Status
Stable development checkpoint.

---
## [0.14] - 2026-08-22

### Added
- Introduced modular `engine` package.
- Added shared Core Engine interface through `J29Engine`.
- Added dedicated system information module.
- Added shared configuration loader.
- Added game library loader.
- Added program launcher module.
- Added modular `shells` package.
- Added J-29 Terminal Shell package.
- Added clean `main.py` application entry point.
- Preserved `j29.py` as a compatibility launcher.

### Changed
- Terminal Shell now communicates with engine functionality through `J29Engine`.
- CPU, memory, storage, and operating-system detection moved out of the UI.
- Game configuration loading moved out of the UI.
- Program launching moved out of the UI.
- Game configuration now uses the shared configuration loader.
- Importing the Terminal Shell no longer automatically launches the application.

### Architecture
The project is now separated into the beginnings of:

- Engine — shared functionality and services
- Shell — interface and interaction
- Entry point — application startup

The J-29 Terminal remains the reference shell.

### Testing
Full regression test passed:

- Boot sequence
- Main menu navigation
- System Information
- Game Library
- External program launching
- Missing-program handling
- Escape/back navigation

### Status
Stable development checkpoint.

---

## [0.13] - 2026-08-21

### Added
- Completed migration of visible interface elements to the Tkinter Canvas.
- Added Canvas-based status messages.
- Preserved CRT scanlines behind interface text.
- Stabilized Canvas-based blinking cursor behavior.
- Cleaned up System Info cursor behavior.

### Status
Stable development checkpoint.

---

## [0.12] - 2026-08-21

### Added
- Began converting the interface from Tkinter Labels to Canvas-rendered text.
- Converted terminal title to Canvas.
- Converted main menu to Canvas.
- Converted Game Library to Canvas.
- Converted System Info display to Canvas.
- Converted boot sequence text to Canvas.
- Converted blinking cursor to Canvas.

### Improved
- Removed black background rectangles behind terminal text.
- Improved CRT scanline integration.

---

## [0.11] - 2026-08-21

### Added
- CRT-style horizontal scanlines.
- Adjustable scanline spacing and intensity.

### Improved
- Tuned scanlines for a more subtle retro display effect.

---

## [0.10] - 2026-08-21

### Added
- Centralized font-size configuration.
- Separate title, menu, status, and cursor font sizes.

### Improved
- Repositioned interface toward the upper-left of the display.
- Improved layout for the planned 10.1-inch reference display.

---

## [0.9] - 2026-08-21

### Added
- Fullscreen Terminal Mode.
- F11 development shortcut to enter fullscreen.
- F12 development shortcut to leave fullscreen.
- Hidden mouse cursor while in Terminal Mode.
- Mouse cursor restoration while in development/maintenance mode.

### Note
These temporary development shortcuts are planned to be replaced by the future secured maintenance system.

---

## [0.8] - 2026-08-21

### Added
- Real hardware information to the startup sequence.
- CPU detection.
- Installed memory detection.
- System storage capacity detection.
- Windows system drive detection.

### Improved
- Startup sequence now reflects the actual host computer.

---

## [0.7.1] - 2026-08-21

### Added
- Installed memory display.
- Explicit Windows system-drive detection.

### Fixed
- Verified storage and free-space values are read from the correct system volume.

---

## [0.7] - 2026-08-21

### Added
- Real System Information screen.
- Windows version detection.
- CPU model detection through the Windows registry.
- Storage capacity detection.
- Available disk-space detection.

---

## [0.6] - 2026-08-21

### Added
- External `games.ini` configuration.
- Game Library entries can now be defined outside the Python source.
- Game name and executable path configuration.
- Graceful message for unavailable programs.

### Changed
- Game Library is no longer hardcoded directly into the launcher.

---

## [0.5] - 2026-08-21

### Added
- Arrow-key navigation inside the Game Library.
- Enter key selection inside the Game Library.
- Escape key navigation back to the main menu.

---

## [0.4] - 2026-08-21

### Added
- External Windows application launching.
- Initial launch test using Windows Notepad.

### Significance
This milestone proved that the J29 interface could act as a frontend for real applications and games.

---

## [0.3] - 2026-08-21

### Added
- Animated startup sequence.
- Simulated system initialization.
- CPU, memory, storage, display, and network startup messages.
- Automatic transition from startup sequence to the main menu.

---

## [0.2] - 2026-08-21

### Added
- Arrow-key main-menu navigation.
- Enter key selection.
- Dedicated Game Library screen.
- Dedicated System Information screen.
- Escape key navigation.

---

## [0.1] - 2026-08-21

### Added
- Initial Python/Tkinter application.
- Black terminal-style window.
- Green monospace text.
- J-29 Terminal OS title.
- Main menu.
- Basic keyboard input.
- Game Library prototype screen.
- Blinking terminal cursor.

### Significance
First functioning J-29 Terminal OS prototype.

---

# Planned Architecture Pivot

Beginning with **v0.14**, development will transition from a single monolithic J-29 application into a modular frontend-engine architecture.

The project will separate:

- **Engine** — shared functionality and services.
- **Shell** — interface and interaction model.
- **Theme** — visual and audio presentation.
- **Identity** — configurable fictional-computer branding.

The original J-29 Terminal interface will remain the reference shell and the target experience for the initial v1.0 release.

This pivot was made early in development after the project expanded beyond its original purpose-built launcher concept. The modular architecture is intended to support future shells, themes, hardware projects, and community-created interfaces without requiring the core engine to be rewritten.
## v0.24 — Steam Support — COMPLETE

### Added
- Automatic Steam installation detection.
- Automatic discovery of installed Steam libraries and games.
- Parsing of Steam `libraryfolders.vdf` and `appmanifest_*.acf` files.
- Support for multiple Steam library locations.
- Automatic `GAMES/STEAM/` library population.
- Steam App ID and launch-type metadata integration.
- Engine-level Steam launch dispatch using `steam://run/<appid>`.
- Cross-platform Steam URI launching architecture for Windows, Linux, and macOS.
- Manual Steam-entry example support in `games.example.ini`.

### Changed
- Steam titles now use the same Program Information workflow as other J-29 games.
- Steam launches integrate with existing Favorites and Recent Games state.
- Manual Steam metadata overrides duplicate auto-discovered Steam entries.
- J-29 remains active while an external Steam game is running and returns to the selected game's metadata screen after exit.

### Fixed
- Filtered Steamworks Common Redistributables (App ID 228980) from the visible game library.
- Updated system information handling to avoid unconditional Windows-only dependencies and preserve Windows, Linux, and macOS compatibility.

### Validation
- Validated against a real Windows Steam installation.
- Confirmed automatic discovery of installed Steam titles.
- Confirmed successful launch of three separate Steam games.
- Confirmed fullscreen game operation does not disrupt J-29.
- Confirmed J-29 returns to the correct Program Information screen after game exit.

### Roadmap
- v0.24 Steam Support is complete.
- ROM/emulator dispatch remains reserved for v0.25 Emulator Support.


## v0.25 — Emulator Support — READY FOR VALIDATION

### Added
- Cross-platform emulator profile configuration in `config/emulators.ini`.
- Engine-level ROM launch dispatch.
- Explicit per-game emulator profile selection.
- Automatic platform-to-emulator profile matching when no emulator is specified.
- Per-OS emulator executable configuration for Windows, Linux, and macOS.
- Configurable emulator argument templates using `{rom}`.
- Initial example profiles for RetroArch, Dolphin, PCSX2, and PPSSPP.

### Architecture
- Emulator-specific behavior remains in the engine layer.
- Terminal and future shells launch ROM records without knowing emulator command lines.
- Missing ROMs, profiles, or emulator executables fail safely instead of crashing J-29.

### Validation
- Awaiting validation against a real emulator and ROM before v0.25 is marked complete.
