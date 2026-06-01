# CURRENT_STATUS

This file records the current RAIkeep workspace state after the PitSeeder cloud-relative pitroot fix.

## Current focus

PitSeeder now resolves `-c <provider> -r <pitroot>` by treating the `-r` value as a provider-relative `RaiRelPath`.

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

Umbrella validation was run with filesystem access outside the workspace, because the existing suite writes to configured temp and cloud roots:

```text
dotnet test RAIkeep.slnx --nologo -v minimal
Passed: 238, Failed: 0, Skipped: 0
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
