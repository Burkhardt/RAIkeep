# OsLib RELEASE NOTES 4.5.8

- Release version: `4.5.8`
- Coordination tag: `v4.5.8`

## Highlights
- Adds typed `DenoCommand` supporting sandboxed local and `OverSsh` remote execution with `--context` / `--context-file` and explicit runtime permissions (`--allow-net`, `--allow-read`, `--deny-read`).
- Adds `CliCommand.OverSsh<T>` fluent remote routing and SSH target dispatch.
- Adds typed fleet CLI wrappers: `AmafuCommand`, `IorgCommand`, `JpitCommand`, `PitsCommand`, and `RaidCommand`.

## Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.8` line.
