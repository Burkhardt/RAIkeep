# OneDrive Tests

Date: 2026-03-16

## 3.5.0 scope note

As of `RAIkeep 3.5.0`, `OneDrive` is one of the three supported cloud providers in the packaged stack alongside `GoogleDrive` and `Dropbox`.

For `JsonPit`, `PitItem.Id` is now the canonical identifier. Legacy persisted payloads that still use `Name` are normalized internally to `Id`, and the framework-managed `Name` field is dropped during normalization.

## Purpose

This note lists the current OneDrive-relevant tests in `RAIkeep`, what each test is meant to prove, how to debug through it, and what runtime or propagation timeframe to expect.

It is intentionally practical rather than exhaustive.

## Short Answer

There is OneDrive coverage at four levels:

1. config and discovery logic
2. provider-path and cloud-flag logic
3. real local writable-provider integration
4. remote sync integration via `Mzansi`

The most important distinction is:

- many OneDrive tests are hermetic and always runnable
- some require a real writable OneDrive root on the local machine
- some also require ssh access plus a valid remote OneDrive root on `Mzansi`

## Local Machine Status In This Session

From the current machine state during this session:

- local `osconfig.json` contains `onedrive: /Users/Shared/AfricaStageOneDrive/`
- `/Users/Shared/AfricaStageOneDrive/` exists
- `remote-test-config.json` contains observer `mzansi`

That means the local preconditions for real local OneDrive tests look present.

What was not verified in this session:

- whether `Mzansi` is reachable by ssh right now
- whether `Mzansi` has a valid OneDrive root configured in its own `~/.config/RAIkeep/osconfig.json`

So local real-provider OneDrive tests are likely runnable here, while remote OneDrive sync tests are only probable, not confirmed.

## Test Inventory

### 1. Discovery and Config Tests

These are fast, hermetic tests. They do not depend on a real OneDrive client.

#### `GetCloudStorageRoots_UsesConfiguredRoots`

File:

- `OsLib/OsLib.Tests/CloudStorageDiscoveryTests.cs`

What it tests:

- when config explicitly contains a OneDrive root, `Os.GetCloudStorageRoots(refresh: true)` returns it

Expected behavior:

- the returned dictionary contains the configured OneDrive path exactly

Expected runtime:

- usually far below 1 second

How to debug:

- step through `env.WriteConfig(...)`
- step into `Os.GetCloudStorageRoots(refresh: true)`
- confirm the config path is read before probe fallback is used

#### `LoadConfig_AutoCreatesDefaultUserConfigFile_WhenMissing`

File:

- `OsLib/OsLib.Tests/CloudStorageDiscoveryTests.cs`

What it tests:

- when the default config file is missing, `Os.LoadConfig(refresh: true)` auto-creates it
- the generated JSON contains an empty `cloud.onedrive` entry rather than inventing a fake path

Expected behavior:

- config file is created
- `cloud.onedrive` is present and empty

Expected runtime:

- usually below 1 second

How to debug:

- step into `Os.LoadConfig(refresh: true)`
- inspect the generated JSON on disk

#### `GetCloudStorageRoots_PrefersConfiguredProviderValue_WithoutProbeFallback`

File:

- `OsLib/OsLib.Tests/CloudStorageDiscoveryTests.cs`

OneDrive case:

- `CloudStorageType.OneDrive`

What it tests:

- if OneDrive is explicitly configured, probe-discovered locations such as `~/OneDrive - Personal` must not override the configured value

Expected behavior:

- effective OneDrive root equals configured path
- effective OneDrive root does not equal the discovered fallback path

Expected runtime:

- usually below 1 second

How to debug:

- place a breakpoint inside `ProbeOneDrive(...)`
- verify configured values win before probe candidates are applied as the effective result

#### `GetCloudDiscoveryReport_IncludesProviderLines`

File:

- `OsLib/OsLib.Tests/CloudStorageDiscoveryTests.cs`

What it tests:

- diagnostic output includes a OneDrive line

Expected behavior:

- report text contains `OneDrive`

Expected runtime:

- usually below 1 second

How to debug:

- inspect the returned report string

### 2. Agreement and Fallback Behavior Tests

These are also fast hermetic tests, but they are closer to documented behavior and fallback semantics.

