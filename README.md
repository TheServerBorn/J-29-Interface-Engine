# J-29 Interface Engine

A modular retro-computing interface engine for games, physical media, and fictional computer systems.

## Project Status

**Stable Development Release:** v0.27 — Media Metadata & Collections
**Current Development:** v0.28 — Custom Audio

J-29 began as a custom retro terminal launcher for the Callisto J-29 computer project.

The project has since evolved into a modular retro-computing interface engine designed to support configurable fictional computers, game libraries, physical media, themes, and multiple user-interface shells.

The original **J-29 Terminal OS** remains the reference implementation and the target experience for version 1.0.

> **Big vision. Small versions. Stable checkpoints. No chaos.**

---

## Current Architecture

J-29 is built around four major concepts:

### Engine

Handles what the computer can do.

Current Engine responsibilities include:

- Game library loading
- Game metadata and persistent library state
- Steam discovery and launching
- ROM discovery and emulator launching
- Physical-media detection, metadata, launch keys, and collections
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

This separation allows alternate graphical or text-based Shells to use the same underlying Engine without rewriting the core application logic.

### Theme

Controls how a Shell looks and sounds.

Theme support is now part of the project architecture and is being expanded incrementally.

Current and future theme elements may include:

- Colors
- Fonts
- Font sizes
- Scanlines
- CRT effects
- Cursor styles
- Sounds
- Background assets
- Interface graphics

Themes are intended to remain separate from Engine functionality so the appearance of a fictional computer can change without altering the underlying application logic.

### Identity

Defines the fictional computer presented to the user.

Identity information is externally configurable and does not require Python source-code changes.

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
- Terminal command system

### Core Engine

- Modular Engine package
- Shared `J29Engine` interface
- Separate Terminal Shell package
- Clean `main.py` application entry point
- Legacy `j29.py` compatibility launcher
- Shared configuration system
- Configurable machine identity
- Configurable application settings
- Theme architecture

### Hardware Information

J-29 currently reads real host-system information including:

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

### Terminal Commands

The J-29 Terminal Shell includes a command system that provides an alternate method of interacting with the interface alongside keyboard menu navigation.

The command architecture is designed to expand as additional Engine features are introduced.

---

## Identity & Configuration

J-29 supports configurable machine identities using:

```text
config/identity.ini
```

Identity values include:

- Manufacturer
- System / OS name
- Model
- Version
- Unit ID
- Owner
- Location

Example reference identity:

```text
Manufacturer: Callisto Computer Systems
System: J-29 Terminal OS
Model: J-29 Personal Terminal
Unit ID: J29-001
```

The same Engine can load a completely different fictional identity without modifying Python source code.

For example:

```text
Manufacturer: Solar Hardware Systems
System: Pigeonaut OS
```

The Terminal Shell currently uses identity configuration for:

- Boot branding
- Window title
- Terminal title
- System Information display

### Configuration Layout

Public templates are stored in:

```text
config/identity.example.ini
config/settings.example.ini
config/games.example.ini
```

Local user configuration is stored separately:

```text
config/identity.ini
config/settings.ini
config/games.ini
```

Local configuration files are ignored by Git so personal machine settings are not accidentally published.

### Settings

The Engine loads configurable application settings including:

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

The **J-29 Interface Engine itself is not tied to one specific fictional computer, enclosure, or hardware platform.**

The Callisto J-29 is the official reference implementation used to develop and demonstrate the Engine.

---

## Reference Hardware / Case Design

The reference J-29 build uses the **Raspberry Pi Retro Computer** enclosure designed by **lowbudgettech**.

**Original designer:** lowbudgettech  
**Original project:** Raspberry Pi Retro Computer  
**Thingiverse:** https://www.thingiverse.com/thing:3478048

The enclosure design is the work of its original creator and is not part of the J-29 Interface Engine software.

J-29 Interface Engine does not require this specific enclosure.

The software can be used with:

