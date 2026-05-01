# RAIkeep

`RAIkeep` is the umbrella workspace for the related `JsonPit`, `OsLib`, `RaiUtils`, and `RaiImage` libraries plus the `PitSeeder` CLI.

It keeps the child repositories available together for local integration work while preserving each package's own identity, solution files, and release flow.

## Current Aligned Version

The current aligned workspace version is `3.7.7` for:

- `JsonPit`
- `OsLib`
- `PitSeeder`
- `RaiUtils`
- `RaiImage`

## 3.7.7 Decisions

- Patch release: aligns the package line on `3.7.7` across all five projects in the workspace.
- Current markdown and PlantUML surfaces were refreshed so the live release docs match the current codebase state.

## Included repositories

- `JsonPit`
- `OsLib`
- `PitSeeder`
- `RaiUtils`
- `RaiImage`

`PitSeeder` is included in the umbrella workspace so the CLI can build against the local `JsonPit` and `OsLib` source projects while package publishing catches up.

## Local validation

From the repository root:

- `dotnet build RAIkeep.slnx`
- `dotnet test RAIkeep.slnx`
- `dotnet test RaiImage/RaiImage.slnx`
