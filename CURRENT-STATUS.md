# CURRENT-STATUS

This file captures the current release-ready status of the RAIkeep workspace so a later session can resume without re-deriving the recent decisions.

## Current focus

The `3.6.1` patch corrects the NuGet publish order and aligns all packages on version `3.6.1`.

## 3.6.1 release decisions

- The supported cloud-provider claim for the packaged `RAIkeep` stack is `OneDrive`, `GoogleDrive`, and `Dropbox`.
- In `JsonPit`, `PitItem.Id` replaces `Name` as the framework identifier.
- Legacy files that contain `Name` but not `Id` are normalized internally to `Id`, and the framework-managed `Name` field is removed.
- `Name` remains supported as an application-defined custom field outside the framework contract.

## Agreed direction

The following points are now agreed:

- the canonical Os config location is `~/.config/RAIkeep/osconfig.json`
- resolution of `~` is acceptable and does not count as an environment-variable violation
- real cloud tests must use config-driven cloud roots only
- mechanics tests may still use controlled test environments
- `tempDir` and `localBackupDir` belong to the base Os configuration
- `UserHomeDir` and `AppRootDir` are intrinsic runtime paths and are not config-driven
- legacy `homeDir` is compatibility input only and is ignored at runtime
- cloud provider entries are optional individually

The important clarification from the latest discussion is this:

- none of the four cloud providers are mandatory
- if a provider is absent from config, tests for that provider should skip
- if a provider is present in config and its configured directory is invalid or missing, tests for that provider should fail

## Current implementation status

The `3.5.0` refactor and release-alignment work is now implemented in the workspace.

Completed concepts currently in the codebase:

- fixed default config path handling in `Os.CloudStorage.cs`
- config-path override support for tests
- config-only cloud resolution mode for real cloud tests
- real cloud test helper split through `CloudStorageRealTestEnvironment`
- replacement of the old soft helper with a mandatory helper that throws when mandatory preconditions are not met
- `UserHomeDir`, `AppRootDir`, `TempDir`, `LocalBackupDir`, and `CloudStorageRootDir` clarified and documented with current semantics
- startup-critical `osconfig.json` diagnostics now log through `ILogger<T>` and emit explicit degraded-mode console diagnostics
- `GetBackupRelativeDirectoryPath(...)` now returns `RaiPath`, and `RaiFile.backup(copy)` composes destinations through `Os.LocalBackupDir / relativePath`
- workspace package versions and fallback package references are aligned to `3.6.1`

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

The remote test setup was repaired during this session by fixing the remote `mzansi` `osconfig.json` content. The previously skipped remote SSH and cloud-sync tests now execute successfully.

## Latest validation result

Most recent umbrella command:

```bash
dotnet test RAIkeep.slnx --nologo -v minimal
```

Latest umbrella result:

- total: 200
- failed: 2
- succeeded: 200
- skipped: 0

Targeted rerun of the previously skipped remote-gated tests:

- passed: 8
- failed: 0
- skipped: 0

One intermediate full-suite rerun showed two transient remote-sync failures, but those same tests passed on immediate targeted rerun and the subsequent clean full-suite rerun above. The current release-ready status is based on the latest clean full pass.

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

The workspace is being aligned to version `3.6.1` across:

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`
- the umbrella `RAIkeep` workspace documentation and release tag

## Important remaining task

The main remaining task is operational rather than code-centric:

1. review the dirty subprojects and umbrella docs one final time
2. check in the `3.6.1` release-alignment changes
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
Please read CURRENT-STATUS.md first, then continue from the release-ready `3.6.1` state. The code and tests are green; the next task is final review, check-in, and release labeling.
```