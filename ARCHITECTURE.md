# J29 Terminal Engine — Architecture

## Purpose

J29 began as a single Python/Tkinter application designed to create a retro terminal-style game launcher for the Callisto J-29 computer project.

As development progressed, the project expanded beyond a single custom launcher.

The architecture is now intentionally divided into four major layers:

- Engine
- Shell
- Theme
- Identity

This separation allows J29 to remain flexible, extensible, and easier to maintain.

---

# Core Design Rule

> Engine = what the machine can do  
> Shell = how the user interacts with it  
> Theme = how the shell looks and sounds  
> Identity = whose fictional machine it is

No single shell, theme, or fictional manufacturer should be permanently hardcoded into the core engine.

---

# Engine

The Engine contains shared functionality that should work regardless of which user interface is active.

Planned responsibilities include:

- Game library management
- Game launching
- Steam launching
- Emulator launching
- Game metadata
- Favorites
- Recent games
- Physical media detection
- Media metadata
- System information
- Configuration management
- Hardware integrations
- OLED / auxiliary display support
- Logging
- Future archive and lore services

The Engine should not care whether the user is interacting through:

- A green terminal
- A graphical desktop
- A console-style interface
- A community-created shell

Example conceptual calls:

    engine.get_games()
    engine.launch_game(game_id)
    engine.get_system_info()
    engine.get_recent_games()
    engine.get_favorites()
    engine.get_media_status()

The exact API will evolve during development.

---

# Shell

A Shell controls the user experience.

The first official shell is:

**J-29 Terminal Shell**

The Terminal Shell currently provides:

- Fullscreen interface
- CRT scanlines
- Keyboard navigation
- Startup sequence
- System information
- Game Library
- Blinking cursor
- Retro terminal presentation

Future shells may provide completely different interaction models while using the same Engine.

Potential future shells:

- Retro Console Shell
- Linux-style Shell
- 1980s Computer Shell
- 1990s Desktop Shell
- Early-2000s Desktop-Inspired Shell
- Community-created shells

---

# Shell Compatibility

Each shell will eventually contain a manifest.

Concept example:

    [SHELL]

    name=J-29 Terminal
    version=1.0
    engine_api=1

The Engine will verify that the shell supports the installed Engine API before loading it.

If compatibility requirements are not met, the shell should fail gracefully rather than crash the application.

Example message:

    SHELL INCOMPATIBLE

    REQUIRED ENGINE API: 2
    INSTALLED ENGINE API: 1

    INSTALL A COMPATIBLE SHELL OR UPDATE
    THE J29 TERMINAL ENGINE.

---

# Theme

A Theme changes presentation without changing the Shell's fundamental behavior.

Possible theme settings include:

- Primary text color
- Secondary text color
- Background color
- Fonts
- Font sizes
- Cursor appearance
- Scanlines
- CRT effects
- Audio
- Background assets
- Icons or graphical resources

Concept folder:

    themes/
        callisto_green/
            theme.ini
            sounds/
            fonts/
            images/

Concept theme file:

    [THEME]

    name=Callisto Green

    [COLORS]

    background=#000000
    primary=#39FF14
    secondary=#167A10
    footer=#0D520A

    [DISPLAY]

    scanlines=true
    scanline_spacing=6
    flicker=true
    glow=true

Themes should be replaceable without modifying the core Engine.

---

# Identity

Identity defines the fictional computer presented to the user.

Identity should be configuration-driven.

Possible fields:

- Manufacturer
- System name
- Model
- Unit ID
- Owner
- Location

Reference configuration:

    Manufacturer: Callisto Computer Systems
    System Name: J-29 Terminal OS
    Model: J-29 Personal Terminal
    Unit ID: J29-001

Alternate configuration:

    Manufacturer: Solar Hardware Systems
    System Name: Pigeonaut OS
    Model: SHS-01

The same Engine and Shell should support both without source-code changes.

Identity values should eventually appear dynamically in:

- Startup screens
- System Information
- Maintenance screens
- Footer/status displays
- OLED output
- Physical media messages
- Dynamic lore
- Other fictional-computer presentation

---

# Configuration

Machine-specific values should live outside the source code.

Planned configuration areas:

    config/
        identity.ini
        settings.ini
        games.ini

