## v0.28.0 — Custom Audio Foundation — TEST BUILD

### Added
- New engine-level `AudioManager` service in `engine/audio.py`.
- Dependency-free asynchronous WAV playback for Windows, macOS, and Linux host environments.
- Failure-safe audio behavior: missing files or unavailable host playback tools fall back to silence without interrupting J-29.
- Runtime `enabled` and `master_volume` support using the existing `[AUDIO]` settings.
- Cached PCM WAV volume scaling so theme sounds can honor J-29 master volume without a third-party audio library.
- Theme-owned audio mappings under each theme's `[AUDIO]` section.
- Reference Callisto sound set for boot, menu movement, selection, error, media detection, access granted, access denied, game launch, and shutdown.

### Wired Events
- Boot / reboot startup tone.
- Menu movement feedback on navigable lists.
- Selection feedback for menu, library, favorites, recent, and physical-media confirmation.
- Error feedback for unknown commands and failed program launches.
- Physical-media insertion acknowledgement.
- Maintenance/windowed-mode access-granted tone.
- Universal launch-transition tone before the existing launch engine dispatch.
- Clean terminal shutdown tone.

### Architecture
- Audio remains an engine service while sound identity remains theme data.
- Terminal UI requests semantic events such as `menu_move`, `media_detected`, and `launch`; it does not know filenames or playback backends.
- `access_denied` is included in the theme/API now and is reserved for the secured maintenance authorization flow.

### Status
TEST BUILD — requires real J-29 hardware/audio validation before v0.28 is marked complete.

---

## v0.27 — Media Metadata & Collections — COMPLETE

### Added
- Standard `j29-media.ini` metadata format for J-29 physical media.
- Self-contained game media with explicit ROM paths.
- Metadata-only launch keys that resolve existing J-29 library entries by stable `game_id`.
- Steam launch keys using existing `STEAM_<appid>` library IDs.
- `type=COLLECTION` media containing multiple launchable entries.
- Collection browser inside the Terminal Shell with keyboard navigation and repeated launching without closing the collection.
- Dynamic `PHYSICAL MEDIA` main-menu entry while recognized media remains mounted.
- Boot-time detection of already-inserted recognized J-29 media.
- Example J-29 media configuration for single-game and collection formats.

### Changed
- Physical media now represents software rather than requiring the complete software payload to reside on the removable device.
- `game_id` takes precedence when both a library target and local ROM path are defined.
- Current mounted media can be reopened from the main menu without requiring physical reinsertion.
- Main-menu navigation now supports dynamic entries safely instead of relying on fixed indexes.

### Fixed
- Metadata ROM paths now accept either Windows-style or portable path separators.
- Missing metadata ROMs report the resolved expected path instead of a generic failure.
- Failed physical-media launches restore the true media-prompt state so `ESC` / `N` works normally.
- Hot removal from an open collection safely returns to the main menu.
- Invalid collection `game_id` entries report failure without damaging collection state.
- Media present before J-29 startup is now recognized during boot when it contains valid J-29 metadata or recognizable software.

### Real Hardware Validation
- Self-contained metadata + ROM media: PASS.
- Metadata-only local ROM launch key: PASS.
- Metadata-only Steam launch key: PASS.
- Multi-entry collection media: PASS.
- Launching multiple games while collection remains open: PASS.
- Reopening mounted media through dynamic `PHYSICAL MEDIA`: PASS.
- Dynamic menu removal after physical ejection: PASS.
- Invalid collection library ID recovery: PASS.
- Hot removal while inside collection: PASS.
- Reinsertion after hot removal: PASS.
- Boot with recognized physical media already inserted: PASS.

### Significance
J-29 physical media can now act as a self-contained software carrier, a lightweight physical launch key for software stored elsewhere, or a multi-program collection. The physical object is the interface; the underlying software may live on removable media, local storage, or Steam.

---

## v0.26.1 — Universal Launch Transition — COMPLETE

