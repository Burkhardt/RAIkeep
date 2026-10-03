# Release Notes: OsLib v4.5.3

OsLib v4.5.3 delivers CR051 configuration compatibility for multi-account cloud roots and symbolic shortcuts:

- **Unrestricted Cloud Roots**: `Os.Config` reads every nonempty string root declared in `Cloud`, eliminating the previous restriction to four legacy provider names. Roots are normalized and deduplicated.
- **Symbolic Link Resolution**: `ConfiguredCloudPaths` resolves symbolic shortcuts (such as `~/.CloudStorage/*`) and existing ancestors of new candidate paths, ensuring cloud-safe atomic in-place file handling across shortcuts.
- **Dependency Alignment**: Internal package dependencies align to 4.5.3.

Validation and release handoff: [RAIkeep 4.5.3](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RAIkeep_RELEASE_NOTES_4.5.3.md). Preparation does not publish this package.
