# OsLibCore 4.1.0

Implements the OsLib portion of
`CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md`.

- `Os.TempDir` remains the configured runtime `RaiPath` and is documented as a
  public boundary.
- First Os initialization validates the configured directory by creating,
  observing, and removing an OsLib `TmpFile`.
- Initialization fails fast when the probe cannot be written. `Os.Config` is not
  mutated and the configured path is not silently replaced by a fallback.
- Adds `RaiPathException` and `RaiPathNotFoundException` for explicit missing-path
  failures.
- Adds `RaiFile.WriteFromAsync(IAsyncEnumerable<byte[]>, CancellationToken)` for
  consumers that should not receive a `System.IO.Stream` boundary.

Release verification: 81 OsLib Release tests passed.
