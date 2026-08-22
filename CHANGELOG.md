# Changelog

All notable development milestones for the J29 Terminal Engine will be documented here.

The project currently uses small development versions so each stable milestone can be tested, preserved, and documented before moving forward.

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