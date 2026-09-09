# J-29 Interface Engine

> **Modern hardware. Retro experience.**

A modular retro-computing interface engine for games, physical media, fictional computer systems, and custom interface shells.

---

## Project Status

**Latest completed milestone:** `v0.31 — Maintenance Terminal`  
**Next development milestone:** `v0.32 — Guided First-Launch Setup`  
**Primary release target:** Windows  
**License:** MIT

J-29 began as a custom retro-terminal launcher for the **Callisto J-29 computer project**.

It has since evolved into a modular interface engine designed to support:

- Unified software libraries
- Steam
- ROMs and emulators
- Physical media
- Custom machine identities
- Themes
- Audio
- Alternate interface shells
- Custom hardware builds

The original **J-29 Terminal** remains the official reference implementation.

> **Big vision. Small versions. Stable checkpoints. No chaos.**

---

# What Is J-29?

J-29 is not intended to be another conventional game launcher.

It is an attempt to make modern hardware feel like a **dedicated fictional computer system** again.

Instead of exposing separate launchers, emulator directories, ROM folders, removable drives, and desktop shortcuts directly to the user, J-29 places them behind a unified interface.

The current Terminal Shell presents that system as a retro-futuristic computer terminal.

Future shells can present the same underlying Engine in completely different ways.

```text
                 J-29 INTERFACE ENGINE
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   GAME LIBRARY     PHYSICAL MEDIA     SYSTEM DATA
        │                │
   ┌────┼────┐       ┌───┼────┐
   │    │    │       │   │    │
 STEAM ROMS LOCAL   KEY MEDIA COLLECTION
   │    │    │
   └────┴────┴───────────────┐
                             ▼
                       LAUNCH SYSTEM
```

---

# Core Architecture

J-29 is organized around four major concepts:

1. **Engine**
2. **Shell**
3. **Theme**
4. **Identity**

---

## Engine

The Engine controls what the system can do.

Current responsibilities include:

- Game-library loading
- Persistent library state
- Game metadata
- Favorites
- Recently played software
- Steam discovery and launching
- ROM discovery
- Emulator profile handling
- Physical-media detection
- Physical-media metadata parsing
- Physical-media collections
- Physical Media Creator
- Safe removable-media writing
- External application launching
- System information
- Shared configuration
- Machine identity
- Application settings
- Semantic audio services
- Auxiliary-display state publishing and adapter management
- Maintenance authentication
- Controlled application / host system actions

The Engine exposes shared functionality so interface shells do not need to duplicate core application logic.

---

## Shell

A Shell controls how the user interacts with the Engine.

The current reference shell is:

> **J-29 Terminal Shell**

The Terminal Shell provides:

- Fullscreen terminal presentation
- Animated startup
- Keyboard navigation
- Command input
- Game-library browsing
- System information
- Physical-media interaction
- Media creation
- Contextual control hints
- CRT-style presentation
- Configurable identity
- Semantic audio feedback
- Auxiliary-display status integration
- Authenticated Maintenance Terminal
- Advanced Maintenance Terminal
- Context-aware Settings / Media Tools navigation

The v1.0 architecture is intended to support more than one interface presentation while preserving the same Engine and library state.

The planned second reference shell is a **classic late-1980s / early-1990s desktop-inspired interface**. Its purpose is to prove the shared Engine architecture rather than replace the J-29 Terminal.

---

## Theme

Themes define how a Shell looks and sounds.

Theme-controlled elements may include:

- Colors
- Fonts
- Font sizes
- Scanlines
- CRT effects
- Cursor presentation
- Sounds
- Background assets
- Interface graphics

Themes remain separate from Engine behavior.

This allows the same functional computer system to have multiple visual or audio identities.

---

## Identity

Identity defines the fictional computer presented to the user.

Machine identity is externally configurable and does not require editing Python source code.

Example:

```text
Manufacturer: Callisto Computer Systems
System: J-29 Terminal OS
Model: J-29 Personal Terminal
Unit ID: J29-001
```

The same Engine could instead present another fictional machine:

```text
Manufacturer: Solar Hardware Systems
System: Pigeonaut OS
Model: PX-4
```

---

# Current Features

## Terminal Interface

- Fullscreen retro-terminal presentation
- Callisto Green, Callisto Amber, and Callisto White reference themes
- CRT-style scanlines
- Animated boot sequence
- Blinking block cursor
- Keyboard-driven navigation
- Game Library
- System Information
- Terminal command system
- Dynamic footer / contextual control hints
- Development fullscreen/window controls

