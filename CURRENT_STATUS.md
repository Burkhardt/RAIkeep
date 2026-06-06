# CURRENT_STATUS

Current note for `3.9.0`:

- The workspace is prepared on the coordinated `3.9.0` minor release line.
- Package metadata, fallback dependency versions, live release docs, and PlantUML markers are aligned in the active repositories.
- RaiImage is the only package with source-level API movement in this line: naming-aware rooted `ImageTreeFile` construction plus public naming inference.
- Umbrella validation passed with 251 tests passed, 0 failed, and 1 skipped.
- This prep run does not publish to NuGet and does not dispatch the GitHub Sequential NuGet Release Chain.

This file records the current RAIkeep workspace state after the `3.9.0` release-prep pass.

## Current focus

The active line is a coordinated `3.9.0` workspace release across:

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`
- `PitSeeder`

## Implementation

- `JsonPit`, `OsLib`, `RaiUtils`, `RaiImage`, and `PitSeeder` package versions were aligned to `3.9.0`.
- Downstream fallback package references were advanced to the same `3.9.0` line.
- Live README, API, release-note, and root status documents were refreshed to point at the `3.9.0` baseline.
- PlantUML release markers were updated and the changed SVGs were regenerated locally.
- RaiImage docs and diagrams now describe the naming-aware `ImageTreeFile.FromName(...)` factories and public `InferSourceNamingConvention(...)`.

## Test coverage

The focused validation set for this prep run covered:

- `JsonPit/JsonPit.Tests/JsonPit.Tests.csproj`
- `OsLib/OsLib.Tests/OsLib.Tests.csproj`
- `RaiUtils/tests/RaiUtils.Tests/RaiUtils.Tests.csproj`
- `RaiImage/RaiImage.Tests/RaiImage.Tests.csproj`
- `PitSeeder/pits.Tests/pits.Tests.csproj`
- `RAIkeep.slnx`

## Validation

Focused package results:

- `JsonPit.Tests`: 88 passed, 1 skipped
- `OsLib.Tests`: 64 passed
- `RaiUtils.Tests`: 21 passed
- `RaiImage.Tests`: 75 passed
- `pits.Tests`: 3 passed

Umbrella validation:

```text
dotnet test RAIkeep.slnx --nologo -v minimal
Passed: 251, Failed: 0, Skipped: 1
```

## Suggested resume prompt

```text
Please read CURRENT_STATUS.md first. The `3.9.0` release-prep baseline is validated; continue from the aligned umbrella state.
```
