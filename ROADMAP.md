# J29 Terminal Engine — Development Roadmap

## Project Goal

J29 Terminal Engine is a customizable retro-computing frontend designed to make modern hardware feel like a fictional computer system.

The initial v1.0 release will focus on the original J-29 vision:

- Retro terminal interface
- Unified game launching
- Physical media interaction
- Custom machine identity
- Configurable themes
- Terminal commands
- Maintenance environment
- Stable appliance-style operation

Development follows one rule:

> **Big vision. Small versions. Stable checkpoints.**

---

# Current Stable Build

## v0.27 — Media Metadata & Collections

### Status

**COMPLETE — REAL HARDWARE VALIDATED**

### Goal

Introduce a standard J-29 physical-media format in which the physical object represents software regardless of where the software payload actually resides.

### Completed

- Standard `j29-media.ini` descriptor
- `type=GAME` self-contained media using explicit ROM paths
- Metadata-only launch keys using stable J-29 `game_id` values
- Steam launch keys through existing `STEAM_<appid>` records
- `type=COLLECTION` multi-program media
- Collection browser with repeated launches while media remains open
- Dynamic `PHYSICAL MEDIA` main-menu entry while recognized media is mounted
- Reopen currently mounted media without reinsertion
- Boot-time recognition of already-inserted J-29 media
- Safe invalid-ID handling
- Safe hot-removal handling
- Fresh detection after reinsertion

### Validated

- Self-contained SNES media
- Metadata-only SNES launch key
- Metadata-only Steam launch key
- Mixed collection containing local-ROM and Steam targets
- Multiple launches from one open collection
- Broken collection target without collection-state loss
- Hot removal while collection is open
- Dynamic main-menu appearance/removal
- Boot with media already inserted

### Architecture Principle

> **J-29 physical media represents software. It does not require the software to physically reside on that media.**

This allows a floppy disk, SD card, USB device, or other supported medium to behave as a physical software object even when the actual program is stored on local storage or managed by another launcher.

---

# v0.28 — Custom Audio

### Goal

Add configurable retro audio feedback.

Possible sounds:

- Boot
- Menu movement
- Selection
- Error
- Media detected
- Access granted
- Access denied
- Game launch
- Shutdown

Sounds will be replaceable through themes.

---

# v0.29 — OLED / Auxiliary Display Support

### Goal

Allow compatible secondary displays to show terminal status.

Examples:

    J-29
    READY

or:

    DOOM
    RUNNING

or:

    MEDIA
    DETECTED

Exact hardware support will be determined during development.

---

# v0.30 — Maintenance Terminal

### Goal

Replace temporary development shortcuts with an in-universe maintenance environment.

Normal access:

    CTRL + ALT + F12

Example:

    ====================================

    CALLISTO COMPUTER SYSTEMS
    MAINTENANCE TERMINAL

    ====================================

    AUTHORIZED PERSONNEL ONLY

    PASSWORD REQUIRED

    >

Successful authorization:

    ACCESS GRANTED

    OPENING MAINTENANCE ENVIRONMENT...

Failed authorization may display:

    ACCESS DENIED

    USER NOT RECOGNIZED

    NICE TRY

The maintenance password will not be stored as plain text.

---

# v0.31 — Appliance Mode

### Goal

Make J29 behave like a dedicated computer rather than a visible Windows application.

Planned work:

- Windows auto-login
- Automatic engine startup
- Hide normal desktop during operation
- Prevent distracting notifications
- Reliable return from games
- Safe maintenance access
- Startup recovery
- Controlled shutdown/restart

---

# v0.32 — Boot Maintenance Console

### Goal

Allow maintenance access during startup.

Example:

    PRESS F12 FOR MAINTENANCE

Possible console:

    CALLISTO MAINTENANCE CONSOLE

    1. EXIT TO WINDOWS
    2. SYSTEM DIAGNOSTICS
    3. TERMINAL SETTINGS
    4. MEDIA SETTINGS
    5. RESTART TERMINAL

---

# v0.33 — Deployment Build

### Goal

Package J29 so the target machine does not require Python development tools.

Planned output:

    J29Terminal.exe

or equivalent packaged release.

Development PC:

- Python
- Source code
- Development environment

Target PC:

- J29 packaged application
- Configuration
- Assets
- Games / emulators

---

# v0.34–v0.99 — Stabilization

After the major systems are complete, development will focus on reliability rather than adding major new features.

Testing will include:

- Missing games
- Missing emulators
- Invalid media
- Removed media
- Steam unavailable
- Unsupported hardware
- Missing configuration
- Display-resolution differences
- Auxiliary display failure
- Application crashes
- Maintenance recovery
- Returning from games
- Clean shutdown
- Fresh installation

No major feature additions should occur during final stabilization unless required for v1.0 functionality.

---

# v1.0 — J29 Terminal Engine

## Initial Public Release

Version 1.0 will deliver the original J-29 vision on top of the modular engine architecture.

The reference experience will include:

- J-29 Terminal Shell
- Configurable machine identity
- Theme support
- Game Library
- Filesystem-style navigation
- Terminal commands
- Steam launching
- Emulator support
- Physical media support
- Favorites
- Recent games
- Game metadata
- Custom sounds
- Maintenance environment
- First-run configuration
- Appliance-mode operation
- Packaged deployment

The Callisto J-29 will remain the official reference build.

---

# Post-v1.0 Development

Version 1.0 marks a stable platform, not the end of development.

Future development will use optional expansions rather than unnecessarily replacing the core engine.

---

# v1.1 — Archive & Lore Expansion

### Goal

Introduce environmental storytelling inside the fictional computer.

The base system may contain:

- Hidden directories
- Text files
- Maintenance logs
- Incident reports
- Personnel records
- Undocumented commands
- Clues leading to deeper directories

Example discovery:

    > TYPE INCIDENT_04.TXT

A document may reveal:

    ARCHIVE ACCESS CODE: JANUS

The user may then discover:

    > JANUS

which exposes an undocumented archive.

---

## Expandable Lore Media

Additional story content may be distributed through physical media.

Example:

    MEDIA DETECTED

    CALLISTO ARCHIVE MEDIA

    ACCESS FILES?

    [Y/N]

Archive media may contain optional story content without permanently installing it into the base system.

The amount of future lore development will depend on community interest.

---

# Future Shell Packs

The J29 Terminal Engine will support additional interface shells after the stable 1.0 platform exists.

Possible future shells:

- Retro Console
- Linux-style terminal
- 1980s computer interface
- 1990s desktop interface
- Early-2000s desktop-inspired interface
- Community-created shells

Shells will use the same core engine.

Users who already have J29 installed should be able to add compatible shell packs without reinstalling the engine.

New users may eventually download preconfigured bundles containing the engine and their preferred shell.

---

# Shell Compatibility

Future shells will contain a manifest defining compatibility with the engine API.

Concept example:

    Shell Name: J-29 Terminal
    Shell Version: 1.0
    Engine API: 1

The engine will verify compatibility before loading a shell.

This prevents incompatible shells from silently breaking an installation.

---

# Community Vision

J29 is intended to eventually support a community of builders.

Users will be encouraged to share:

- Custom shells
- Themes
- Hardware builds
- Configuration ideas
- Feature suggestions
- Code improvements

Community participation will be encouraged, not required.

---

# Scope Freeze

The v1.0 roadmap is now considered feature-frozen.

New ideas should generally be recorded for post-v1.0 development instead of being added to the initial release unless they are required for reliability, architecture, security, or completion of an existing milestone.

The priority is now:

> **Build the roadmap. Test the roadmap. Finish the roadmap. Ship v1.0.**