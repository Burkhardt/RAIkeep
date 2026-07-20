# RAIkeep

`RAIkeep` is the umbrella workspace for the related `OsLib`, `RaiUtils`, `RaiImage`, and `JsonPit` libraries plus the `ImgSeeder`/`iorg` and `PitSeeder` CLIs.

It keeps the child repositories available together for local integration work while preserving each package's own identity, solution files, and release flow.

## Current Aligned Version

The prepared next workspace release line is `3.12.1` for:

- `OsLib`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder`
- `PitSeeder`

## 3.12.1 Decisions

- Patch release prep: aligns the package line on `3.12.1` across the four NuGet-published libraries plus the `ImgSeeder`/`iorg` and `PitSeeder` CLIs.
- The live child `HEAD` baseline for this prep is `3.12.0` across all six child repositories, so the next coordinated patch is `3.12.1`.
- Remote GitHub tag and publication state could not be re-verified from this environment because `github.com` DNS resolution failed during this run.
- The concrete source-level behavior carried into this patch line includes RaiImage's current `WordCase` guidance, JsonPit's `DeleteProperty(...)` top-level tombstone projection, and the integrated `iorg`/`pits` tool packaging flow.
- Current markdown and PlantUML surfaces were refreshed so the prepared release docs match the `3.12.1` package state.
- The strict package order is `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`; each package must complete publish workflow success, NuGet flat-container visibility, and the 300-second indexing hold before the next package starts.

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
- `dotnet test RaiImage/RaiImage.slnx`
- `dotnet test ImgSeeder/ImgSeeder.slnx`
- `dotnet test PitSeeder/PitSeeder.slnx`
- `dotnet test RAIkeep.slnx`
