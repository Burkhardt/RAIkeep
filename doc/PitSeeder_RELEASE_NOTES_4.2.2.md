# PitSeeder 4.2.2

Coordinated dependency release for the seven-package RAIkeep 4.2.2 line.

- Aligns fallback dependencies on JsonPit and OsLibCore 4.2.2.
- Retains the 4.2.1 Nerd Font provider and numbered-option glyphs, Blink
  stylesheet guidance, and clipping tolerance.
- Retains the command-first and compatible 4.x legacy `pits` behavior.
- Reports `pits v4.2.2` through the CLI version boundary.
- Its package-owned entry-point tests invoke the managed CLI through
  `OsLib.PitsCommand.ForManagedAssembly(...)`; its `--version` case is the
  CR014.1 real-CLI smoke check. OsLib tests the transport contract and does not
  duplicate pit behavior.

No tag or publication is authorized by these notes. RAI starts the coordinated
release chain manually after reviewing the prepared commits and verification.

Release verification: 20 PitSeeder Release tests passed.