---

## Unified Game Library

J-29 presents supported software through one shared library.

Current software sources include:

- Local executable programs
- Steam games
- Automatically discovered ROMs
- Emulator-managed software
- Physical-media targets

The interface does not require the user to think about where a program originally came from once it has entered the J-29 library.

---

## Game Metadata

Library entries can include information such as:

- Title
- Platform
- Year
- Genre
- Developer
- Publisher
- Launch type
- Emulator
- Steam App ID
- Favorite state
- Stable internal game ID

Metadata is used across library browsing, launching, favorites, recent games, and physical media.

---

## Favorites & Recently Played

J-29 maintains persistent favorite and recent-game state between sessions.

Steam games, ROMs, local software, and other supported launch types participate in the same shared library experience.

---

# Steam Integration

J-29 can discover installed Steam libraries and titles automatically.

Steam games are added to the same software library used by local software and emulated titles.

Steam titles can then be:

- Browsed
- Favorited
- Added to recent history
- Launched normally
- Represented by physical launch keys
- Included in physical collections

Steam is treated as a launch backend rather than a separate user-facing experience.

---

# ROM & Emulator Support

J-29 can automatically scan configured ROM libraries and organize discovered software by platform.

Supported emulator workflows can use:

- RetroArch
- Configured RetroArch cores
- Standalone emulators
- Platform-specific emulator profiles

A discovered ROM becomes a normal J-29 library entry.

The user does not need to manually navigate emulator directories during normal operation.

---

# Physical Media

Physical media is one of J-29's core systems.

Supported mounted media can include devices such as:

- SD cards
- USB storage
- External removable drives
- Other compatible mounted media

J-29 follows one central principle:

> **Physical media represents software. It does not require the software to physically reside on that media.**

A physical object can operate in several ways.

---

## Self-Contained Media

The physical medium contains both:

- J-29 metadata
- The actual software or ROM payload

Example:

```text
SD CARD
│
├── j29-media.ini
└── games/
    └── harvest_moon.sfc
```

---

## Metadata-Only Launch Key

The medium contains only a small metadata descriptor.

The actual game remains installed elsewhere.

Example:

```ini
[J29_MEDIA]
type=GAME
title=HARVEST MOON
platform=SNES
game_id=ROM_SNES_6009C68D2439
```

When the medium is inserted, J-29 resolves the `game_id` against the installed library and launches the corresponding software.

This means a tiny removable device can behave like a physical game disk even when the software itself lives on internal storage.

---

## Steam Launch Keys

Physical media can also represent installed Steam software.

```ini
[J29_MEDIA]
type=GAME
title=EXAMPLE GAME
platform=STEAM
game_id=STEAM_123456
```

The physical object becomes the interaction point while Steam remains the launch backend.

---

## Physical Collections

One physical medium can represent multiple programs.

Example:

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
platform=STEAM
game_id=STEAM_1658150
```

When mounted, J-29 presents the collection through its own interface.

Multiple programs can be launched from the same physical object without reinserting it between launches.

---

## Dynamic Media Interface

When recognized J-29 media is mounted:

```text
PHYSICAL MEDIA
```

appears dynamically on the main menu.

J-29 also supports:

- Media already inserted during startup
- Hot removal
- Reinsertion
- Invalid target handling
- Broken library references
- Collection browsing
- Multiple launches from one mounted collection

Removing the media removes its dynamic interface entry.

---

# Physical Media Creator

v0.29 introduced a complete built-in authoring system for J-29 physical media.

Normal users no longer need to manually edit `j29-media.ini` files or look up internal game IDs.

```text
MEDIA TOOLS
    │
    ▼
CREATE MEDIA
    │
    ├── SINGLE GAME
    │
    └── COLLECTION
    │
    ▼
SELECT SOFTWARE
    │
    ▼
SELECT REMOVABLE MEDIA
    │
    ▼
VERIFY
    │
    ▼
