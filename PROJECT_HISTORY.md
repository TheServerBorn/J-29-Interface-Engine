# J29 Terminal Engine — Project History

## Origin

J29 began as a personal retro-computing project built around the Callisto J-29 computer enclosure.

The original goal was simple:

Use modern PC hardware inside a retro-styled enclosure and create a fullscreen terminal interface that made the machine feel like its own fictional computer rather than a Windows PC running a launcher.

The reference system became:

- Manufacturer: Callisto Computer Systems
- System: J-29 Terminal OS
- Model: J-29 Personal Terminal

---

# The First Prototype

The first functional prototype was written in Python using Tkinter.

Early versions established the basic concept:

- Black terminal display
- Green monospace text
- Keyboard navigation
- Game Library
- Animated startup sequence
- External application launching
- Real system information
- Fullscreen operation
- CRT scanlines
- Canvas-based rendering

Development progressed rapidly through small numbered checkpoints.

By v0.13, the project had become a stable proof of concept capable of launching software and presenting real modern hardware as a fictional retro computer.

---

# Why the Project Changed

Originally, J29 was designed specifically for one machine.

As development continued, several ideas emerged:

- Configurable manufacturers
- Custom operating-system names
- Themes
- Physical game media
- Steam support
- Emulator support
- Auxiliary displays
- Maintenance environments
- Hidden filesystem content
- Community-created interfaces

At that point, keeping everything inside one large `j29.py` file would eventually make the project difficult to maintain.

So the project changed direction early rather than waiting until the architecture became difficult to untangle.

---

# The Architecture Pivot

Beginning with v0.14, J29 started transitioning from a purpose-built application into a reusable retro-computing frontend engine.

The new architecture separates four concepts:

> Engine = what the machine can do  
> Shell = how the user interacts with it  
> Theme = how the shell looks and sounds  
> Identity = whose fictional machine it is

The original J-29 Terminal remains the reference Shell and the primary target for v1.0.

The architecture change does not abandon the original project.

It exists to make the original project easier to build while also allowing others to create their own systems later.

---

# Physical Media

A major part of the project vision is restoring physical interaction to digital game libraries.

Instead of requiring games to physically reside on removable media, J29 can eventually treat disks and storage devices as physical representations or keys for installed software.

Examples may include:

- Floppy disks
- SD cards
- USB drives
- External SSDs
- External hard drives

The software identifies what the media represents rather than depending on one specific physical format.

---

# Open Source Direction

The decision was made to develop J29 publicly on GitHub.

The project is intended to allow others to:

- Build their own retro computers
- Create Themes
- Create alternate Shells
- Improve the Engine
- Share hardware builds
- Suggest features
- Report bugs
- Adapt the software to completely different fictional machines

Contributions are encouraged but are not intended to be mandatory.

---

# Development Philosophy

J29 uses small development milestones instead of large unstable rewrites.

The guiding principle is:

> **Big vision. Small versions. Stable checkpoints. No chaos.**

Working versions are preserved before major changes are attempted.

The v0.13 prototype serves as the stable reference before the v0.14 architecture refactor.

---

# Current Chapter

The immediate objective is no longer to expand the feature list.

The v1.0 scope has been frozen.

Development is now focused on completing the roadmap one milestone at a time, beginning with the modular Engine/Shell architecture.

The next chapter starts with:

**v0.14 — Core Engine Separation**