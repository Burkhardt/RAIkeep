# CURRENT_STATUS

Current note for `3.9.1`:

- The workspace is prepared on the coordinated `3.9.1` patch release line.
- Package metadata, fallback dependency versions, live release docs, and PlantUML markers are aligned across `JsonPit`, `OsLib`, `RaiUtils`, `RaiImage`, `ImgSeeder`, and `PitSeeder`.
- The concrete patch payload is RaiImage filename normalization plus the integrated `iorg` packaging/test/release-chain flow.
- Umbrella validation passed with 271 tests passed and 1 skipped.
- `OsLibCore`, `RaiUtils`, `RaiImage`, and `JsonPit` were already published successfully from their repo tag workflows.
- `ImgSeeder` child-repo publication is blocked by a missing `NUGET_API_KEY` secret in the `iorg` repository, so the parent `RAIkeep` sequential chain is the release path for `ImgSeeder` and `PitSeeder`.

This file records the current RAIkeep workspace state after the `3.9.1` release-prep pass.

## Current focus

The active line is a coordinated `3.9.1` workspace release across:

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`
- `ImgSeeder`
- `PitSeeder`

## Implementation

- `JsonPit`, `OsLib`, `RaiUtils`, `RaiImage`, `ImgSeeder`, and `PitSeeder` package versions were aligned to `3.9.1`.
- Downstream fallback package references were advanced to the same `3.9.1` line.
- Live README, API, release-note, workflow, and root status documents were refreshed to point at the `3.9.1` baseline.
- PlantUML release markers were updated and the changed SVGs were regenerated locally.
- `RAIkeep.slnx` now includes `iorg/iorg.csproj` and `iorg/iorg.Tests/iorg.Tests.csproj`.
- The parent sequential release chain now packs and publishes `ImgSeeder` between `JsonPit` and `PitSeeder`, with the existing 300-second waits preserved.

## Test coverage

The focused validation set for this prep run covered:

- `JsonPit/JsonPit.slnx`
- `OsLib/OsLib.slnx`
- `RaiUtils/RaiUtils.slnx`
- `RaiImage/RaiImage.slnx`
- `iorg/iorg.slnx`
- `PitSeeder/PitSeeder.slnx`
- `RAIkeep.slnx`

## Validation

Focused package results:

- `JsonPit.Tests`: 88 passed, 1 skipped
- `OsLib.Tests`: 64 passed
- `RaiUtils.Tests`: 21 passed
- `RaiImage.Tests`: 91 passed
- `iorg.Tests`: 4 passed
- `pits.Tests`: 3 passed

Umbrella validation:

```text
dotnet test RAIkeep.slnx --nologo -v minimal
Passed: 271, Failed: 0, Skipped: 1
```

## Publishing state

- `OsLib` run `27111254613`: completed successfully for tag `v3.9.1`.
- `RaiUtils` run `27111459597`: completed successfully for tag `v3.9.1`.
- `RaiImage` run `27111673295`: completed successfully for tag `v3.9.1`.
- `JsonPit` run `27111855497`: completed successfully for tag `v3.9.1`.
- `iorg` run `27112104921`: failed because `NUGET_API_KEY` is empty in the repo workflow environment.
- `iorg` run `27112207429`: rerun after CI fix, but the same repo-secret blocker remains.
- The remaining publish path is the parent `RAIkeep` workflow `.github/workflows/sequential-nuget-release-chain.yml` with `publish_to_nuget=true`.

## Suggested resume prompt

```text
Please read CURRENT_STATUS.md first. The `3.9.1` release-prep baseline is validated; finish publication through the parent sequential NuGet release chain.
```
