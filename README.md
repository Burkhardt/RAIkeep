# RAIkeep

`RAIkeep` is the umbrella workspace for the related `OsLib`, `RaiUtils`, `RaiImage`, and `JsonPit` libraries plus the `ImgSeeder`/`iorg` and `PitSeeder` CLIs.

It keeps the child repositories available together for local integration work while preserving each package's own identity, solution files, and release flow.

All RAIkeep change requests and release notes are centralized in [`doc/`](doc/README.md). Files use a source-project prefix, such as `RaiImage_CR_...` and `JsonPit_RELEASE_NOTES_...`, to prevent collisions; child repositories should not keep separate `CR_*.md` or `RELEASE_NOTES*.md` files.

## Current Aligned Version

The prepared next workspace release line is `3.13.1` for:

- `OsLib`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder`
- `PitSeeder`

## 3.13.1 Decisions

- Patch release prep: aligns the package line on `3.13.1` across the four NuGet-published libraries plus the `ImgSeeder`/`iorg` and `PitSeeder` CLIs.
- The coordinated next-release version is `3.13.1` across all six child repositories.
- Remote GitHub tag and publication state could not be re-verified from this environment because `github.com` DNS resolution failed during this run.
- The concrete source-level behavior carried into this minor line includes RaiImage's current `WordCase` guidance, JsonPit's `DeleteProperty(...)` top-level tombstone projection, and the integrated `iorg`/`pits` tool packaging flow.
- PitSeeder finite commands now release their ownership-verified, per-process JsonPit activity windows by default; `--retain-window` explicitly keeps the timeout behavior, while master writer tickets remain separate.
- Current markdown and PlantUML surfaces were refreshed so the prepared release docs match the `3.13.1` package state.
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
