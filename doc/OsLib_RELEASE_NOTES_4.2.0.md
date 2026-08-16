# OsLibCore 4.2.0

Coordinated release for the seven-package RAIkeep 4.2 line.

- Preserves the CR008 `Os.TempDir` contract introduced in 4.1.0: the configured
  `RaiPath` is validated once with an OsLib `TmpFile` probe and initialization
  fails fast when it cannot be written.
- Preserves `Os.Config` as the immutable runtime source of truth without a
  fallback to a different temporary directory.
- Carries `RaiPathException`, `RaiPathNotFoundException`, and asynchronous byte
  chunk ingestion forward for RaiImage and RaiDiagram consumers.
- Updates package metadata and documentation for the coordinated 4.2.0 line.

No intentional OsLib runtime behavior change is introduced after 4.1.0.

Release verification: 81 OsLib Release tests passed.
