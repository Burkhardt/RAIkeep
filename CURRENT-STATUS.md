# CURRENT-STATUS

This file captures the current release-ready status of the RAIkeep workspace so a later session can resume without re-deriving the recent decisions.

## Current focus

The current release-and-docs alignment pass is `3.8.12`.

## 3.8.12 release decisions

- The active OsLib config contract is `RAIkeep.json5` with PascalCase property names and lazy `dynamic` access through `Os.Config`.
- `UserHomeDir` and `AppRootDir` are intrinsic runtime values.
- `TempDir` and `LocalBackupDir` remain config-driven.
- `SyncPropagationDelayMs` is optional config and can override metadata-propagation waits.
- `CloudPathWiring` initializes `RaiPath.CloudEvaluator`, and `RaiPath` buffers its `Cloud` state.
- Directory wait logic lives in `RaiPath`; file wait logic lives in `RaiFile`.
- `RaiFile.BackdateCreationTime(...)` manipulates `CreationTimeUtc`, nudges sync via a sentinel file, and honors the configured propagation delay order.
- Current markdown and PlantUML release markers were refreshed so the live release surface matches the current codebase state.
- Older references to `CloudStorageRootDir`, public `LoadConfig(...)`, provider-selection helpers, and observer-specific `Os` APIs are historical only.

## Agreed direction

The following points are now agreed:

- the canonical Os config location is `~/.config/RAIkeep.json5`
- resolution of `~` is acceptable and does not count as an environment-variable violation
- real cloud tests must use config-driven cloud roots only
- mechanics tests may still use controlled test environments
- `TempDir` and `LocalBackupDir` belong to the base Os configuration
- `UserHomeDir` and `AppRootDir` are intrinsic runtime paths and are not config-driven
- legacy `homeDir` is compatibility input only and is ignored at runtime
- cloud provider entries are optional individually

The important clarification from the latest discussion is this:

- none of the four cloud providers are mandatory
- if a provider is absent from config, tests for that provider should skip
- if a provider is present in config and its configured directory is invalid or missing, tests for that provider should fail

## Current implementation status

Completed concepts currently in the codebase:

- `Os.Config` is lazy, internal-load, and backed by `RAIkeep.json5`
- `Os.IsConfigLoaded` exposes config lifecycle state without opening a public reload API
- `CloudPathWiring` provides the delegate bridge from `Os.Config` to `RaiPath.CloudEvaluator`
- `RaiPath` buffers its `Cloud` state and owns directory wait logic
- `RaiFile` copies the buffered `Cloud` flag and owns file wait logic
- `RaiFile.DefaultSyncPropagationDelayMs` provides the in-process fallback for metadata propagation waits
- `RaiFile.BackdateCreationTime(...)` supports deterministic remote-sync test setup without forcing one global latency for every machine
- the fake config-writing test backdoor was removed from `OsLib.Tests`
- OsLib diagrams and current docs are being aligned to the post-purge architecture

The current real-cloud helper is:

- `OsLib/OsLib.Tests/CloudStorageRealTestEnvironment.cs`

The real cloud tests currently using that flow are:

- `OsLib/OsLib.Tests/ConfiguredCloudStorageRootTests.cs`
- `OsLib/OsLib.Tests/CloudStorageAgreementTests.cs`
- `OsLib/OsLib.Tests/CloudStorageProviderPathTests.cs`
- `OsLib/OsLib.Tests/CloudStorageRealWorldIntegrationTests.cs`
- `OsLib/OsLib.Tests/CloudRemoteSyncTests.cs`
- `JsonPit/JsonPit.Tests/CloudRemoteSyncTests.cs`
- `OsLib/OsLib.Tests/RemoteSshTests.cs`

## Current result

The most recent verified command in this session is the umbrella solution test:

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- result: 243 passed, 0 failed, 1 skipped

## Latest validation result

Latest directly verified result in this workspace state:

- umbrella solution build and test pass succeeded
- PlantUML SVG regeneration completed with the local `plantuml` binary
- package pack validation is partial: `OsLibCore.3.8.12.nupkg` and `RaiUtils.3.8.12.nupkg` were created locally, while solution-level and remaining package pack attempts exited without useful diagnostics before creating packages
- the older umbrella and remote-observer notes below this point should be treated as historical context unless revalidated

## Design insight from the latest discussion

One key architectural point was clarified:

- if alternative temp-directory behavior is ever needed, it belongs in `Os`, not in the real cloud test helper

This means the real cloud helper should not invent fallback roots under `Path.GetTempPath()`.

That fallback has already been removed from the mandatory helper path.

## Additional documentation and diagram updates completed in this session

- `Os-ClassDiagram.puml` was updated to reflect `Os` as a static partial class
- PlantUML marker convention was made explicit with `Ⓢ`, `Ⓟ`, and `Ⓐ`
- the stale `Persist()` entry was removed from the `OsConfigFile` diagram node
- the class header sizing was tuned using inline PlantUML label formatting

## Release alignment

The workspace is aligned to version `3.8.12` across:

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`
- `PitSeeder`
- the umbrella `RAIkeep` workspace documentation and submodule references

## Current operational note

- The `3.8.12` release-prep pass updates package metadata, dependency fallbacks, live release docs, and PlantUML markers.
- The intended fire-and-forget publishing path is the GitHub Sequential NuGet Release Chain with `publish_to_nuget=true`.
- The chain publishes `OsLibCore`, `RaiUtils`, `RaiImage`, `JsonPit`, and `PitSeeder` in dependency order.

## Suggested resume prompt

```text
Please read CURRENT-STATUS.md first, then continue from the prepared `3.8.12` umbrella baseline. Use the GitHub Sequential NuGet Release Chain with `publish_to_nuget=true` for the fire-and-forget publishing step.
```

## Related files

- `CURRENT-STATE.md`
- `MANIFESTO.md`
- `OsLib/Os.CloudStorage.cs`
- `OsLib/ConfigFile.cs`
- `OsLib/RaiFile.cs`
- `OsLib/OsLib.Tests/CloudStorageRealTestEnvironment.cs`
- `OsLib/OsLib.Tests/ConfiguredCloudStorageRootTests.cs`
- `OsLib/OsLib.Tests/CloudStorageAgreementTests.cs`
- `OsLib/OsLib.Tests/CloudStorageProviderPathTests.cs`
- `OsLib/OsLib.Tests/CloudStorageRealWorldIntegrationTests.cs`
- `OsLib/OsLib.Tests/CloudRemoteSyncTests.cs`
- `OsLib/OsLib.Tests/RemoteSshTests.cs`
- `JsonPit/JsonPit.Tests/CloudRemoteSyncTests.cs`
- `OsLib/OsLib.Tests/OsEnvironmentPathTests.cs`
