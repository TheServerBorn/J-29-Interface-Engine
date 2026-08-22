# Contributing to J29 Terminal Engine

Thank you for your interest in the J29 Terminal Engine.

J29 is being developed as an open-source retro-computing frontend platform built around games, physical media, customizable fictional computer systems, and community creativity.

The goal is not only to build the original J-29 Terminal, but to create an engine that other people can adapt to their own projects.

Contributions are welcome, but never required.

If you build something cool with J29, we would love to see it.

---

# Ways to Contribute

There are several ways to participate in the project.

You can:

- Report bugs
- Suggest features
- Improve documentation
- Submit code improvements
- Create themes
- Create shells
- Share hardware builds
- Improve accessibility
- Test development releases
- Suggest compatibility improvements
- Share ideas for physical media support
- Help improve installation or configuration

You do not need to be a programmer to contribute.

---

# Bug Reports

If you encounter a problem, please open a GitHub Issue.

When possible, include:

- J29 Engine version
- Shell version
- Windows version
- Hardware information
- What you were trying to do
- What you expected to happen
- What actually happened
- Any error messages
- Steps that reproduce the issue

Screenshots are helpful when relevant.

Please remove personal information before posting logs or screenshots publicly.

---

# Feature Requests

Feature ideas are welcome.

Before submitting a new feature request, please consider the current project scope and roadmap.

The primary development goal is currently:

> Complete a stable J29 Terminal Engine v1.0.

Large new ideas may be considered for post-v1.0 development rather than added immediately.

When suggesting a feature, explain:

- What problem it solves
- How you imagine it working
- Why it fits the J29 project
- Whether it affects the Engine, Shell, Theme, or hardware integration

---

# Sharing Your Build

One of the goals of J29 is to encourage people to create their own fictional computers and retro gaming systems.

If you build a machine using J29, please consider sharing it with the community.

Examples include:

- Custom computer enclosures
- Cyberdecks
- Arcade systems
- Retro terminal builds
- Repurposed laptops
- Mini PCs
- Raspberry Pi-style projects
- Custom physical game libraries

Photos, videos, hardware notes, and configuration ideas are encouraged.

---

# Themes

Themes change the appearance and sound of an existing Shell.

A Theme may eventually include:

- Colors
- Fonts
- Font sizes
- Scanlines
- CRT effects
- Sounds
- Background assets
- Cursor appearance
- Interface graphics

Themes should not modify the core Engine.

Community-created themes are encouraged.

---

# Shells

Shells provide alternate interfaces for the J29 Engine.

The original reference Shell is:

**J-29 Terminal Shell**

Future community shells may provide completely different experiences.

Examples might include:

- Retro console interfaces
- Text-only computer systems
- Graphical desktop environments
- 1980s-inspired computer interfaces
- 1990s-inspired desktop interfaces
- Original fictional computer systems

Shells should communicate with the J29 Engine through documented interfaces rather than duplicating core functionality whenever possible.

Future Shell packages will include compatibility information describing which Engine API versions they support.

---

# Machine Identity

J29 is designed so users can create their own fictional computer identity.

A custom system may define:

- Manufacturer
- Operating environment name
- Model
- Unit ID
- Owner
- Location
- Theme
- Shell

The Callisto J-29 is the official reference configuration, but users are encouraged to create completely original systems.

---

# Physical Media

J29 physical media support is intended to be format-agnostic.

Community experiments may involve:

- Floppy disks
- SD cards
- microSD cards
- USB flash drives
- External SSDs
- External hard drives
- Other removable storage

Please share successful hardware configurations and compatibility findings.

---

# Lore and Story Content

The J29 Engine may eventually support optional fictional archive and lore systems.

Please avoid posting spoilers for official lore content in unrelated Issues or Discussions.

Community-created fictional universes and lore packs may be supported in the future.

Official unreleased story content should remain private until intentionally published.

---

# Pull Requests

Code contributions should normally be submitted through GitHub Pull Requests.

Before submitting a large change:

1. Check the roadmap.
2. Check existing Issues.
3. Consider opening an Issue or Discussion first.
4. Explain what the change does and why it is useful.

Pull Requests should ideally:

- Focus on one purpose
- Avoid unrelated changes
- Preserve existing functionality
- Include testing notes
- Update documentation when necessary
- Follow the Engine / Shell / Theme / Identity architecture

---

# Development Philosophy

J29 development follows:

> Big vision. Small versions. Stable checkpoints.

Changes should be implemented incrementally whenever possible.

A working system is more valuable than a large unfinished feature.

---

# Engine / Shell Separation

Contributors should preserve the architectural separation between:

## Engine

Shared functionality such as:

- Game launching
- Library management
- Physical media
- Metadata
- Configuration
- System services

## Shell

User interface and interaction.

## Theme

Visual and audio presentation.

## Identity

User-configurable fictional computer branding.

Features that can be implemented generically should not be unnecessarily tied to one Shell or Theme.

---

# Compatibility

Future Shell and Theme systems will include version metadata.

Do not assume every Shell supports every Engine version.

Compatibility information should be clearly documented.

---

# Security

Never commit:

- Passwords
- API keys
- Authentication tokens
- Private account information
- Personal file paths containing sensitive information
- Unreleased private lore
- Other secrets

User-specific configuration should remain outside the public repository when appropriate.

---

# Community Conduct

Be respectful.

People participating in J29 may have very different levels of programming, electronics, fabrication, or computer experience.

Constructive feedback is encouraged.

Gatekeeping is not.

The goal is to help people build interesting things.

---

# Community Philosophy

J29 exists because building computers should be fun.

Take the Engine.

Build your own machine.

Create your own Shell.

Design your own Theme.

Put it inside something weird.

And if you make something awesome, show us.