### Improved
- Added one shared launch-transition experience for Steam games, local ROMs,
  physical-media ROMs, configured executables, Favorites, and Recent Games.
- J-29 now acknowledges RUN immediately with a dedicated
  `LAUNCHING PROGRAM... / PLEASE WAIT` screen while Steam or an emulator starts.
- The correct J-29 context is restored behind the external application so the
  user returns to the expected screen when the game exits.
- Terminal navigation is ignored during the brief external-program handoff.
- Failed launches restore context and continue to show the existing diagnostic
  launch error.

### Validation
- Universal launch transition validated successfully after v0.26 hardware
  validation.
- User confirmed the transition is substantially cleaner than exposing the
  previous menu during emulator or Steam startup latency.

---

## v0.26 — Physical Media System — COMPLETE

### Added
- Cross-platform physical-media detection foundation for removable media.
- Runtime insertion and removal monitoring.
- Automatic recognition of single-ROM removable media.
- `MEDIA DETECTED` / `LOAD GAME? [Y/N]` terminal prompt.
- Physical-media ROMs launch through the existing emulator pipeline.
- Multiple simultaneous insertion events are queued safely.
- Duplicate insertion events for the same mounted media are ignored.
- Reinsertion after removal is treated as a fresh media event.

### Windows Integration
- Windows mounted-volume discovery supports removable media and USB storage
  devices that may report as fixed disks.
- Empty USB/SD reader slots are ignored rather than treated as mounted media.
- Mounted-media identity uses volume information rather than drive letter alone,
  allowing SD-card readers that retain the same drive letter to work correctly.
- Fixed Terminal startup so the recurring physical-media polling chain actually
  begins when the UI launches.

### Safety
- Removing media while `LOAD GAME?` is displayed cancels the prompt cleanly.
- Queued entries for removed media are discarded.
- J-29 verifies media still exists before attempting a launch.
- Removal events are nonfatal and display `MEDIA REMOVED`.

### Real Hardware Validation
- SD card inserted into an already-connected USB reader: PASS.
- Full USB reader removal: PASS.
- `MEDIA REMOVED` notification: PASS.
- Full reader reinsertion with fresh detection prompt: PASS.
- Removal while the load prompt is open: PASS.
- Physical-media ROM launch through RetroArch: PASS.
- Repeated remove / insert / load / launch cycles: PASS.

---

## v0.25.1 — Long-List Scrolling Polish — COMPLETE

### Improved
- Added centered scrolling for long Game Library lists.
- Selected entries stay visible and approximately centered during navigation.
- Added stronger footer/bottom-screen safety.
- Applied the same behavior to Game Library, Favorites, and Recent Games.

### Validation
- Real UI validation passed; long lists no longer disappear beneath the footer.

---

## v0.25 — Emulator Support — COMPLETE

### Added
- Emulator profiles and automatic ROM launching through configured emulators.
- Cross-platform emulator configuration foundation.
- Automatic ROM-library discovery from configured folders.
- Stable generated IDs for discovered ROMs.
- Manual game records override automatically discovered ROMs with the same path.
- RetroArch core selection based on platform and installed cores.
- Ordered core fallback lists for supported platforms.
- Clear visible launch diagnostics when a required emulator/core is unavailable.
- Standalone emulator auto-detection foundation for:
  - PCSX2
  - RPCS3
  - Dolphin
  - PPSSPP
- Dedicated standalone emulator priority where appropriate, with RetroArch used
  for supported systems.

### Real Hardware Validation
- SNES: PASS.
- NES: PASS.
- Nintendo 64: PASS.
- Game Boy Advance: PASS.
- Game Boy Color: PASS.
- Sega Genesis: PASS.
- RetroArch fullscreen launch and return to J-29 metadata screen: PASS.
- Standalone PCSX2/RPCS3/Dolphin/PPSSPP real-world testing deferred to the final
  release-candidate regression because matching local hardware/software test
  cases were not available during v0.25.

---
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
