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

## v0.13 — Stable Prototype

Completed:

- Fullscreen terminal interface
- CRT scanlines
- Canvas-rendered interface
- Blinking terminal cursor
- Animated startup sequence
- Real CPU information
- Real memory information
- Real storage information
- Keyboard navigation
- Game Library
- External `games.ini`
- External program launching
- System Information screen
- Development maintenance shortcuts

v0.13 represents the final version of the original monolithic prototype.

---

# Architecture Pivot

Beginning with v0.14, J29 will transition from a single application into a modular frontend engine.

The software will be separated into four major concepts:

## Engine

Handles what the system can do.

Examples:

- Game launching
- Library management
- Emulator support
- Steam launching
- Physical media detection
- Metadata
- Favorites
- Recent games
- System information
- Configuration
- Hardware integrations

## Shell

Controls how the user interacts with the engine.

The first official shell will be:

**J-29 Terminal Shell**

Future shells may provide completely different interfaces while using the same engine.

## Theme

Controls how a shell looks and sounds.

Examples:

- Colors
- Fonts
- Scanlines
- CRT effects
- Sounds
- Background assets
- Cursor appearance

## Identity

Defines the fictional computer itself.

Examples:

- Manufacturer
- System name
- Model
- Unit ID
- Owner
- Location

The engine must not permanently hardcode the Callisto or J-29 identity.

---

# v0.14 — Core Engine Separation

### Goal

Refactor the v0.13 prototype into the first modular architecture.

### Planned Work

- Preserve v0.13 unchanged as the reference prototype
- Create engine package
- Create shell package
- Move hardware detection out of the UI
- Move game-launching logic out of the UI
- Separate configuration loading
- Establish clean entry point
- Confirm the J-29 Terminal Shell still behaves like v0.13

### Completion Requirement

The terminal must work exactly as before while core functionality is separated from presentation.

---

# v0.15 — Identity & Configuration Engine

### Goal

Remove machine-specific identity information from the source code.

### Planned Settings

- Manufacturer
- System name
- Model
- Unit ID
- Owner
- Location
- Version display

Example:

    Manufacturer: Callisto Computer Systems
    System Name: J-29 Terminal OS
    Model: J-29 Personal Terminal
    Unit ID: J29-001

Another user could configure:

    Manufacturer: Solar Hardware Systems
    System Name: Pigeonaut OS
    Model: SHS-01

without modifying Python source code.

---

# v0.16 — Theme System

### Goal

Move presentation settings outside the shell code.

### Planned Theme Options

- Primary color
- Secondary color
- Background color
- Font
- Font sizes
- Cursor style
- Scanline spacing
- Scanline intensity
- CRT effects
- Sound profile

### Goal

Users should eventually be able to install or create themes without modifying the engine.

---

# v0.17 — First-Run Setup

### Goal

Allow a fresh installation to configure itself without editing files manually.

### Setup Wizard

- Manufacturer
- System name
- Model
- Unit ID
- Display profile
- Audio profile
- Maintenance password
- Basic terminal preferences

After setup, the terminal behaves as though that identity has always belonged to the machine.

---

# v0.18 — Dynamic Footer

### Goal

Add a context-sensitive control and status bar.

Example:

    ↑↓ MOVE   ENTER SELECT   ESC BACK   HELP COMMANDS

Different screens will display different hints.

Future status indicators may include:

    OFFLINE   MEDIA READY   J29 ENGINE

---

# v0.19 — Terminal Command System

### Goal

Allow typed commands as an alternative to menu navigation.

Initial commands may include:

    HELP
    GAMES
    DIR
    LS
    SYSINFO
    CLEAR
    BACK
    REBOOT
    SHUTDOWN

Future support:

    RUN DOOM

Menus and typed commands will coexist.

---

# v0.20 — Filesystem-Style Library Browser

### Goal

Allow users to browse their game library like a retro filesystem.

Example:

    GAMES/

    [DIR] DOS
    [DIR] WINDOWS
    [DIR] SNES
    [DIR] STEAM

Navigation will support:

- Arrow keys
- Enter
- Escape
- Terminal commands

---

# v0.21 — Game Metadata

### Goal

Replace simple name/path entries with structured game information.

Possible metadata:

- Title
- Platform
- Release year
- Genre
- Launch type
- Executable path
- ROM path
- Emulator
- Steam ID
- Favorite status

---

# v0.22 — Favorites

### Goal

Allow users to mark frequently used games as favorites.

Planned features:

- Add favorite
- Remove favorite
- Favorites view
- Favorites command

---

# v0.23 — Recent Games

### Goal

Track recently launched software.

Possible display:

    RECENT SOFTWARE

    DOOM
    QUAKE
    FALLOUT

---

# v0.24 — Steam Support

### Goal

Allow Steam games to appear alongside local games.

The shell should not need to know whether a game comes from Steam or another launch method.

The engine handles launching.

---

# v0.25 — Emulator Support

### Goal

Allow ROMs to launch automatically through configured emulators.

Example:

    Platform: SNES
    ROM: SuperMarioWorld.sfc
    Emulator: RetroArch

The user selects the game.

The engine determines how to launch it.

---

# v0.26 — Physical Media System

### Goal

Bring physical interaction back to digital game libraries.

Physical media support will be format-agnostic.

Potential media:

- Floppy disks
- SD cards
- microSD cards
- USB flash drives
- External SSDs
- External HDDs
- Other removable storage

J29 identifies what the media represents rather than relying on a specific drive type.

Example:

    MEDIA DETECTED


    DOOM


    LOAD GAME?

    [Y/N]

Physical media may represent a game without necessarily storing the complete game itself.

---

# v0.27 — Media Metadata & Collections

### Goal

Introduce a standard J29 media format.

Possible metadata file:

    J29MEDIA.INI

Possible media types:

- Single game
- Multi-game collection
- Software archive
- Configuration media
- Maintenance media
- Future lore archive media

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