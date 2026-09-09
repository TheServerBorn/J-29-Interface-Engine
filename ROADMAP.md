# J-29 Interface Engine — Development Roadmap

## Project Goal

J-29 Interface Engine is a customizable retro-computing frontend designed to make modern hardware feel like a fictional computer system.

The initial v1.0 release will focus on the original J-29 vision while preserving the modular Engine + Shell architecture that allows the project to grow beyond a single interface.

Core goals include:

- Retro terminal interface
- Unified game launching
- Physical-media interaction
- Custom machine identity
- Configurable themes
- Terminal commands
- Guided first-launch setup
- Maintenance and recovery environments
- Stable appliance-style operation
- Packaged deployment
- A shared Engine architecture capable of supporting alternate shells

Development follows one rule:

> **Big vision. Small versions. Stable checkpoints. No chaos.**

---

# Current Stable Build

## v0.31 — Maintenance Terminal

### Status

**COMPLETE — FULL REGRESSION PASSED**

### Goal

Replace temporary development shortcuts with a complete in-universe maintenance environment while keeping administrative access separate from normal J-29 operation.

### Completed

- Authenticated Maintenance Terminal
- F12 maintenance entry
- Salted PBKDF2-HMAC-SHA256 password storage
- Constant-time password verification
- Masked password entry
- Safe ACCESS GRANTED / ACCESS DENIED behavior
- Password setup utility
- Controlled Desktop Mode
- Advanced Maintenance Terminal
- Read-only System Diagnostics
- Editable Terminal Settings
- Maintenance access to Media Tools
- Reboot Terminal
- True process-level Restart J-29
- Confirmed host Reboot System
- Confirmed host Shutdown System
- Context-aware return navigation
- Main-menu and Settings consolidation
- Callisto Green, Callisto Amber, and Callisto White theme validation

### Advanced Terminal

The authenticated Advanced Terminal is a controlled J-29 service console rather than a raw host shell.

Supported commands include:

- `HELP`
- `STATUS`
- `SETTINGS`
- `MEDIA`
- `DESKTOP`
- `REBOOT`
- `RESTART`
- `SYSTEM REBOOT`
- `SYSTEM SHUTDOWN`
- `RETURN` / `EXIT`
- `CLEAR`

### Restart Semantics

- **REBOOT TERMINAL** reruns the fictional J-29 boot sequence inside the current process.
- **RESTART J-29** relaunches J-29 as a fresh process so startup-loaded configuration and themes are reloaded.
- **REBOOT SYSTEM** and **SHUTDOWN SYSTEM** request host operating-system actions after explicit confirmation.

### Navigation

Media Tools returns to the context that opened it:

- Settings → Media Tools → Settings
- Maintenance Terminal → Media Tools → Maintenance Terminal
- Advanced Terminal → Media → Advanced Terminal

### Validation

Full regression passed across normal J-29 operation and the Maintenance Terminal, including the final Media Tools context-return correction.

### Design Principle

> **Normal operation stays immersive. Maintenance stays available.**

---

# Previous Completed Milestone

## v0.32 — Guided First-Launch Setup

### Status

**NEXT MILESTONE**

### Goal

Give new users a clear first-run experience that can configure J-29 without requiring them to understand internal configuration files or host-integration requirements beforehand.

The first launch should begin with a Welcome screen and offer two paths:

```text
WELCOME TO THE INTERFACE ENGINE

[ BEGINNER / GUIDED SETUP ]
[ POWER USER / MANUAL SETUP ]
```

### Beginner / Guided Setup

The guided path should walk the user through the major configuration needed for a working installation.

Planned steps include:

- Welcome / introduction
- Basic application configuration
- Machine identity
- Game-library locations
- Steam discovery and sign-in/install guidance where needed
- GOG / Epic and other launcher integration guidance where supported
- ROM-library locations
- Emulator configuration and optional emulator acquisition guidance
- Theme / appearance basics
- Audio enable/disable
- Master volume
- Physical-media support
- Windows host-integration requirements
- Final configuration review
- Physical-media verification

The wizard should explain what it is changing and why.

### Power User / Manual Setup

Experienced users should be able to bypass the guided flow and proceed directly to normal operation or manual configuration.

Skipping the wizard must not permanently disable it.

The setup flow should remain available later through Settings.

### Windows Integration

On Windows, Guided Setup must explain and help configure the host so Windows does not interrupt the intended J-29 physical-media experience.

Required guidance includes:

