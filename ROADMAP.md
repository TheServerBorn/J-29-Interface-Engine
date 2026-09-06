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

## v0.28.1 — Custom Audio / Callisto Audio Identity

### Status

**COMPLETE — CROSS-HARDWARE VALIDATED**

### Goal

Give J-29 configurable, theme-owned audio feedback that feels like part of the machine rather than a layer added on top of it.

### Completed

- Engine-level `AudioManager` service
- Theme-owned semantic sound mappings
- Runtime audio enable/disable control
- Master-volume support
- Failure-safe handling for missing or unavailable sound files
- Boot / reboot sound
- Menu movement sound
- Selection / confirmation sound
- Error sound
- Physical-media detection sound
- Access-granted sound
- Access-denied API / sound
- Universal game-launch transition sound
- Shutdown sound
- Rapid menu-repeat throttling so navigation audio cannot build a delayed backlog
- Physical-media polling tightened from 2000 ms to 500 ms for faster media acknowledgement
- Persistent Windows audio-output path so very short terminal sounds are not swallowed by hardware / endpoint startup latency
- Callisto Rev C industrial terminal sound identity adopted as the current reference set

### Audio Identity

The current Callisto reference sound set uses:

- Dry mechanical key / relay clicks
- Muted CRT-era electronic beeps
- Low-fi industrial texture
- Minimal melody
- Short, restrained acknowledgements
- One cohesive retro-futuristic terminal palette

### Cross-Hardware Validation

- Windows laptop: PASS
- Windows desktop: PASS
- Short one-shot WAV playback through persistent Windows audio path: PASS
- Rapid menu-repeat stress test: PASS
- Audio enable/disable: PASS
- Master-volume control: PASS
- Missing-sound failure handling: PASS
- Physical-media detection cue at 500 ms polling interval: PASS

### Windows Integration Requirement

The guided first-run setup must explain and help the user configure the host so Windows does not interrupt the J-29 physical-media experience:

- Disable AutoPlay for removable drives
- Disable Windows Device Connect sound
- Disable Windows Device Disconnect sound
- Keep removable-drive mounting enabled
- Explain changes before applying them
- Provide a physical-media verification step after configuration

### Architecture Principle

> **The engine requests semantic audio events; themes define how those events sound.**

The Terminal Shell should not depend on specific filenames or a specific host playback backend.

---

# Previous Completed Milestone

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

---

# v0.28 — Custom Audio

### Status

**COMPLETE — v0.28.1 CROSS-HARDWARE VALIDATED**

Custom Audio is now part of the stable J-29 foundation. Further sound changes should be treated as normal polish or theme work rather than expansion of the milestone.

---

# v0.29 — Physical Media Creator

### Goal

Turn J-29 physical-media authoring into a normal user workflow so users do not need to manually edit `j29-media.ini` files or look up internal game IDs.

Planned workflow:

    MEDIA TOOLS
    CREATE MEDIA
    SELECT GAME(S)
    SELECT TARGET MEDIA
    WRITE MEDIA

Planned capabilities:

- Detect writable removable media selected by the user
- Browse and select games from the installed J-29 library
- Create metadata-only launch keys automatically
- Create multi-game collection media automatically
- Write the correct stable `game_id`, title, platform, and media type without exposing internal IDs to normal users
- Support naming collections and choosing collection order
- Validate the target before writing
- Avoid accidental writes to non-removable or system storage
- Preserve manual `j29-media.ini` authoring for advanced users
- Reopen newly created media through the existing Physical Media workflow for immediate validation

Self-contained media copying may be included only if it can be implemented safely without expanding scope; launch-key and collection authoring are the required v1.0 functionality.

### Design Principle

> **Users choose the software. J-29 writes the metadata.**

The INI format remains open and editable, but it becomes an implementation detail rather than a setup requirement for ordinary users.

---

# v0.30 — OLED / Auxiliary Display Support

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

# v0.31 — Maintenance Terminal

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

# v0.32 — Appliance Mode

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

# v0.33 — Boot Maintenance Console

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

# v0.34 — Deployment Build

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

# v0.35–v0.99 — Stabilization

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
- Audio playback across different Windows audio endpoints
- First-run Windows integration verification

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
- Built-in physical media creator for launch keys and collections
- Favorites
- Recent games
- Game metadata
- Custom sounds
- Maintenance environment
- First-run configuration
- Guided Windows integration for removable-media AutoPlay and device sounds
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