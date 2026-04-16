# CURRENT-STATUS

This file captures the current release-ready status of the RAIkeep workspace so a later session can resume without re-deriving the recent decisions.

## Current focus

The current release-and-docs alignment pass is `3.7.6`.

## 3.7.6 release decisions

- The active OsLib config contract is `RAIkeep.json5` with PascalCase property names and lazy `dynamic` access through `Os.Config`.
- `UserHomeDir` and `AppRootDir` are intrinsic runtime values.
- `TempDir` and `LocalBackupDir` remain config-driven.
- `SyncPropagationDelayMs` is optional config and can override metadata-propagation waits.
- `CloudPathWiring` initializes `RaiPath.CloudEvaluator`, and `RaiPath` buffers its `Cloud` state.
- Directory wait logic lives in `RaiPath`; file wait logic lives in `RaiFile`.
- `RaiFile.BackdateCreationTime(...)` manipulates `CreationTimeUtc`, nudges sync via a sentinel file, and honors the configured propagation delay order.
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

The most recent verified command in this session is the OsLib test project:

- `dotnet test OsLib/OsLib.Tests/OsLib.Tests.csproj --nologo -v minimal`
- result: 56 passed, 0 failed

## Latest validation result

Latest directly verified result in this workspace state:

- OsLib test project build and test pass succeeded
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

The workspace is being aligned to version `3.7.6` across:

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`
- the umbrella `RAIkeep` workspace documentation and release tag

## Important remaining task

The main remaining task is operational rather than code-centric:

1. review the dirty subprojects and umbrella docs one final time
2. check in the `3.7.6` release-alignment changes
3. create the release label/tag once the final review is complete

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

## Suggested resume prompt

```text
Please read CURRENT-STATUS.md first, then continue from the release-ready `3.7.6` state. The code and tests are green; the next task is final review, check-in, and release labeling.
```