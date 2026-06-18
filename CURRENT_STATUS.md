# CURRENT_STATUS

Current note for `3.10.1`:

- The workspace is prepared locally on the coordinated `3.10.1` patch release line.
- Package metadata, fallback dependency versions, live release docs, and PlantUML markers are aligned across `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder/iorg`, and `PitSeeder`.
- The carried-forward payload is RaiImage filename normalization plus the integrated `iorg` packaging/test/release-chain flow.
- Fresh local `dotnet test` reruns are blocked in this sandbox because MSBuild/VSTest cannot open the required named-pipe/socket endpoints.
- No `3.10.1` child commits, parent submodule-pointer updates, or publish workflows have been pushed from this environment yet.

This file records the current RAIkeep workspace state after the local `3.10.1` release-prep pass.

## Current focus

The active line is a coordinated `3.10.1` workspace release across:

- `OsLib`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder/iorg`
- `PitSeeder`

## Implementation

- `OsLib`, `RaiUtils`, `RaiImage`, `JsonPit`, `ImgSeeder/iorg`, and `PitSeeder` package versions were aligned to `3.10.1`.
- The coordinated release order remains `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- Downstream fallback package references were advanced to the same `3.10.1` line.
- Live README, API, release-note, workflow, and root status documents were refreshed to point at the `3.10.1` baseline.
- PlantUML release markers were updated and the changed SVGs were regenerated locally where those SVGs are tracked.
- `RAIkeep.slnx` includes `PitSeeder/pits/pits.csproj`, `PitSeeder/pits.Tests/pits.Tests.csproj`, `iorg/iorg.csproj`, and `iorg/iorg.Tests/iorg.Tests.csproj`.
- The parent sequential release chain now packs and publishes `ImgSeeder` between `JsonPit` and `PitSeeder`, with the existing 300-second waits preserved.

## Test coverage

The intended focused validation set for this prep run is:

- `OsLib/OsLib.slnx`
- `RaiUtils/RaiUtils.slnx`
- `RaiImage/RaiImage.slnx`
- `JsonPit/JsonPit.slnx`
- `iorg/iorg.slnx`
- `PitSeeder/PitSeeder.slnx`
- `RAIkeep.slnx`

## Validation

Most recent previously verified package results in this workspace:

- `OsLib.Tests`: 64 passed
- `RaiUtils.Tests`: 21 passed
- `RaiImage.Tests`: 91 passed
- `JsonPit.Tests`: 88 passed, 1 skipped
- `iorg.Tests`: 4 passed
- `pits.Tests`: 3 passed

Most recent previously verified umbrella validation:

```text
dotnet test RAIkeep.slnx --nologo -v minimal
Passed: 271, Failed: 0, Skipped: 1
```

## Publishing state

- No `3.10.1` tags or publish workflows were triggered in this prep run.
- The intended publish path remains the parent `RAIkeep` workflow `.github/workflows/sequential-nuget-release-chain.yml`.
- The expected order is `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- The workflow now preserves the 300-second waits and adds NuGet flat-container `.nupkg` verification steps for every published package, including `imgseeder`.
- This environment cannot push the prepared child commits because shell GitHub access is DNS-blocked and no workflow-dispatch tool is available in-session.

## Suggested resume prompt

```text
Please read CURRENT_STATUS.md first. The `3.10.1` release-prep baseline is ready locally, but push and publish still require an environment with GitHub network access.
```
