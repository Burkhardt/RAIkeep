# CURRENT_STATUS

Current note for `3.10.0`:

- The workspace is prepared on the coordinated `3.10.0` minor release line.
- Package metadata, fallback dependency versions, live release docs, and PlantUML markers are aligned across `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder/iorg`, and `PitSeeder`.
- The carried-forward payload is RaiImage filename normalization plus the integrated `iorg` packaging/test/release-chain flow.
- Umbrella validation passed with 271 tests passed and 1 skipped.
- No `3.10.0` publish workflows or NuGet releases were triggered in this prep run.

This file records the current RAIkeep workspace state after the `3.10.0` release-prep pass.

## Current focus

The active line is a coordinated `3.10.0` workspace release across:

- `OsLib`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder/iorg`
- `PitSeeder`

## Implementation

- `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder/iorg`, and `PitSeeder` package versions were aligned to `3.10.0`.
- The coordinated release order remains `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- Downstream fallback package references were advanced to the same `3.10.0` line.
- Live README, API, release-note, workflow, and root status documents were refreshed to point at the `3.10.0` baseline.
- PlantUML release markers were updated and the changed SVGs were regenerated locally.
- `RAIkeep.slnx` includes `PitSeeder/pits/pits.csproj`, `PitSeeder/pits.Tests/pits.Tests.csproj`, `iorg/iorg.csproj`, and `iorg/iorg.Tests/iorg.Tests.csproj`.
- The parent sequential release chain now packs and publishes `ImgSeeder` between `JsonPit` and `PitSeeder`, with the existing 300-second waits preserved.

## Test coverage

The focused validation set for this prep run covered:

- `OsLib/OsLib.slnx`
- `RaiUtils/RaiUtils.slnx`
- `RaiImage/RaiImage.slnx`
- `JsonPit/JsonPit.slnx`
- `iorg/iorg.slnx`
- `PitSeeder/PitSeeder.slnx`
- `RAIkeep.slnx`

## Validation

Focused package results:

- `OsLib.Tests`: 64 passed
- `RaiUtils.Tests`: 21 passed
- `RaiImage.Tests`: 91 passed
- `JsonPit.Tests`: 88 passed, 1 skipped
- `iorg.Tests`: 4 passed
- `pits.Tests`: 3 passed

Umbrella validation:

```text
dotnet test RAIkeep.slnx --nologo -v minimal
Passed: 271, Failed: 0, Skipped: 1
```

## Publishing state

- No `3.10.0` tags or publish workflows were triggered in this prep run.
- The later publish path remains the parent `RAIkeep` workflow `.github/workflows/sequential-nuget-release-chain.yml`.
- The expected order is `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- The `iorg` child repo still lacks a usable `NUGET_API_KEY` secret, so `ImgSeeder` should continue to publish through the parent chain when publication is intentionally requested.

## Suggested resume prompt

```text
Please read CURRENT_STATUS.md first. The `3.10.0` release-prep baseline is validated; tag and publish only when explicitly requested.
```
