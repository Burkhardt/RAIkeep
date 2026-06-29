# RAIkeep

`RAIkeep` is the umbrella workspace for the related `OsLib`, `RaiUtils`, `RaiImage`, and `JsonPit` libraries plus the `ImgSeeder`/`iorg` and `PitSeeder` CLIs.

It keeps the child repositories available together for local integration work while preserving each package's own identity, solution files, and release flow.

## Current Aligned Version

The current aligned workspace release line is `3.13.0` for:

- `OsLib`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder`
- `PitSeeder`

## 3.13.0 Decisions

- Minor release update: aligns the package line on `3.13.0` across the four NuGet-published libraries plus the `ImgSeeder`/`iorg` and `PitSeeder` CLIs.
- The concrete source-level behavior carried into this minor line remains RaiImage's smarter filename normalization and `WordCase` guidance, JsonPit's participant-identity ticket ownership flow, and the integrated `iorg` packaging/test/release-chain flow with cache-delete alias support.
- Current markdown and PlantUML surfaces were refreshed so the live release docs match the current codebase state.
- The GitHub Sequential NuGet Release Chain remains the intended later publish path, in the order `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`, but it is not triggered by this prep pass.

## Included repositories

- `OsLib`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder`
- `PitSeeder`

`PitSeeder` and `iorg` are included in the umbrella workspace so each CLI can build against the local package sources and ship from the same release baseline.

## Local validation

From the repository root:

- `dotnet build RAIkeep.slnx`
- `dotnet test RAIkeep.slnx`
- `dotnet test RaiImage/RaiImage.slnx`
