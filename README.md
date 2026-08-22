# J29 Terminal Engine

A customizable retro-computing frontend engine for games, physical media, and fictional computer interfaces.

## Project Status

**Current Development Version:** v0.13

J-29 began as a custom retro terminal launcher for the Callisto J-29 computer project. During early development, the project expanded into a more general frontend engine capable of supporting customizable machine identities, themes, physical media, game libraries, and eventually alternate user-interface shells.

The original J-29 Terminal OS remains the reference implementation and the target experience for version 1.0.

## Current Features

- Fullscreen retro terminal interface
- CRT-style scanlines
- Keyboard-driven navigation
- Animated startup sequence
- Real CPU, memory, and storage information
- Configurable game library
- External application launching
- System information screen
- Blinking terminal cursor
- Development maintenance controls

## Project Direction

Beginning with v0.14, J29 is transitioning from a single monolithic application into a modular architecture.

The project will separate:

- **Engine** — game launching, media detection, metadata, configuration, system services
- **Shell** — the user interface and interaction model
- **Theme** — colors, fonts, sounds, visual effects, and presentation
- **Identity** — manufacturer, system name, model, unit ID, and other fictional-computer branding

This will allow the same core engine to eventually support multiple retro-computing interfaces without duplicating the underlying functionality.

## Reference System

The original reference implementation is:

**Manufacturer:** Callisto Computer Systems  
**System:** J-29 Terminal OS  
**Hardware Concept:** Modern PC hardware presented as a fictional retro computer

Users will eventually be able to configure their own system identities without modifying the source code.

## Reference Hardware / Case Design

The reference J29 build uses the **Raspberry Pi Retro Computer** enclosure designed by **lowbudgettech**.

**Original designer:** lowbudgettech  
**Original project:** Raspberry Pi Retro Computer  
**Thingiverse:** https://www.thingiverse.com/thing:3478048

The enclosure design is the work of its original creator and is not part of the J29 Terminal Engine software.

J29 Terminal Engine does not require this specific enclosure. The software can be used with custom cases, repurposed computers, cyberdecks, mini PCs, and other hardware.

## Long-Term Goals

J29 is planned to support:

- Game libraries
- Steam games
- Retro emulators
- Game metadata
- Favorites
- Recently played games
- Physical game media
- Floppy disks
- SD cards
- USB storage
- External HDDs and SSDs
- Terminal commands
- Filesystem-style navigation
- Custom themes
- Custom sounds
- OLED display integration
- Maintenance mode
- First-run system configuration
- Community-created shells and themes

## Physical Media

One of the primary goals of J29 is to bring a sense of physical ownership back to digital games.

Supported physical media will eventually be format-agnostic. A game, archive, or other J29 media package may be represented by:

- Floppy disk
- SD or microSD card
- USB flash drive
- External SSD
- External HDD
- Other removable storage

The J29 engine will identify what the media represents rather than depending on a specific physical format.

Example interaction:

    MEDIA DETECTED

    DOOM

    LOAD GAME?

    [Y/N]

## Open Source

J29 is being developed as an open-source project.

Community members will eventually be encouraged to create and share:

- Themes
- Shells
- Hardware builds
- Configuration profiles
- Improvements
- Feature ideas

## Development Philosophy

Big vision. Small versions. Stable checkpoints.

Each development milestone is implemented, tested, documented, and preserved before moving on to the next.

## License

A permissive open-source license will be selected before the first public release.

## Documentation

Additional installation, architecture, development, configuration, and contribution documentation will be added as development continues.

---

**J29 Terminal Engine is currently experimental software under active development.**