WRITE MEDIA
```

Design principle:

> **Users choose the software. J-29 writes the metadata.**

---

## Single-Game Media Creation

Users can:

- Browse existing J-29 library groups
- Select a game
- Preview generated metadata
- Choose a safe removable target
- Write a metadata-only launch key
- Verify the new descriptor through the existing J-29 media reader

Internal game IDs are hidden from the normal creation workflow.

---

## Collection Creation

Users can:

- Select multiple programs
- Move between different library groups without losing selections
- Mix Steam, ROM, and supported local software
- Name the collection
- Reorder collection entries
- Preview the final collection
- Write the collection to removable media
- Verify it immediately using the existing media reader

---

# Media Creator Safety

Writing removable media is intentionally more restrictive than reading it.

Current safety protections include:

- System drive exclusion
- Fixed/internal drive exclusion from creator targets
- Conservative removable-media detection
- Explicit write confirmation
- Existing J-29 metadata protection
- Two-step confirmation for intentional replacement
- Writes limited to J-29's own descriptor file
- Unrelated files preserved
- Post-write verification
- Atomic replacement
- Automatic restoration of the original descriptor if replacement verification fails

Existing J-29 media cannot be replaced accidentally through a single Enter or write action.

Intentional reuse requires a deliberate replacement workflow.

---

# Audio System

J-29 includes an Engine-level semantic audio system.

The Shell requests events such as:

```text
boot
menu_move
select
error
media_detected
access_granted
access_denied
launch
shutdown
```

Themes determine what those events actually sound like.

Architecture principle:

> **The Engine requests semantic audio events; themes define how those events sound.**

---

## Callisto Reference Audio Identity

The current Callisto reference sound set uses:

- Dry mechanical key clicks
- Relay-like interface sounds
- Muted CRT-era electronic tones
- Low-fi industrial texture
- Short acknowledgements
- Minimal melody
- Restrained confirmations and errors

The intent is a retro-futuristic terminal rather than a cartoonish arcade sound set.

The Windows playback implementation maintains a persistent output path so very short interface sounds remain reliable across different audio hardware.

---

# Auxiliary Display Support

v0.30 added an optional Engine-level auxiliary-display system.

The Engine publishes semantic states while adapters decide how those states are presented. This keeps the main application independent of any one display module.

Validated states include:

- BOOTING
- READY
- MEDIA DETECTED
- LAUNCHING
- RUNNING
- REBOOTING
- SHUTDOWN

Auxiliary-display support remains optional. J-29 continues operating normally when no secondary display is present.

The Terminal Settings environment can configure the auxiliary-display enabled state, adapter, and display width. Adapter reload behavior is also available for testing and maintenance.

Architecture principle:

> **The Engine publishes status. Hardware adapters decide how to display it.**

---

# Maintenance Terminal

v0.31 introduced a complete authenticated maintenance environment.

The Maintenance Terminal keeps administrative and recovery functions separate from normal J-29 navigation while preserving an in-universe service experience.

Current capabilities include:

- Password-protected maintenance access
- Salted PBKDF2-HMAC-SHA256 credential storage
- Constant-time password verification
- Controlled Desktop Mode
- Advanced Maintenance Terminal
- Read-only System Diagnostics
- Terminal Settings
- Media Tools
- Reboot Terminal
- True process-level Restart J-29
- Confirmed host Reboot System
- Confirmed host Shutdown System
- Return to normal J-29 operation

The Advanced Terminal provides a controlled Callisto-style service console rather than exposing a raw host command shell.

Supported commands include:

```text
HELP
STATUS
SETTINGS
MEDIA
DESKTOP
REBOOT
RESTART
SYSTEM REBOOT
SYSTEM SHUTDOWN
RETURN
CLEAR
```

J-29 distinguishes three different levels of restart behavior:

- **Reboot Terminal** — reruns the fictional J-29 boot sequence in the current process.
- **Restart J-29** — starts a fresh J-29 process and reloads startup configuration and themes.
- **Reboot System / Shutdown System** — requests the corresponding host operating-system action after explicit confirmation.

Settings that require a fresh process report:

```text
SAVED — RESTART J-29 TO APPLY
```

Media Tools also preserves its navigation context. When opened from regular Settings it returns to Settings; when opened from Maintenance it returns to Maintenance; and when opened from the Advanced Terminal it returns there.

Design principle:

> **Normal operation stays immersive. Maintenance stays available.**

---

# System Information

J-29 can currently read host information including:

- CPU model
- Installed memory
- Host operating system
- System drive
- Total storage capacity
- Available storage space

The fictional interface can therefore present information from the real underlying computer.

---

# Configuration

Public configuration templates are stored separately from local user configuration.

Example templates:

```text
config/identity.example.ini
config/settings.example.ini
config/games.example.ini
```

Local configuration:

```text
config/identity.ini
config/settings.ini
config/games.ini
```

Local configuration files are ignored by Git so personal machine settings are not accidentally published.

---

## Configurable Identity

Identity values may include:

- Manufacturer
- System / OS name
- Model
- Version
- Unit ID
- Owner
- Location

Identity information can be used by:

- Boot branding
- Window titles
- Terminal titles
- System Information
- Other Shell presentation

---

## Application Settings

Configurable settings include or are being expanded to include:

- Startup fullscreen behavior
- Boot-sequence enable/disable
- Footer behavior
- Audio enable/disable
- Master volume
- Development controls
- Interface preferences
- Host-integration behavior
- Theme selection
- Auxiliary-display enabled state
- Auxiliary-display adapter
- Auxiliary-display width

---

# Guided First-Launch Setup — Planned v0.32

v0.32 is dedicated to making a fresh installation approachable without removing control from experienced users.

The planned first-launch screen offers two paths:

```text
WELCOME TO THE INTERFACE ENGINE

