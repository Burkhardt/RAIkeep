# RaiDiagram 4.2.4

Coordinated dependency release for accepted CR016.

- Aligns fallback dependencies on OsLibCore, RaiUtils, and RaiImage 4.2.4.
- Adopts RaiImage's Unicode-safe ImageTree placement for `.raid`, `.puml`,
  `_config.puml`, and rendered diagram artifacts.
- Introduces no RaiDiagram public API change.

Release verification: 34 RaiDiagram Release tests passed through the real
PlantUML integration path.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.