- Disable AutoPlay for removable drives
- Disable Windows Device Connect sound
- Disable Windows Device Disconnect sound
- Keep normal removable-drive mounting enabled
- Explain host changes before applying them
- Provide a physical-media verification step afterward

### Final Verification

Before guided setup is considered complete, the user should be able to verify the systems available on the host, including:

- Library discovery
- Steam detection
- Emulator configuration
- Audio
- Physical media
- Host-integration behavior

Failures should return the user to the relevant setup step instead of leaving them at an unusable installation.

### Design Principle

> **Beginner users should be guided. Power users should never be trapped by the wizard.**

---

# v0.33 — Appliance Mode

### Status

**PLANNED**

### Goal

Make J-29 behave like a dedicated computer rather than a visible Windows application.

### Planned Work

- Windows auto-login
- Automatic Engine startup
- Hide the normal desktop during operation
- Prevent distracting notifications
- Reliable return from games
- Safe Maintenance Terminal access
- Startup recovery
- Controlled shutdown
- Controlled restart
- Reliable relaunch after external programs close
- Preserve a recoverable path back to the host operating system

### Design Principle

> **The host OS should support the experience, not become the experience.**

---

# v0.34 — Boot Maintenance Console

### Goal

Provide recovery and maintenance access during startup before the normal Shell fully loads.

Example startup prompt:

```text
PRESS F12 FOR MAINTENANCE
```

Possible console:

```text
CALLISTO MAINTENANCE CONSOLE

1. EXIT TO WINDOWS
2. SYSTEM DIAGNOSTICS
3. TERMINAL SETTINGS
4. MEDIA SETTINGS
5. RESTART TERMINAL
```

### Planned Work

- Pre-Shell maintenance entry point
- Exit to host operating system
- Basic diagnostics
- Configuration recovery
- Media configuration access
- Restart J-29
- Safe behavior when the normal Shell cannot load
- Safe behavior when configuration files are invalid or missing

### Design Principle

> **A broken Shell must not mean a trapped machine.**

---

# v0.35 — Deployment Build

### Goal

Package J-29 so a target computer does not require Python development tools or a development environment.

Planned output:

```text
J29Terminal.exe
```

or equivalent packaged release.

### Development System

- Python
- Source code
- Development environment
- Testing tools

### Target System

- Packaged J-29 application
- Configuration
- Themes and assets
- Required runtime components
- Game / emulator configuration

### Planned Work

- Create repeatable packaged builds
- Remove dependency on a local Python development environment
- Preserve external configuration
- Preserve themes and assets
- Ensure Guided First-Launch Setup works on a clean deployment
- Ensure maintenance/recovery paths survive packaging
- Validate application startup without development tools installed

---

# v0.36–v0.99 — Stabilization

After the major systems are complete, development will focus on reliability, compatibility, usability, and release readiness rather than major feature expansion.

### Validation Areas

Testing will include:

- Fresh installation
- First-launch wizard
- Beginner / Guided Setup path
- Power User / Manual Setup path
- Windows integration
- Missing games
- Missing emulators
- Invalid media
- Removed media
- Steam unavailable
- Unsupported hardware
- Missing configuration
- Invalid configuration
- Display-resolution differences
- Auxiliary-display failure
- Application crashes
- Maintenance recovery
- Boot maintenance recovery
- Returning from games
- Appliance-mode startup
- Clean shutdown
- Clean restart
- Audio playback across different Windows endpoints
- Physical-media detection across supported devices
- Physical-media creation and replacement
- Cross-platform regression where supported

### Scope Rule

No major feature additions should occur during final stabilization unless required for:

- Reliability
- Architecture
- Security
- Accessibility
- Compatibility
- Completion of an existing v1.0 requirement

The priority during this phase is:

> **Fix what exists. Validate what exists. Ship what exists.**

---

# v1.0 — Initial Public Release

## Goal

Version 1.0 will deliver the original J-29 experience on top of a stable modular Interface Engine.

The Callisto J-29 remains the official reference implementation.

### v1.0 Reference Experience

The release target includes:

- J-29 Terminal Shell
- Modular Engine + Shell architecture
- Configurable machine identity
- Theme support
- Game Library
- Filesystem-style navigation
- Terminal commands
- Favorites
- Recently played software
- Game metadata
- Steam launching
- Emulator / ROM launching
- Physical-media support
- Metadata-only launch keys
- Self-contained media
- Physical-media collections
- Built-in Physical Media Creator
- Configurable custom audio
- OLED / auxiliary display support
- Guided First-Launch Setup
- Beginner / Guided Setup path
- Power User / Manual Setup path
- Guided Windows integration
- Maintenance Terminal
- Appliance Mode
- Boot Maintenance Console
- Packaged deployment
- Final regression and usability polish

