# Early Development Archive

This directory preserves the recovered original source snapshots from the first monolithic J-29 Terminal OS prototype, before the v0.14 modular architecture pivot.

These files are **historical development artifacts**. They are preserved as found and are not the current application source. For current development, use the live `engine/`, `shells/`, configuration, and entry-point files in the repository root.

## Recovered Sequence

The archive contains the original Python snapshots from **v0.1 through v0.13**, plus the `games.ini` file used by the configurable game-library prototype.

The recovered sources show the progression documented in `CHANGELOG.md`:

- v0.1 — initial Tkinter terminal prototype
- v0.2 — keyboard/menu navigation and System Info screen
- v0.3 — animated startup sequence
- v0.4 — external application launching
- v0.5 — Game Library navigation
- v0.6 — external `games.ini` configuration
- v0.7 / v0.7.1 / v0.8 — real host system information work
- v0.9 — fullscreen terminal/maintenance development shortcuts
- v0.10 — display/font layout tuning
- v0.11 — CRT scanlines
- v0.12 — Canvas rendering migration
- v0.13 — stable monolithic proof-of-concept checkpoint

## Preservation Notes

The recovered files are intentionally not edited to make their internal displayed version strings match their filenames. Several development snapshots were saved under a new checkpoint filename before every visible version string had been updated.

That mismatch is part of the authentic development history.

Known examples:

- `j29_v0.3.py` still displays `v0.2`
- `j29_v0.6.py` still displays `v0.5`
- `j29_v0.7.1.py` displays `v0.7`
- `j29_v0.8.py` still displays `v0.7`
- `j29_v0.10.py` still displays `v0.9`

A recovered file named `j29(1).py` was also found. It is byte-for-byte identical to `j29_v0.13.py` and is therefore not stored as a second archive copy.

All recovered Python files passed a syntax-compilation check during the recovery audit. No modernization or cross-platform refactoring was applied to these historical snapshots.

## Integrity

SHA-256 hashes below identify the exact recovered files committed to this archive.

| File | SHA-256 |
|---|---|
| `j29_v0.1.py` | `6bfd26c63c87d4573e9fa1385344b838e25e82a67f2a15a286a05c9c29d212f1` |
| `j29_v0.2.py` | `cbab1c63ea288d2295659c6f57e343a94a3ecc6d20d34f10165d4e37bb6952e6` |
| `j29_v0.3.py` | `c1b17fa77941f32b957a1ab973e2116a39dbd1e87ed0fbb4da62c52be4717f7e` |
| `j29_v0.4.py` | `8ccdbcaaa693788ef890649eee8bb6b3773abf1e622cfada313522615b6233ad` |
| `j29_v0.5.py` | `9e35645a5e97064110d895b91288f8eb5ba63dbae6e65024af4c932a3e0a2cc2` |
| `j29_v0.6.py` | `2ab0fece4411b33968f21c58fe0ed2c66747e9d55a83a565ed079341dde778df` |
| `j29_v0.7.1.py` | `133762ed5e5bec2fd071bf1d608577874f9a0b6be20792a3bdab3913b2e4aaf9` |
| `j29_v0.8.py` | `011b71fff3e2f864457de5f4fee6b4617a323b4911caa03eec3cc2a0620999c5` |
| `j29_v0.9.py` | `0bc968e91990b05ed06b6239675ea78ca21dd23b8d5348b5a8d6979229910f95` |
| `j29_v0.10.py` | `0cfb6be6527a741ceaf8d2abe36f09502cff466e3c27210f945985bca41443cd` |
| `j29_v0.11.py` | `aa899793471dd9ba5f64e6100512b86d2b54863dbffab3f37c974cad1123d4f0` |
| `j29_v0.12.py` | `e38ce5a2c3c9f01668e28876565c57c5203f9b92628f085e68496e337b88eed4` |
| `j29_v0.13.py` | `126c1e387ee451c70bca9de3e0242df573f7c82ea1fa2130e497d994df7216db` |
| `games.ini` | `30d5c8232f0eaee90d904ffcc040acc05e8e48d795fef472bd3a50b34c67702b` |

## Relationship to Current Development

`v0.13` remains the stable reference snapshot immediately before the **v0.14 — Core Engine Separation** architecture pivot.

The project's development rule remains:

> **Big vision. Small versions. Stable checkpoints. No chaos.**

Future work should preserve stable checkpoints without rewriting these historical source files.