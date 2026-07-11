# RAIkeep

`RAIkeep` is the umbrella workspace for the related `OsLib`, `RaiUtils`, `RaiImage`, and `JsonPit` libraries plus the `ImgSeeder`/`iorg` and `PitSeeder` CLIs.

It keeps the child repositories available together for local integration work while preserving each package's own identity, solution files, and release flow.

## Current Aligned Version

The current aligned workspace release line is `3.11.4` for:

- `OsLib`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder`
- `PitSeeder`

## 3.11.4 Decisions

- Patch release update: aligns the package line on `3.11.4` across the four NuGet-published libraries plus the `ImgSeeder`/`iorg` and `PitSeeder` CLIs.
- The release baseline was the latest remote tag common to all six child repos, `v3.11.3`; local unreleased `3.13.0` prep was not used as the release source of truth.
- The concrete source-level behavior carried into this patch line includes RaiImage's current `WordCase` guidance, JsonPit's fixed `DeleteProperty(...)` top-level tombstone projection, and the integrated `iorg`/`pits` tool packaging flow.
- Current markdown and PlantUML surfaces were refreshed so the live release docs match the current `3.11.4` package state.
- The strict package order is `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`; each package must complete publish workflow success, NuGet flat-container visibility, and the 330-second indexing hold before the next package starts.

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
