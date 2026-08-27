# OsLibCore 4.2.3

Coordinated CR015 patch release.

- Adds public `PitsDeletePropertyRequest` and `PitsDeleteItemRequest` contracts.
- Adds exact token builders for `pits delete-property` and `pits delete-item`.
- Adds synchronous and asynchronous typed execution through `PitsCommand`.
- Validates mandatory pit, item, and dot-delimited property-path values before
  process execution.
- Retains the CR014 `CliCommand`/`RaiSystem` tokenized execution and result
  boundary unchanged.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

Release verification: 110 OsLib Release tests passed, including six added
CR015 typed-delete token and validation cases.
