# RaiImage 4.2.0

Coordinated release supporting approved
`CR009_AIA_to_RAIkeep_RaiDiagram_Package.md`.

- Supplies RaiDiagram's supported PlantUML rendering and image-artifact boundary.
- Keeps `RaiImageIOException`, `RaiImageNotFoundException`,
  `RaiPathNotFoundException`, and `ToolNotFoundException` distinctions intact.
- Keeps asynchronous byte-chunk ingestion available without exposing a stream
  boundary to consumers.
- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.0.
- Makes `UseLocalRAIkeepSources=false` force package references, so the release
  gate cannot silently substitute sibling project sources.

The public RaiImage behavior introduced in 4.1.0 remains compatible.

Release verification: 97 RaiImage Release tests passed.
