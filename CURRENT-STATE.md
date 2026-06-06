# CURRENT-STATE

This file captures the current working state of the `RAIkeep` umbrella workspace so a future session can resume quickly.

Current note for `3.8.12`:

- the active OsLib config contract is `RAIkeep.json5`
- `Os.Config` is lazy and dynamic
- `CloudPathWiring` plus `RaiPath.CloudEvaluator` drive buffered cloud state
- directory waits live in `RaiPath`, file waits live in `RaiFile`
- `RaiFile.BackdateCreationTime(...)` now supports deterministic `FileAge` manipulation with configurable sync propagation delay
- live markdown and PlantUML release markers were refreshed for the `3.8.12` package line
- older remote-observer and `osconfig.json` references in historical notes should not be treated as the current OsLib public surface

## Role of this repo

`RAIkeep` is the umbrella workspace for the related C# libraries:

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`

The intent is to keep package repos independent while using `RAIkeep` as the cross-library integration workspace.

## Latest umbrella validation

Most recent command:

```bash
dotnet test RAIkeep.slnx --nologo -v minimal
```

Most recent result:

- total: 244
- failed: 0
- succeeded: 243
- skipped: 1

Earlier remote SSH and remote cloud-sync notes in this file refer to an older harness setup and should be treated as historical unless revalidated.

## Earlier verified baseline

The umbrella solution baseline was verified successfully.

Command:

```bash
dotnet test RAIkeep.slnx
```

Verified result at the time of this note:

- total: 149
- failed: 0
- succeeded: 144
- skipped: 5

In addition, later focused validation around the recent cloud-test restructuring passed for the affected OsLib cloud test set.

Focused result at the time of this note:

- targeted cloud test batch: 27 passed
- failed: 0

## Current aligned package version

The workspace is aligned on version `3.8.12` for:

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`
- `PitSeeder`

## 3.8.12 documentation decisions

- Current docs are being aligned to the post-purge OsLib architecture.
- Historical release/design notes remain useful context but no longer define the live OsLib API surface.
- Active package diagrams now carry the `3.8.12` release marker so current diagrams are easy to distinguish from historical design artifacts.

## Solution structure

`RAIkeep.slnx` includes:

- `JsonPit/JsonPit.csproj`
- `JsonPit/JsonPit.Tests/JsonPit.Tests.csproj`
- `OsLib/OsLib.csproj`
- `OsLib/OsLib.Tests/OsLib.Tests.csproj`
- `RaiUtils/RaiUtils.csproj`
- `RaiUtils/tests/RaiUtils.Tests/RaiUtils.Tests.csproj`
- `RaiImage/RaiImage.csproj`
- `RaiImage/RaiImage.Tests/RaiImage.Tests.csproj`

The missing OsLib and RaiUtils test projects were added to the umbrella solution during this session.

## JsonPit.Tests sunset

Decision:

- package-owned JsonPit tests now live in the `JsonPit` repo
- the separate `JsonPit.Tests` repository is being sunset and archived

Status:

- the standalone `JsonPit.Tests` README was updated with an archival notice
- the archival notice points to `JsonPit` for package tests and `RAIkeep` for integration work

Recommended GitHub sequence:

1. Commit and push the archival README change in `JsonPit.Tests`
2. Archive the `JsonPit.Tests` GitHub repository
3. Keep it archived for historical reference instead of deleting it immediately

## Rename direction

Decision:

- the parent umbrella repo is intended to be `RAIkeep`
- renaming from `JsonPitSolution` to `RAIkeep` makes architectural sense now that the repo truly acts as the umbrella workspace

Recommended sequence:

1. Push child repo changes first if submodule SHAs changed
2. Push the umbrella repo changes last
3. Rename the GitHub repo from `JsonPitSolution` to `RAIkeep`
4. Update local `origin` URL after the rename

## PlantUML artifacts added or updated

At the `RAIkeep` root:

- `RAIkeep-Package-Dependencies.puml`
- `RAIkeep-Library-Dependencies.puml`

Under `OsLib`:

- `Os-ClassDiagram.puml`

At the `RAIkeep` root:

- `MANIFESTO.md`

## Current cloud-test state

The OsLib cloud-related tests were recently split into two honest layers.

Real cloud tests now target actual provider-backed roots on the machine that runs the tests:

- `OsLib/OsLib.Tests/CloudStorageDiscoveryTests.cs`
- `OsLib/OsLib.Tests/CloudStorageAgreementTests.cs`
- `OsLib/OsLib.Tests/CloudStorageProviderPathTests.cs`
- `OsLib/OsLib.Tests/CloudStorageRealWorldIntegrationTests.cs`

Mechanics-oriented tests now hold the sandboxed/config/probe logic:

- `OsLib/OsLib.Tests/CloudStorageConfigMechanicsTests.cs`
- `OsLib/OsLib.Tests/CloudStorageAgreementMechanicsTests.cs`
- `OsLib/OsLib.Tests/CloudStoragePathMechanicsTests.cs`

Supporting helper:

- `OsLib/OsLib.Tests/CloudStorageRealTestEnvironment.cs`

Remote environment-backed tests that are now active and passing:

- `OsLib/OsLib.Tests/CloudRemoteSyncTests.cs`
- `JsonPit/JsonPit.Tests/CloudRemoteSyncTests.cs`
- `OsLib/OsLib.Tests/RemoteSshTests.cs`

This means the naming is now much closer to reality than before: sandboxed tests no longer present themselves as real cloud-provider tests.

## Current release state

The `3.8.12` release-alignment work is the current umbrella baseline.

Key current facts:

- package versions are aligned to `3.8.12`
- OsLib path/config/logging semantics were refactored and documented
- OsLib now exposes `RaiFile.BackdateCreationTime(...)` and `SyncPropagationDelayMs` configuration for remote-sync timing control
- release-note files were added or updated across the package repos
- active PlantUML headers were refreshed across the umbrella and child-package diagrams
- the remote `mzansi` test setup is now valid enough for the remote SSH and cloud-sync tests to execute successfully
- the latest umbrella solution validation is green with 243 passed and 1 skipped
- package pack validation is partial: OsLibCore and RaiUtils packages were created locally, while solution-level and remaining package pack attempts exited without useful diagnostics before creating packages

The fire-and-forget release sequence is complete once the child commits, submodule pointers, rendered diagrams, root docs, and GitHub Sequential NuGet Release Chain dispatch with `publish_to_nuget=true` have completed.

## PlantUML conventions established in this session

For package layout:

- hidden `right` links are useful for defining columns
- hidden `down` links are useful for defining rows
- `..[norank]>` helps keep visible dependency arrows from dominating layout

For built-in UML icons:

- `show circle` restores class and enum header icons
- `hide circle` removes those header icons
- `classAttributeIconSize` controls the visibility size of member glyphs

For static members:

- explicit `Ⓢ` markers work well in class diagrams

For package/member text diagrams:

- `Ⓒ` was used for production-class markers
- `Ⓣ` was used for test-class markers

## Important files

- `RAIkeep.slnx`
- `README.md`
- `MANIFESTO.md`
- `.gitmodules`
- `RAIkeep-Package-Dependencies.puml`
- `RAIkeep-Library-Dependencies.puml`
- `OsLib/Os-ClassDiagram.puml`
- `CURRENT-STATE.md`

## Suggested prompt for a future session

```text
Please read CURRENT-STATE.md in the RAIkeep repo root first, then continue from there.
```