User-specific configuration files may be excluded from the public Git repository.

Example files should be provided for documentation and setup.

---

# Physical Media Architecture

Physical media is treated as a logical concept rather than a single device type.

Supported targets may include:

- Floppy disks
- SD cards
- microSD cards
- USB drives
- External SSDs
- External HDDs
- Other removable storage

The Engine should identify the media's role through metadata rather than assuming a particular drive letter.

Concept metadata file:

    J29MEDIA.INI

Possible media roles:

- Single game
- Multi-game collection
- Software archive
- Configuration media
- Maintenance media
- Lore/archive media

Example:

    [MEDIA]

    type=GAME
    title=DOOM
    game_id=DOOM_1993

The Shell may then display:

    MEDIA DETECTED

    DOOM

    LOAD GAME?

    [Y/N]

---

# Future Lore Architecture

Lore is planned as a post-v1.0 feature.

Two categories are anticipated:

## Dynamic Lore

Dynamic lore may contain variables such as:

    {MANUFACTURER}
    {SYSTEM_NAME}
    {MODEL}
    {UNIT_ID}
    {OWNER}
    {LOCATION}

These values will be replaced using the current machine identity.

## Canonical Lore

Canonical lore belongs to a fixed fictional universe and should not change with the user's configured identity.

Example:

    CALLISTO COMPUTER SYSTEMS
    PROJECT JANUS

Canonical lore packs remain fixed even when loaded on a differently branded system.

---

# Repository Direction

Beginning with v0.14, the project will gradually transition toward a structure similar to:

    J29-Terminal-Engine/
    |
    |-- main.py
    |
    |-- engine/
    |   |-- __init__.py
    |   |-- core.py
    |   |-- games.py
    |   |-- system_info.py
    |   |-- config.py
    |   `-- launcher.py
    |
    |-- shells/
    |   |-- __init__.py
    |   `-- terminal/
    |       |-- terminal_ui.py
    |       |-- screens.py
    |       |-- commands.py
    |       `-- effects.py
    |
    |-- themes/
    |   `-- callisto_green/
    |       |-- theme.ini
    |       |-- sounds/
    |       |-- fonts/
    |       `-- images/
    |
    |-- config/
    |   |-- identity.example.ini
    |   |-- settings.example.ini
    |   `-- games.example.ini
    |
    |-- docs/
    |
    |-- README.md
    |-- ROADMAP.md
    |-- CHANGELOG.md
    |-- ARCHITECTURE.md
    |-- CONTRIBUTING.md
    |-- LICENSE
    `-- .gitignore

This structure is a target, not a requirement to complete all at once.

The v0.14 refactor should be incremental and preserve working behavior throughout the transition.

---

# Architecture Pivot — Why It Happened

The original prototype was intentionally simple.

A single `j29.py` file was sufficient to prove:

- The retro terminal concept
- Game launching
- System information
- CRT presentation
- Keyboard navigation
- External configuration

As additional goals emerged, including:

- Configurable identities
- Themes
- Physical media
- Multiple interface styles
- Community shells
- Steam
- Emulators
- Lore
- Hardware integrations

continuing to place all functionality into one file would make the software increasingly difficult to maintain.

The architecture pivot was therefore made before the project became deeply coupled to the original prototype.

The v0.13 prototype remains preserved as a historical and functional reference.

---

# Development Principle

The modular architecture must not become an excuse to overcomplicate the project.

Each refactor should have a practical reason.

Development will continue using:

> Big vision. Small versions. Stable checkpoints.

The immediate priority remains delivering a stable v1.0 J-29 Terminal experience.

## v0.25 Emulator Layer

ROM launching is handled by `engine/emulators.py`. Shells provide a game
record to the engine; they do not construct emulator command lines.

`config/emulators.ini` maps emulator profile IDs and platforms to
OS-specific executables and argument templates. This keeps Windows, Linux,
and macOS differences out of the shell and allows emulator configuration
without modifying source code.


## Standalone emulator auto-detection

For PS2, PS3, GameCube/Wii, and PSP, the engine prefers dedicated emulator detection (PCSX2, RPCS3, Dolphin, PPSSPP) before RetroArch. Explicit emulator profiles remain the highest-priority override. Shell code remains emulator-agnostic.