[ BEGINNER / GUIDED SETUP ]
[ POWER USER / MANUAL SETUP ]
```

The guided path is planned to cover:

- Basic application configuration
- Machine identity
- Game-library locations
- Steam discovery
- ROM-library locations
- Emulator configuration
- Theme / appearance basics
- Audio settings
- Physical-media support
- Windows host integration
- Final configuration review
- Physical-media verification

The Power User path can skip the wizard, and the guided setup will remain available later through Settings.

Design principle:

> **Beginner users should be guided. Power users should never be trapped by the wizard.**

---

# Windows Integration

Windows is the initial supported release target.

For the intended physical-media experience, Guided First-Launch Setup will explain and help configure host settings such as:

- Disabling AutoPlay for removable media
- Disabling Windows Device Connect sounds
- Disabling Windows Device Disconnect sounds
- Keeping normal removable-drive mounting enabled
- Verifying physical-media behavior afterward

Host changes should be explained before they are applied.

The goal is to keep Windows from visually or audibly interrupting the fictional-computer experience.

---

# Cross-Platform Direction

The project is currently Windows-first, but Engine components are being written to remain portable where practical.

Target direction:

1. **Windows**
2. **macOS**
3. **Linux**
4. Potential dedicated Debian-based appliance environment later

Platform-specific code should remain isolated where possible so the shared Engine does not become unnecessarily tied to Windows.

---

# Reference System

The original reference configuration is:

**Manufacturer:** Callisto Computer Systems  
**System:** J-29 Terminal OS  
**Model:** J-29 Personal Terminal

The physical J-29 project combines modern computer hardware with a fictional retro-computer presentation.

The Interface Engine itself is **not tied to the J-29 enclosure or a specific computer**.

The Callisto J-29 is the reference implementation used to design and validate the platform.

---

# Reference Hardware / Case Design

The reference J-29 build uses the **Raspberry Pi Retro Computer** enclosure originally designed by **lowbudgettech**.

**Original designer:** lowbudgettech  
**Original project:** Raspberry Pi Retro Computer  
**Thingiverse:** https://www.thingiverse.com/thing:3478048

The enclosure is the work of its original creator and is not part of the J-29 Interface Engine software.

J-29 can also be used with:

- Custom computer cases
- Repurposed PCs
- Mini PCs
- Cyberdecks
- Laptops
- Single-board computers
- Purpose-built retro systems
- Other custom hardware projects

---

# Development Structure

The project is organized around a small application entry point with Engine, Shell, Theme, and configuration layers.

```text
J-29-Interface-Engine/
│
├── main.py
├── j29.py
│
├── engine/
│   ├── core.py
│   ├── config.py
│   ├── games.py
│   ├── launcher.py
│   ├── system_info.py
│   ├── media.py
│   ├── media_creator.py
│   ├── audio.py
│   ├── auxiliary_display.py
│   ├── maintenance_auth.py
│   └── system_actions.py
│
├── shells/
│   └── terminal/
│
├── themes/
│
├── config/
│   ├── identity.example.ini
│   ├── settings.example.ini
│   └── games.example.ini
│
├── README.md
├── ROADMAP.md
├── CHANGELOG.md
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── PROJECT_HISTORY.md
└── LICENSE
```

The architecture is being built incrementally rather than through one large rewrite.

Stable functionality should remain intact while new systems are introduced.

---

# Current Roadmap

| Version | Milestone | Status |
|---|---|---|
| v0.20 | Filesystem-Style Library Browser | ✅ Complete |
| v0.21 | Game Metadata | ✅ Complete |
| v0.22 | Favorites | ✅ Complete |
| v0.23 | Recent Games | ✅ Complete |
| v0.24 | Steam Support | ✅ Complete |
| v0.25 | Emulator Support | ✅ Complete |
| v0.25.1 | Long-List Scrolling Polish | ✅ Complete |
| v0.26 | Physical Media System | ✅ Complete |
| v0.26.1 | Universal Launch Transition | ✅ Complete |
| v0.27 | Media Metadata & Collections | ✅ Complete |
| v0.28.1 | Custom Audio / Callisto Audio Identity | ✅ Complete |
| v0.29.0 | Physical Media Creator | ✅ Complete |
| v0.30 | OLED / Auxiliary Display Support | ✅ Complete |
| v0.31 | Maintenance Terminal | ✅ Complete |
| v0.32 | Guided First-Launch Setup | ⏳ Next |
| v0.33 | Appliance Mode | ⏳ Planned |
| v0.34 | Boot Maintenance Console | ⏳ Planned |
| v0.35 | Deployment Build | ⏳ Planned |
| v0.36–v0.99 | Stabilization | ⏳ Planned |
| v1.0 | Initial Public Release | 🎯 Target |

See [`ROADMAP.md`](ROADMAP.md) for the detailed development plan.

---

# Road to v1.0

The initial public release is intended to deliver a complete dedicated-computer experience including:

- J-29 Terminal Shell
- Modular Interface Engine
- Configurable machine identity
- Theme support
- Unified game library
- Filesystem-style browsing
- Terminal commands
- Favorites
- Recently played software
- Game metadata
- Steam integration
- Emulator / ROM support
- Physical media
- Physical Media Creator
- Custom audio
- Auxiliary-display support
- Guided First-Launch Setup
- Maintenance Terminal
- Appliance Mode
- Boot Maintenance Console
- Packaged deployment
- Final cross-hardware regression testing

The v1.0 architecture must also preserve shell-independent shared systems so the project is proven as an Interface Engine rather than a single terminal frontend.

---

# Future Shells

The J-29 Terminal remains the official reference Shell.

The modular architecture is designed so other interfaces can use the same underlying Engine for:

- Games
- Metadata
- Favorites
- Recent history
- Steam
- Emulators
- Physical media
- Configuration
- System information
- Shared services

For v1.0, a second distinct interface is planned as an architecture demonstration. The reference concept is a **classic late-1980s / early-1990s desktop-inspired shell** sharing the same library and Engine state as the J-29 Terminal.

Longer-term shell possibilities include:

- Retro console interfaces
- Linux-style terminals
- Other fictional computers
- Desktop-inspired environments
- Community-created shells

A user should not need separate game libraries for every interface.

---

# Shell Compatibility

Future shell packages are expected to declare compatibility with the Engine API.

Concept:

```text
Shell Name: J-29 Terminal
Shell Version: 1.0
Engine API: 1
```

The Engine can then verify compatibility before loading a Shell.

This allows shell development to grow without silently breaking existing installations.

---

# Open Source

J-29 Interface Engine is released under the **MIT License**.

You are free to use, modify, distribute, and build upon the software under the terms of that license.

Community participation is encouraged.

Potential contributions include:

- Custom shells
- Themes
- Hardware builds
- Bug fixes
- Documentation
- Platform compatibility
- Emulator profiles
- Configuration examples
- Accessibility improvements
- Feature ideas

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for more information.

---

# Development Philosophy

J-29 development follows one rule:

> **Big vision. Small versions. Stable checkpoints. No chaos.**

Each major milestone is:

1. Built
2. Tested
3. Validated
4. Documented
5. Committed
6. Preserved as a stable checkpoint

Development then moves forward from that known-good state.

The goal is not to race toward version 1.0.

The goal is to arrive at version 1.0 with a system that is understandable, testable, recoverable, and pleasant to use.

---

# Project Vision

J-29 started with a fictional retro computer.

The larger idea is a platform where modern software can feel like it belongs to a dedicated machine again.

A game does not have to feel like a file.

A removable drive does not have to feel like storage.

A launcher does not have to feel like a launcher.

The interface can become part of the machine.

The physical object can become part of the interaction.

And modern hardware can disappear behind the experience.

> **Modern hardware. Retro experience.**

---

# Disclaimer

J-29 Interface Engine is experimental software under active development.

Configuration formats, internal APIs, Shell behavior, platform support, and feature organization may change before version 1.0.

The **Callisto Computer Systems**, **J-29 Terminal**, and related fictional systems are used as the reference environment for development and demonstration of the Interface Engine.

