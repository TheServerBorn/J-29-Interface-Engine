# J29 Terminal Engine

A customizable retro-computing frontend engine for games, physical media, and fictional computer interfaces.

## Project Status

**Stable Development Release:** v0.19 — Terminal Command System 
**Current Development:** v0.20 — Filesystem-Style Library Browser

J29 began as a custom retro terminal launcher for the Callisto J-29 computer project.

The project has since evolved into a modular retro-computing frontend engine designed to support configurable fictional computers, game libraries, physical media, themes, and eventually multiple user-interface shells.

The original **J-29 Terminal OS** remains the reference implementation and the target experience for version 1.0.

> **Big vision. Small versions. Stable checkpoints. No chaos.**

---

## Current Architecture

Beginning with v0.14, J29 is built around four major concepts:

### Engine

Handles what the computer can do.

Current Engine responsibilities include:

- Game library loading
- External program launching
- CPU detection
- Memory detection
- Storage information
- Host operating system detection
- Shared configuration loading
- Machine identity loading
- Application settings loading

### Shell

Controls how the user interacts with the Engine.

The current reference Shell is:

**J-29 Terminal Shell**

The Terminal Shell communicates with the Engine through the shared `J29Engine` interface rather than accessing individual Engine modules directly.

### Theme

Controls how a Shell looks and sounds.

Theme architecture is planned for a future development milestone.

### Identity

Defines the fictional computer presented to the user.

Identity information is now externally configurable and does not require Python source-code changes.

---

## Current Features

### Terminal Interface

- Fullscreen retro terminal interface
- Green-on-black presentation
- CRT-style scanlines
- Canvas-rendered interface
- Animated startup sequence
- Blinking block cursor
- Keyboard-driven navigation
- Game Library screen
- System Information screen
- Development fullscreen/window controls

### Core Engine

- Modular Engine package
- Shared `J29Engine` interface
- Separate Terminal Shell package
- Clean `main.py` application entry point
- Legacy `j29.py` compatibility launcher

### Hardware Information

J29 currently reads real host-system information including:

- CPU model
- Installed memory
- Host operating system
- System drive
- Total storage capacity
- Available storage space

### Game Library

- External game configuration
- Configurable game names and executable paths
- External application launching
- Missing-program handling
- Engine-based game loading and launching

---

## v0.15 — Identity & Configuration

Version 0.15 is currently under development.

### Implemented So Far

J29 now supports configurable machine identities using:

    config/identity.ini

Identity values include:

- Manufacturer
- System / OS name
- Model
- Version
- Unit ID
- Owner
- Location

Example reference identity:

    Manufacturer: Callisto Computer Systems
    System: J-29 Terminal OS
    Model: J-29 Personal Terminal
    Unit ID: J29-001

The same Engine can also load a completely different fictional identity without modifying Python source code.

For example:

    Manufacturer: Solar Hardware Systems
    System: Pigeonaut OS

The Terminal Shell currently uses identity configuration for:

- Boot branding
- Window title
- Terminal title
- System Information display

### Configuration Layout

Public templates are stored in:

    config/identity.example.ini
    config/settings.example.ini
    config/games.example.ini

Local user configuration is stored separately:

    config/identity.ini
    config/settings.ini
    config/games.ini

Local configuration files are ignored by Git so personal machine settings are not accidentally published.

### Settings

The Engine now loads configurable application settings including:

- Startup fullscreen behavior
- Boot sequence enable/disable
- Footer preference
- Audio enable/disable
- Master volume
- Development fullscreen key
- Development windowed-mode key

Some settings are already connected to the Terminal Shell while others are being prepared for later milestones.

---

## Reference System

The original reference configuration is:

**Manufacturer:** Callisto Computer Systems  
**System:** J-29 Terminal OS  
**Model:** J-29 Personal Terminal

The reference hardware build uses modern PC hardware presented as a fictional retro computer.

J29 itself is not tied to one specific computer enclosure or hardware platform.

---

## Reference Hardware / Case Design

The reference J29 build uses the **Raspberry Pi Retro Computer** enclosure designed by **lowbudgettech**.