#### `GetCloudStorageRoots_ProbesHomeOneDriveVariants_OnUnix`

File:

- `OsLib/OsLib.Tests/CloudStorageAgreementTests.cs`

What it tests:

- on Unix-like systems, OneDrive probe fallback recognizes home-directory variants like `~/OneDrive - Mzansi`

Expected behavior:

- `Os.GetCloudStorageRoot(CloudStorageType.OneDrive, refresh: true)` resolves to the created home-directory variant

Expected runtime:

- usually below 1 second

How to debug:

- step into `Os.GetCloudStorageRoot(...)`
- then into `ProbeOneDrive(...)`
- verify the home-directory variant enumeration is reached

#### `Backup_StripsConfiguredCloudRoot_FromBackupTargetPath`

File:

- `OsLib/OsLib.Tests/CloudStorageAgreementTests.cs`

OneDrive case:

- `CloudStorageType.OneDrive, "OneDriveRoot"`

What it tests:

- backup logic removes the configured OneDrive root prefix from the backup-relative `RaiPath`
- backup output goes into `localBackupDir`, not back into the cloud root

Expected behavior:

- backup relative path becomes `Work/Reports/`
- backup file exists under the local backup directory
- source file still exists

Expected runtime:

- usually below 1 second

How to debug:

- step through `RaiFile.GetBackupRelativeDirectoryPath(...)` and confirm it returns a `RaiPath`
- then through `source.backup(copy: true)`

### 3. Provider Path and Cloud-Flag Tests

These are the cleanest unit-style entry points if you want to understand OneDrive classification logic.

#### `GetCloudStorageRoot_UsesConfiguredRoot_ForEachProvider`

File:

- `OsLib/OsLib.Tests/CloudStorageProviderPathTests.cs`

OneDrive case:

- `CloudStorageType.OneDrive, "OneDriveRoot"`

What it tests:

- a configured OneDrive path is returned as the OneDrive root

Expected behavior:

- returned root equals the configured directory exactly

Expected runtime:

- usually below 1 second

How to debug:

- this is the best first breakpoint if you are debugging root resolution logic

#### `GetCloudStorageProviderForPath_ReturnsConfiguredProvider_ForEachProvider`

File:

- `OsLib/OsLib.Tests/CloudStorageProviderPathTests.cs`

OneDrive case:

- `CloudStorageType.OneDrive, "OneDriveRoot"`

What it tests:

- paths under the configured OneDrive root classify as OneDrive
- non-cloud paths remain unclassified

Expected behavior:

- provider root path returns `OneDrive`
- nested cloud path returns `OneDrive`
- unrelated local path returns `null`

Expected runtime:

- usually below 1 second

How to debug:

- step into `Os.GetCloudStorageProviderForPath(...)`
- inspect path normalization carefully

#### `RaiFile_CloudFlag_DetectsFilesUnderEachConfiguredProvider`

File:

- `OsLib/OsLib.Tests/CloudStorageProviderPathTests.cs`

OneDrive case:

- `CloudStorageType.OneDrive, "OneDriveRoot"`

What it tests:

- `RaiFile.Cloud` is `true` for files under the configured OneDrive tree
- `RaiFile.Cloud` is `false` for unrelated local files

Expected behavior:

- cloud file reports `Cloud == true`
- local file reports `Cloud == false`

Expected runtime:

- usually below 1 second

How to debug:

- this is the best entry point if the question is "why is this file being treated as cloud-backed?"

### 4. Machine-State Diagnostic Test

#### `MachineCloudState_PrintsDiscoveryInputs_AndProviderStatus_WithoutFailingForMissingRoots`

File:

- `OsLib/OsLib.Tests/CloudStorageMachineStateTests.cs`

What it tests:

- diagnostics run without failing just because a provider is absent
- output includes a OneDrive section

Expected behavior:

- report contains `OneDrive`
- the test remains informational rather than strict about actual availability

Expected runtime:

- usually below 1 second

How to debug:

- use this first if you are unsure what the current machine thinks OneDrive is
- inspect the console report before touching deeper tests

### 5. Real Local OneDrive Integration Tests

These are the first tests that depend on an actual writable OneDrive root on the current machine.

They skip when:

- OneDrive root is not configured or discoverable
- configured OneDrive root directory does not exist
- OneDrive root is not writable

