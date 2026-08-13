# RaiUtils 4.1.0

Implements the shared exception portion of
`CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md`.

- Adds `RaiException` as the dependency-light base for public RAIkeep domain
  exceptions.
- Adds `ToolNotFoundException`, carrying stable tool-name and executable-path
  diagnostics for missing command-line dependencies.
- Establishes the shared exception boundary consumed by RaiImage and the
  upcoming RaiDiagram package.

Release verification: 22 RaiUtils Release tests passed.