**Original designer:** lowbudgettech  
**Original project:** Raspberry Pi Retro Computer  
**Thingiverse:** https://www.thingiverse.com/thing:3478048

The enclosure design is the work of its original creator and is not part of the J29 Terminal Engine software.

J29 Terminal Engine does not require this specific enclosure. The software can be used with custom cases, repurposed computers, cyberdecks, mini PCs, laptops, and other hardware.

---

## Physical Media Vision

One of the primary goals of J29 is to bring physical interaction back to digital game libraries.

Future physical media support will be format-agnostic.

Potential media include:

- 3.5-inch floppy disks
- SD cards
- microSD cards
- USB flash drives
- External SSDs
- External hard drives
- Other removable storage

J29 will identify what the media represents rather than depending on a specific physical format.

A physical disk or storage device may act as a representation or key for software already installed digitally.

Example future interaction:

    MEDIA DETECTED

    DOOM

    LOAD GAME?

    [Y/N]

Physical media support is planned but is **not yet implemented** in the current development build.

---

## Planned v1.0 Features

The roadmap toward v1.0 includes:

- Configurable machine identity
- Settings system
- Theme architecture
- First-run setup
- Dynamic footer / control hints
- Terminal command system
- Filesystem-style library browsing
- Game metadata
- Favorites
- Recently played games
- Steam integration
- Emulator / ROM launching
- Physical media
- Configurable audio
- Auxiliary OLED display support
- Maintenance environment
- Appliance-style operation
- Packaged Windows deployment

Major new features are generally being deferred until their planned roadmap milestone.

---

## Future Shells

The modular architecture is designed to eventually support alternate interfaces without replacing the Engine.

Possible future Shells include:

- Retro console interfaces
- Linux-console-style interfaces
- 1980s-inspired fictional computers
- 1990s-inspired graphical desktops
- Early-2000s-inspired graphical systems
- Community-created Shells

The J-29 Terminal remains the official reference Shell.

---

## Future Themes

Themes will eventually control presentation independently from the Engine.

Possible theme elements include:

- Colors
- Fonts
- Font sizes
- Scanlines
- CRT effects
- Cursor styles
- Sounds
- Background assets
- Interface graphics

---

## Development Structure

The current project is moving toward:

    J29-Terminal-Engine/
    |
    |-- main.py
    |-- j29.py
    |
    |-- engine/
    |   |-- core.py
    |   |-- config.py
    |   |-- games.py
    |   |-- launcher.py
    |   `-- system_info.py
    |
    |-- shells/
    |   `-- terminal/
    |       `-- terminal_ui.py
    |
    |-- config/
    |   |-- identity.example.ini
    |   |-- settings.example.ini
    |   `-- games.example.ini
    |
    |-- README.md
    |-- ROADMAP.md
    |-- CHANGELOG.md
    |-- ARCHITECTURE.md
    |-- CONTRIBUTING.md
    |-- PROJECT_HISTORY.md
    `-- LICENSE

The architecture is intentionally being built incrementally rather than through one large rewrite.

---

## Open Source

J29 Terminal Engine is open-source software released under the **MIT License**.

You are free to use, modify, distribute, and build upon the software under the terms of that license.

Community participation is encouraged but not required.

Possible future community contributions include:

- Custom Shells
- Themes
- Hardware builds
- Bug fixes
- Documentation
- Compatibility improvements
- Feature ideas
- Configuration examples

See `CONTRIBUTING.md` for additional information.

---

## Development Philosophy

J29 development follows a simple rule:

> **Big vision. Small versions. Stable checkpoints. No chaos.**

Each milestone is implemented, tested, documented, and preserved before development moves forward.

Stable milestones are maintained through Git branches, commits, and GitHub releases.

---

## Current Roadmap

- **v0.20 — Filesystem-Style Library Browser**
- **v0.21 — Game Metadata**
- **v0.22 — Favorites**
- **v0.23 — Recent Games**
- **v0.24 — Steam Support**
- **v0.25 — Emulator Support**

Further milestones are documented in [`ROADMAP.md`](ROADMAP.md).

---

## Disclaimer

J29 Terminal Engine is experimental software under active development.

Interfaces, configuration formats, and internal APIs may change before version 1.0.
