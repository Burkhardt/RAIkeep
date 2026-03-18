# CURRENT-STATUS

This file captures the current in-progress status of the RAIkeep workspace so a later session can resume without re-deriving the recent decisions.

## Current focus

The work is currently centered on `OsLib` and specifically on the relationship between:

- `OsConfigFile`
- `Os.HomeDir`, `Os.TempDir`, `Os.LocalBackupDir`, and `Os.Config`
- real cloud tests versus mechanics tests
- the removal of environment-variable-based setup from the real cloud test path
- the release-preparation alignment toward workspace version `3.4.0`

## Agreed direction

The following points are now agreed:

- the canonical Os config location is `~/.config/RAIkeep/osconfig.json`
- resolution of `~` is acceptable and does not count as an environment-variable violation
- real cloud tests must use config-driven cloud roots only
- mechanics tests may still use controlled test environments
- `homeDir`, `tempDir`, and `localBackupDir` belong to the base Os configuration
- cloud provider entries are optional individually

The important clarification from the latest discussion is this:

- none of the four cloud providers are mandatory
- if a provider is absent from config, tests for that provider should skip
- if a provider is present in config and its configured directory is invalid or missing, tests for that provider should fail

## Current implementation status

The refactor has already progressed significantly.

Implemented concepts currently in the codebase:

- fixed default config path handling in `Os.CloudStorage.cs`
- config-path override support for tests
- config-only cloud resolution mode for real cloud tests
- real cloud test helper split through `CloudStorageRealTestEnvironment`
- replacement of the old soft helper with a mandatory helper that throws when mandatory preconditions are not met

The current real-cloud helper is:

- `OsLib/OsLib.Tests/CloudStorageRealTestEnvironment.cs`

The real cloud tests currently using that flow are:

- `OsLib/OsLib.Tests/ConfiguredCloudStorageRootTests.cs`
- `OsLib/OsLib.Tests/CloudStorageAgreementTests.cs`
- `OsLib/OsLib.Tests/CloudStorageProviderPathTests.cs`
- `OsLib/OsLib.Tests/CloudStorageRealWorldIntegrationTests.cs`

## Current problem

The latest implementation made the provider requirement too strict.

At the moment, the real cloud helper treats configured-provider availability as mandatory in a way that causes hard failures for a provider whose directory does not exist, but it does not yet distinguish correctly between these two cases:

1. provider not configured at all
2. provider configured but invalid

The intended behavior is:

- missing `osconfig.json`: hard failure for the mandatory config path
- missing provider entry such as `cloud.googledrive`: skip that provider's tests
- present provider entry with nonexistent directory: fail that provider's tests

This rule is understood, but not yet fully implemented.

## Latest validation result

Most recent umbrella command:

```bash
dotnet test RAIkeep.slnx --nologo -v minimal
```

Latest umbrella result:

- total: 192
- failed: 2
- succeeded: 188
- skipped: 2

Current failing tests:

- `OsLib.Tests.CloudRemoteSyncTests.TextFile_SyncsWithMzansi(provider: GoogleDrive)`
- `OsLib.Tests.CloudStorageAgreementMechanicsTests.CloudStorageRoot_UsesDocumentedDefaultOrder_ForConfiguredRoots()`

Failure details currently observed:

- `CloudRemoteSyncTests.TextFile_SyncsWithMzansi(provider: GoogleDrive)` fails because delete propagation to the Mzansi remote did not complete within the timeout even though the local delete succeeded.
- `CloudStorageAgreementMechanicsTests.CloudStorageRoot_UsesDocumentedDefaultOrder_ForConfiguredRoots()` currently resolves `DropboxRoot` while the test still expects `GoogleDriveRoot`, which means either the documented order or the test expectation is now out of sync.

The most recent OsLib-only command before the umbrella rerun was:

```bash
dotnet test OsLib/OsLib.Tests/OsLib.Tests.csproj --nologo -v minimal
```

That earlier OsLib-only result was:

- total: 119
- failed: 7
- succeeded: 109
- skipped: 3

The unrelated `TempDir_MatchesSystemTempPath_WhenNotConfigured` test was fixed and is now green.

That earlier failing set reflected the prior provider-resolution issue before the latest umbrella rerun exposed a different current pair of failures.

The failing provider is `GoogleDrive`, which is configured in the active config but currently points to a directory that does not exist:

- `/Users/RSB/Library/CloudStorage/GoogleDrive/Umshadisi/TestAfricaStage/`

Representative failing tests:

- `ConfiguredCloudStorageRootTests.GetCloudStorageRoots_ReturnsConfiguredProviderRoots_AsCloudPaths(provider: GoogleDrive)`
- `ConfiguredCloudStorageRootTests.GetCloudStorageRoot_ReturnsConfiguredProviderRoot_WhenAvailable(provider: GoogleDrive)`
- `CloudStorageAgreementTests.RaiFile_UsesConfiguredProviderRoot_ForCloudAwareFlag(provider: GoogleDrive)`
- `CloudStorageProviderPathTests.GetCloudStorageProviderForPath_ReturnsConfiguredProvider_ForConfiguredRoot(provider: GoogleDrive)`
- `CloudStorageProviderPathTests.RaiFile_CloudFlag_DetectsFilesUnderConfiguredProvider(provider: GoogleDrive)`
- `CloudStorageRealWorldIntegrationTests.TextFile_SaveAndRead_WorksAgainstRealWritableCloudProvider(provider: GoogleDrive)`
- `CloudStorageRealWorldIntegrationTests.RaiFile_RoundTrip_WorksAgainstRealWritableCloudProvider(provider: GoogleDrive)`

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

The workspace is being aligned to version `3.4.0` across:

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`
- the umbrella `RAIkeep` workspace documentation and release tag

## Important remaining task

The next implementation step should be to refine the real cloud helper and its callers so that provider entries are treated as optional individually.

That means:

1. keep mandatory failure for missing `osconfig.json`
2. skip tests when the requested provider is absent from config
3. fail tests when the requested provider is present in config but its configured directory is invalid or missing

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
- `OsLib/OsLib.Tests/OsEnvironmentPathTests.cs`

## Suggested resume prompt

```text
Please read CURRENT-STATUS.md first, then continue the OsLib cloud/config refactor. The next task is to make provider entries optional individually: missing config file should fail, missing provider entry should skip, configured-but-missing provider directory should fail.
```