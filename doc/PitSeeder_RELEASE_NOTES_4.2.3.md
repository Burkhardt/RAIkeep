# PitSeeder 4.2.3

Implements the PitSeeder portion of accepted CR015.

- Adds `pits delete-property <PitName> <ItemId> <PropertyPath>` with explicit
  dot-delimited nested paths.
- Adds `pits delete-item <PitName> <ItemId>` using JsonPit's established item
  tombstone.
- Both commands use the existing pit-root/configured-cloud resolution,
  persistence, and process-window release boundaries.
- `-n` remains `--nologo`; it does not suppress saving or flushing.
- Missing pits/items, malformed paths, unknown options, and invalid positional
  counts return nonzero results with contextual command guidance.
- Reports `pits v4.2.3` through the CLI version boundary.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

Release verification: 23 PitSeeder Release tests passed, including three added
CR015 live-CLI deletion and validation scenarios.