### Interface Engine Requirement

The project is intended to remain an Interface Engine rather than a single hard-coded terminal application.

The v1.0 architecture must preserve:

- Shared library state
- Shared metadata
- Shared favorites
- Shared recent history
- Shared Steam integration
- Shared emulator integration
- Shared physical-media systems
- Shared configuration
- Shared Engine services
- Shell-independent core behavior

The J-29 Terminal is the reference Shell.

A second distinct interface shell is part of the broader v1.0 Engine demonstration requirement so the architecture is proven through more than one presentation layer. The planned reference concept is a classic late-1980s / early-1990s desktop-inspired shell using the same underlying Engine and library state.

### Release Principle

> **One Engine. Multiple experiences. Stable foundation.**

---

# Post-v1.0 Development

Version 1.0 marks a stable platform, not the end of development.

Future work should expand the platform through optional capabilities, additional shells, themes, integrations, and content rather than unnecessarily replacing the stable core.

---

# v1.1 — Archive & Lore Expansion

### Goal

Introduce optional environmental storytelling inside the fictional computer.

The base system may contain:

- Hidden directories
- Text files
- Maintenance logs
- Incident reports
- Personnel records
- Undocumented commands
- Clues leading to deeper directories

Example discovery:

```text
> TYPE INCIDENT_04.TXT
```

A document may reveal:

```text
ARCHIVE ACCESS CODE: JANUS
```

The user may then discover:

```text
> JANUS
```

which exposes an undocumented archive.

The amount of future lore development will depend on project direction and community interest.

---

# Expandable Lore Media

Additional story content may be distributed through physical media.

Example:

```text
MEDIA DETECTED

CALLISTO ARCHIVE MEDIA

ACCESS FILES?

[Y/N]
```

Archive media may contain optional story content without permanently installing it into the base system.

---

# Future Shell Packs

The J-29 Interface Engine is designed to support additional interface shells that use the same core Engine.

Possible future shells include:

- Retro console interface
- Linux-style terminal
- 1980s fictional computer
- 1990s desktop interface
- Early-2000s desktop-inspired interface
- Community-created shells

Compatible shell packs should be addable without replacing the shared Engine or rebuilding the user's software library.

New users may eventually be able to download preconfigured bundles containing the Engine and a preferred shell.

---

# Shell Compatibility

Future shells should contain a manifest defining compatibility with the Engine API.

Concept example:

```text
Shell Name: J-29 Terminal
Shell Version: 1.0
Engine API: 1
```

The Engine should verify compatibility before loading a Shell.

This prevents incompatible shells from silently breaking an installation.

---

# Community Vision

J-29 is intended to eventually support a community of builders.

Users may be encouraged to share:

- Custom shells
- Themes
- Hardware builds
- Configuration ideas
- Emulator profiles
- Feature suggestions
- Code improvements
- Compatibility fixes
- Documentation

Community participation is encouraged, not required.

---

# Open Source

J-29 Interface Engine is open-source software released under the **MIT License**.

Users are free to use, modify, distribute, and build upon the software under the terms of that license.

The project should remain approachable to:

- Users who only want the reference J-29 experience
- Power users who want deeper configuration
- Hardware builders
- Theme creators
- Shell developers
- Contributors improving the Engine itself

---

# Development Workflow

Development is performed in stable checkpoints.

The preferred milestone cycle is:

```text
IMPLEMENT A SET OF CHANGES
        │
        ▼
      COMMIT
        │
        ▼
IMPLEMENT NEXT SET OF CHANGES
        │
        ▼
  FINAL MILESTONE COMMIT
        │
        ▼
 CREATE RELEASE / TAG
        │
        ▼
   MERGE MILESTONE
        │
        ▼
 CREATE NEXT BRANCH
        │
        ▼
      REPEAT
```

The goal is to keep every major milestone recoverable and understandable.

---

# Scope Freeze

The v1.0 roadmap is feature-frozen.

New ideas should generally be recorded for post-v1.0 development instead of being inserted into the initial release unless they are required for:

- Reliability
- Architecture
- Security
- Accessibility
- Compatibility
- Completion of an already-approved v1.0 feature

The priority is now:

> **Build the roadmap. Test the roadmap. Finish the roadmap. Ship v1.0.**
