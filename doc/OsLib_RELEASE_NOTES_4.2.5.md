# OsLibCore 4.2.5

Typed command-boundary support for accepted CR017.

- Adds optional `PitsExportRequest.At` for point-in-time exports.
- Emits `--at` and a canonical UTC timestamp as separate exact argument tokens.
- Supports the same request through synchronous and asynchronous `PitsCommand`
  execution and managed-assembly test entry points.
- Omitting `At` preserves the established export argument list.

Release verification: 111 OsLibCore Release tests passed.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.