- Custom computer cases
- Repurposed computers
- Cyberdecks
- Mini PCs
- Laptops
- Single-board computers
- Other custom hardware projects

---

## Physical Media

Physical media is now a working core feature of J-29. The system is format-agnostic and can recognize supported media such as SD cards, USB storage, external drives, and other mounted removable media.

J-29 follows one central rule:

> **Physical media represents software. It does not require the software to physically reside on that media.**

A medium can work in three ways:

- **Self-contained media** — metadata plus the actual ROM/software payload.
- **Launch key** — a tiny metadata file points to an existing J-29 library entry, including local ROMs or Steam titles.
- **Collection media** — one physical object exposes multiple launchable programs through an in-terminal collection browser.

Example single-game launch key:

```ini
[J29_MEDIA]
type=GAME
title=HARVEST MOON
platform=SNES
game_id=ROM_SNES_6009C68D2439
```

Example collection:

```ini
[J29_MEDIA]
type=COLLECTION
title=J-29 FAVORITES

[ITEM_1]
title=HARVEST MOON
platform=SNES
game_id=ROM_SNES_6009C68D2439

[ITEM_2]
title=MOONSTONE ISLAND
platform=PC
game_id=STEAM_1658150
```

When recognized media is mounted, a dynamic **PHYSICAL MEDIA** option appears on the main menu. Already-inserted recognized media is detected during J-29 startup, and removing the media removes the menu entry automatically.

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

Major new features are generally deferred until their planned roadmap milestone.

Completed roadmap features remain listed here because they form part of the intended v1.0 feature set.

---

## Future Shells

The modular architecture is designed to support alternate interfaces without replacing or rewriting the Engine.

Possible future Shells include:

- Retro console interfaces
- Linux-console-style interfaces
- 1980s-inspired fictional computers
- 1990s-inspired graphical desktops
- Early-2000s-inspired graphical systems
- Community-created Shells

The **J-29 Terminal Shell** remains the official reference Shell.

A future Shell may present a completely different visual interface while continuing to use the same underlying Engine for games, hardware information, configuration, media handling, and other shared functionality.

---

## Future Themes

Themes control presentation independently from the Engine.

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

The theme system is intended to allow different fictional machines and visual styles to share the same Shell and Engine architecture.

---

## Development Structure

The current project structure is moving toward:

```text
J-29-Interface-Engine/
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
|-- themes/
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
```

The architecture is intentionally being built incrementally rather than through one large rewrite.

---

## Open Source

J-29 Interface Engine is open-source software released under the **MIT License**.

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

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for additional information.

---

## Development Philosophy

J-29 development follows a simple rule:

> **Big vision. Small versions. Stable checkpoints. No chaos.**

Each milestone is implemented, tested, documented, and preserved before development moves forward.

Stable milestones are maintained through Git branches, commits, tags, and GitHub releases.

---

## Current Roadmap

- **v0.20 — Filesystem-Style Library Browser** ✅
- **v0.21 — Game Metadata** ✅
- **v0.22 — Favorites** ✅
- **v0.23 — Recent Games**✅
- **v0.24 — Steam Support** ✅
- **v0.25 — Emulator Support** ✅
- **v0.25.1 — Long-List Scrolling Polish** ✅
- **v0.26 — Physical Media System** ✅
- **v0.26.1 — Universal Launch Transition** ✅
- **v0.27 — Media Metadata & Collections** ✅
- **v0.28 — Custom Audio** 🚧

Further milestones are documented in [`ROADMAP.md`](ROADMAP.md).

---

## Disclaimer

J-29 Interface Engine is experimental software under active development.

Interfaces, configuration formats, internal APIs, Shell behavior, and feature organization may change before version 1.0.

The Callisto Computer Systems setting, J-29 Terminal OS, and related fictional systems are used as the reference environment for development and demonstration of the Engine.

Interfaces, configuration formats, and internal APIs may change before version 1.0.
