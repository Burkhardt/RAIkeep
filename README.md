# RAIkeep

`RAIkeep` is the umbrella workspace for the related `OsLib`, `RaiUtils`, `RaiImage`, and `JsonPit` libraries plus the `ImgSeeder`/`iorg` and `PitSeeder` CLIs.

It keeps the child repositories available together for local integration work while preserving each package's own identity, solution files, and release flow.

## Current Aligned Version

The current aligned workspace release line is `3.10.0` for:

- `OsLib`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder/iorg`
- `PitSeeder`

## 3.10.0 Decisions

- Release line update: aligns the package line on `3.10.0` across the four NuGet-published libraries plus the `ImgSeeder` and `PitSeeder` CLIs.
- The concrete source-level behavior carried into this minor line remains RaiImage's smarter filename normalization for trailing image numbers and uppercase tokens, plus the integrated `iorg` packaging/test/release-chain flow.
- Current markdown and PlantUML surfaces were refreshed so the live release docs match the current codebase state.
- The GitHub Sequential NuGet Release Chain remains the intended later publish path, in the order `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.

## Included repositories

- `OsLib`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder/iorg`
- `PitSeeder`

`PitSeeder` and `iorg` are included in the umbrella workspace so each CLI can build against the local package sources and ship from the same release baseline.

## Local validation

From the repository root:

- `dotnet build RAIkeep.slnx`
- `dotnet test RAIkeep.slnx`
- `dotnet test RaiImage/RaiImage.slnx`
