# RAIkeep

`RAIkeep` is the umbrella workspace for the related `JsonPit`, `OsLib`, `RaiUtils`, and `RaiImage` libraries plus the `PitSeeder` and `iorg` CLIs.

It keeps the child repositories available together for local integration work while preserving each package's own identity, solution files, and release flow.

## Current Aligned Version

The current aligned workspace release line is `3.9.1` for:

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`
- `PitSeeder`
- `iorg`

## 3.9.1 Decisions

- Release line update: aligns the package line on `3.9.1` across the four NuGet-published libraries plus the `ImgSeeder` and `PitSeeder` CLIs.
- The concrete source-level changes in this patch line are RaiImage's smarter filename normalization for trailing image numbers and uppercase tokens, plus the integrated `iorg` packaging/test/release-chain flow.
- Current markdown and PlantUML surfaces were refreshed so the live release docs match the current codebase state.
- The preferred fire-and-forget publishing path is the GitHub Sequential NuGet Release Chain with `publish_to_nuget=true`.

## Included repositories

- `JsonPit`
- `OsLib`
- `PitSeeder`
- `RaiUtils`
- `RaiImage`
- `iorg`

`PitSeeder` and `iorg` are included in the umbrella workspace so each CLI can build against the local package sources and ship from the same release baseline.

## Local validation

From the repository root:

- `dotnet build RAIkeep.slnx`
- `dotnet test RAIkeep.slnx`
- `dotnet test RaiImage/RaiImage.slnx`