#### `RaiFile_RoundTrip_WorksAgainstRealWritableCloudProvider`

File:

- `OsLib/OsLib.Tests/CloudStorageRealWorldIntegrationTests.cs`

OneDrive case:

- `CloudStorageType.OneDrive`

What it tests:

- create a file inside the real OneDrive root
- copy it
- move it
- delete the copied and moved files
- verify `RaiFile.Cloud` remains true for those files

Expected behavior:

- all local operations succeed inside the real OneDrive tree
- read-back content is preserved across copy and move
- deleted files are gone locally at the end

Expected runtime:

- usually around 1 to 5 seconds on a healthy local system
- can be slower if the cloud client is busy

Important note:

- this test is about local correctness inside a real OneDrive-managed directory
- it does not assert remote propagation

How to debug:

- step through `TryPrepareWritableIntegrationRoot(...)`
- inspect `providerRoot` and `root`
- then step through `sourceText.Save()`, `copy.cp(source)`, `moved.mv(source, ...)`, and the final deletes

#### `TextFile_SaveAndRead_WorksAgainstRealWritableCloudProvider`

File:

- `OsLib/OsLib.Tests/CloudStorageRealWorldIntegrationTests.cs`

OneDrive case:

- `CloudStorageType.OneDrive`

What it tests:

- `TextFile.Save()` and reload/read operations work inside the real OneDrive tree

Expected behavior:

- saved file is marked cloud-backed
- reloaded file is also cloud-backed
- lines round-trip exactly

Expected runtime:

- usually around 1 to 3 seconds

How to debug:

- this is the simplest real-provider OneDrive test in OsLib
- if this fails, debug here before remote tests

#### `Pit_SaveAndReload_WorksAgainstRealWritableCloudProvider`

File:

- `JsonPit/JsonPit.Tests/JsonPitRealWorldIntegrationTests.cs`

OneDrive case:

- `CloudStorageType.OneDrive`

What it tests:

- a real `JsonPit` can save into the OneDrive root and be reloaded correctly

Expected behavior:

- `pit.JsonFile.Cloud` is true
- pit JSON file exists
- reloaded item values match exactly

Expected runtime:

- usually around 1 to 5 seconds

How to debug:

- step through `pit.Save(force: true)`
- then inspect the JSON file physically created under the OneDrive tree
- then step through reloading via `new Pit(..., autoload: true, ...)`

### 6. Remote OneDrive Sync Tests

These are the highest-value existing OneDrive tests, but also the most environment-dependent.

They require:

1. a local writable OneDrive root
2. `remote-test-config.json` with observer `mzansi`
3. ssh connectivity to `rsb@Mzansi`
4. a valid remote OneDrive root for `Mzansi`
5. actual sync convergence between local and remote machines

Each create, update, and delete phase allows up to 2 minutes.

#### `TextFile_SyncsWithMzansi`

File:

- `OsLib/OsLib.Tests/CloudRemoteSyncTests.cs`

OneDrive case:

- `CloudStorageType.OneDrive`

What it tests:

- create a local text file under OneDrive
- wait for remote file appearance on `Mzansi`
- update content and wait for remote update visibility
- delete locally and wait for remote disappearance

Expected behavior:

- remote baseline directory first becomes absent after cleanup
- remote file eventually contains `alpha`
- remote file eventually changes to `gamma` and `delta`
- remote file no longer contains stale `alpha`
- remote file eventually disappears after delete

Expected timeframe:

- ideal case: a few seconds to tens of seconds per phase
- enforced timeout: 2 minutes for create, 2 minutes for update, 2 minutes for delete

How to debug:

- first inspect `Os.GetCloudConfigurationDiagnosticReport(refresh: true)`
- then inspect `Os.GetRemoteTestConfigurationDiagnosticReport(refresh: true)`
- step through `RemoteCloudSyncProbe.TryCreate(...)`
- step into `probe.Observer.WaitForFileContainingAll(...)` and `WaitForMissing(...)`
- if delete fails, inspect the thrown diagnostic payload showing remote path state and directory listing

#### `Pit_SyncsWithMzansi`

File:

- `JsonPit/JsonPit.Tests/CloudRemoteSyncTests.cs`

OneDrive case:

- `CloudStorageType.OneDrive`

What it tests:

