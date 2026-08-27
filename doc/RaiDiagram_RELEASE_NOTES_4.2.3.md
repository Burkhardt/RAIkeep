# RaiDiagram 4.2.3

Coordinated dependency release for accepted CR015.

- Aligns fallback dependencies on OsLibCore, RaiUtils, and RaiImage 4.2.3.
- Carries `.raid`, `_config.puml`, subscriber-scoped artifacts, deterministic
  style resolution, real PlantUML rendering, and SVG provenance forward
  unchanged.
- Introduces no modeling or identity-management subsystem.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

Release verification: 34 RaiDiagram Release tests passed through the production
renderer path, including the real PlantUML integration available locally.
