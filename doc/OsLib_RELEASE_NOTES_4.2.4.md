# OsLibCore 4.2.4

Coordinated dependency release for accepted CR016.

- Retains the existing `RaiPath.EnumerateDirectories(...)` and
  `RaiPath.EnumerateFiles(...)` boundary used by RaiImage's normalization-
  resilient resolver.
- Adds no new direct filesystem API or OsLib runtime behavior.
- Carries CR008, CR014, and CR015 boundaries forward unchanged.

Release verification: 110 OsLibCore Release tests passed.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.