- create a `JsonPit` under OneDrive
- wait for remote JSON visibility on `Mzansi`
- update the pit item and wait for remote JSON change
- delete the pit root and wait for remote directory disappearance

Expected behavior:

- remote JSON contains `CloudItem`, provider name, and `RAIkeep` after create
- remote JSON later contains updated values `84`, `UpdatedBy`, and `Nkosikasi`
- remote pit directory eventually disappears after local delete

Expected timeframe:

- ideal case: a few seconds to tens of seconds per phase
- enforced timeout: 2 minutes per propagation wait

Important note:

- this is directory-backed sync, not just single-file sync
- the delete phase expects disappearance of the remote pit root directory rather than only one file

How to debug:

- this is the best existing OneDrive test if your question is "does JsonPit actually converge remotely over OneDrive?"
- debug `pit.Save(force: true)` first, then `GetRelativePathForLocalFile(...)`, then remote waits

## Recommended Debug Order

If you are debugging OneDrive behavior from scratch, use this order:

1. `MachineCloudState_PrintsDiscoveryInputs_AndProviderStatus_WithoutFailingForMissingRoots`
2. `GetCloudStorageRoot_UsesConfiguredRoot_ForEachProvider`
3. `GetCloudStorageProviderForPath_ReturnsConfiguredProvider_ForEachProvider`
4. `RaiFile_CloudFlag_DetectsFilesUnderEachConfiguredProvider`
5. `TextFile_SaveAndRead_WorksAgainstRealWritableCloudProvider`
6. `Pit_SaveAndReload_WorksAgainstRealWritableCloudProvider`
7. `TextFile_SyncsWithMzansi`
8. `Pit_SyncsWithMzansi`

That sequence moves from pure classification logic to real local integration and finally to distributed sync behavior.

## Best First Breakpoints

If you only want a few breakpoints, use these:

### Classification problems

- `Os.GetCloudStorageRoot(...)`
- `Os.GetCloudStorageProviderForPath(...)`
- `RaiFile.Cloud`

### Real local provider problems

- `TryPrepareWritableIntegrationRoot(...)` in `CloudStorageRealWorldIntegrationTests`
- `pit.Save(force: true)` in `JsonPitRealWorldIntegrationTests`

### Remote sync problems

- `RemoteCloudSyncProbe.TryCreate(...)`
- `SshFileProbe.WaitForFileContainingAll(...)`
- `SshFileProbe.WaitForMissing(...)`

## Running Just the Relevant Tests

Examples:

```bash
dotnet test RAIkeep.slnx --filter FullyQualifiedName~CloudStorageProviderPathTests
dotnet test RAIkeep.slnx --filter FullyQualifiedName~CloudStorageRealWorldIntegrationTests
dotnet test RAIkeep.slnx --filter FullyQualifiedName~CloudRemoteSyncTests
dotnet test RAIkeep.slnx --filter FullyQualifiedName~JsonPitRealWorldIntegrationTests
```

Important note for theory tests:

- command-line filtering by method name usually runs all provider rows for that method
- for OneDrive-only stepping, use a conditional breakpoint like `provider == CloudStorageType.OneDrive`
- if VS Code Test Explorer surfaces theory rows individually, debug the OneDrive row directly there

## What To Expect When A Test Skips

### Real local provider tests skip when

- OneDrive root is missing from config and not discoverable
- configured OneDrive path does not exist
- OneDrive path is not writable

### Remote tests skip when

- local OneDrive root is missing or not writable
- `mzansi` is missing from `remote-test-config.json`
- ssh to `Mzansi` fails
- remote OneDrive root cannot be resolved or accessed

## Practical Summary

If you mostly want named entry points:

- simplest OneDrive unit-style test: `GetCloudStorageProviderForPath_ReturnsConfiguredProvider_ForEachProvider`
- simplest OneDrive real-provider test: `TextFile_SaveAndRead_WorksAgainstRealWritableCloudProvider`
- best OneDrive JsonPit local test: `Pit_SaveAndReload_WorksAgainstRealWritableCloudProvider`
- best OneDrive remote convergence test: `Pit_SyncsWithMzansi`

If something fails unexpectedly, start one layer lower than the failing test.

Example:

- if remote OneDrive sync fails, first prove local real OneDrive save works
- if local real OneDrive save fails, first prove OneDrive path classification and root resolution work