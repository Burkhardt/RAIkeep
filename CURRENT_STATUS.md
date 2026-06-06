# CURRENT_STATUS

Current note for `3.8.12`:

- The workspace is being advanced to the coordinated `3.8.12` patch release line.
- Package metadata, fallback dependency versions, live release docs, and PlantUML markers are aligned in the active repositories.
- Umbrella validation passed with 243 tests passed, 0 failed, and 1 skipped.
- Package pack validation is partial: OsLibCore and RaiUtils packages were created locally, while the remaining pack attempts did not produce packages in this sandboxed run.
- The intended publishing path is the GitHub Sequential NuGet Release Chain with `publish_to_nuget=true`, which includes PitSeeder.
- The older `3.8.10` PitSeeder note below is historical context.

This file records the current RAIkeep workspace state after the PitSeeder cloud-relative pitroot fix.

## Current focus

PitSeeder now resolves `-c <provider> -r <pitroot>` by treating the `-r` value as a provider-relative `RaiRelPath`.

PitSeeder release `3.8.10` is prepared as a PitSeeder-only NuGet release. The other NuGet packages are intentionally unchanged.

For example, on this machine:

```text
pits -h -c OneDrive -r LiveAfricaStage
pits -h -c OneDrive -r LiveAfricaStage/
pits -h -c OneDrive -r /LiveAfricaStage
```

all resolve to:

```text
/Users/RSB/Library/CloudStorage/OneDrive/OneDriveData/LiveAfricaStage/
```

## Implementation

- `PitSeeder/pits/Program.cs` now distinguishes cloud-backed pitroot resolution from local pitroot resolution.
- When `-c` is present, `-r` is normalized as a relative path under the configured cloud root.
- A leading slash in the cloud-relative `-r` value is accepted as CLI convenience, preserving the previously working `/LiveAfricaStage` behavior.
- When `-c` is absent, `-r` keeps the previous `RaiPath` behavior, so absolute/local pitroot usage remains supported.
- No OsLib production code was changed.

## Test coverage

A new PitSeeder xUnit test project was added:

- `PitSeeder/pits.Tests/pits.Tests.csproj`
- `PitSeeder/pits.Tests/PitRootCloudResolutionTests.cs`

The new theory covers:

- `LiveAfricaStage`
- `LiveAfricaStage/`
- `/LiveAfricaStage`

and asserts that each resolves to the configured OneDrive root plus `LiveAfricaStage/`.

## Validation

Focused PitSeeder validation:

```text
dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal
Passed: 3, Failed: 0, Skipped: 0
```

PitSeeder package validation:

```text
dotnet pack PitSeeder/pits/pits.csproj --configuration Release --nologo -v minimal
Created: PitSeeder/artifacts/nuget/PitSeeder.3.8.10.nupkg
Verified package contents include README.md
```

Umbrella validation was run with filesystem access outside the workspace, because the existing suite writes to configured temp and cloud roots:

```text
dotnet test RAIkeep.slnx --nologo -v minimal
Passed: 238, Failed: 0, Skipped: 0
```

Latest attempted umbrella validation during the `3.8.10` release prep reached the PitSeeder, RaiUtils, OsLib, and RaiImage assemblies successfully, then failed in the unrelated JsonPit remote-sync scenario:

```text
JsonPit.Tests.RemoteSyncTests.RemoteSync_MasterClient_FullScenario
Mzansi must create change files as a client (not overwrite the pit)
```

Project-level counts from the successful umbrella run:

- `pits.Tests`: 3 passed
- `RaiUtils.Tests`: 21 passed
- `OsLib.Tests`: 64 passed
- `RaiImage.Tests`: 61 passed
- `JsonPit.Tests`: 89 passed

## Suggested resume prompt

```text
Please read CURRENT_STATUS.md first. PitSeeder cloud-relative pitroot resolution is fixed and covered by tests; continue from the passing umbrella solution state.
```
