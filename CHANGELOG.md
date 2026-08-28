# Changelog

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