# Refactoring 2026-03-12 And 2026-03-13

This document summarizes the refactoring and cleanup work completed in the RAIkeep workspace on 2026-03-12 and 2026-03-13.

## Objectives Completed

- Established repo handoff context from the current workspace state.
- Repaired and normalized PlantUML diagrams across the solution.
- Refactored OsLib backup-directory handling to use an OS-aware local property instead of a hard-coded Unix-specific field.
- Hardened `RaiSystem` command execution and parsing for quoted executable paths.
- Migrated key external-process callers from flat command strings to structured executable-plus-arguments usage.
- Extracted `ImageMagick` from `ImageFile.cs` into its own source file and removed RaiImage's dependency on `Os.winInternal`.
- Introduced a reusable JSON-backed `ConfigFile<TData>` base in OsLib.
- Replaced the cloud-only config model with top-level `Os.Config` backed by `osconfig.json`.
- Moved configurable directory and cloud settings into a typed `OsConfigModel` with nested `CloudModel` state.
- Removed the custom `OSLIB_*` cloud and backup override model from the active OsLib design and migrated tests/docs to config-driven setup.
- Revalidated the full solution after the config refactor.

## Repo Context And Handoff

- Created `CURRENT-STATE.md` at the solution root to capture workspace state, solution structure, test baseline, and diagram conventions.
- Created and updated repo memory notes to preserve handoff context for future sessions.

## PlantUML Repairs And Conventions

### Naming And Header Cleanup

- Added explicit named `@startuml ...` headers to solution diagrams.
- Removed stray prose before `@startuml` where required.
- Standardized diagram naming to match diagram titles and improve plugin behavior.

### Diagram Files Updated

- `RAIkeep-Library-Dependencies.puml`
- `RAIkeep-Package-Dependencies.puml`
- `OsLib/Os-ClassDiagram.puml`
- `OsLib/RaiFile-Hierarchy.puml`
- `RaiImage/RaiImage-Hierarchy.puml`
- `RaiUtils/RaiUtils-ClassDiagram.puml`

### Rendering Fixes

- Fixed invalid clickable-class syntax in `RAIkeep-Library-Dependencies.puml`.
- Validated all `.puml` files locally after repair.
- Regenerated the affected SVG artifacts where needed.

## OsLib Refactoring

### Backup Directory Redesign

- Replaced the old hard-coded `Os.LocalBackupDirUnix` storage approach with a computed, OS-aware `Os.LocalBackupDir` property.
- Ensured the chosen backup directory is local and not cloud-replicated.
- Retained `LocalBackupDirUnix` as an obsolete compatibility alias pointing to `LocalBackupDir`.

### Reusable Configuration Architecture

- Added `OsLib/ConfigFile.cs` with a reusable `ConfigFile<TData> : RaiFile` abstraction for JSON-backed typed configuration.
- Added `OsConfigFile`, `OsConfigModel`, and `CloudModel` in `OsLib/Os.CloudStorage.cs`.
- Standardized the default config file name to `osconfig.json`.
- Standardized config lookup locations to:
  - `~/.config/RAIkeep/osconfig.json` on macOS and Linux
  - `%APPDATA%\RAIkeep\osconfig.json` on Windows
- Moved the following policy values into `Os.Config`:
  - `HomeDir`
  - `TempDir`
  - `LocalBackupDir`
  - `DefaultCloudOrder`
  - nested cloud roots for Dropbox, OneDrive, and Google Drive
- Preserved provider probing and effective cloud-root caching.
- Implemented lazy config initialization to avoid recursive static-constructor re-entry during path normalization and cloud detection.

### Cloud Configuration Redesign

- Replaced the older cloud-only typed config approach with a broader top-level `Os.Config` model.
- Kept convenience compatibility accessors such as `GooglePath` and `GetCloudDirPath(...)` on `OsConfigModel` to reduce migration churn.
- Kept `GetDefaultCloudConfigPath()` only as an obsolete compatibility alias to `GetDefaultConfigPath()`.
- Changed cloud discovery precedence to:
  1. explicit values in `Os.Config`
  2. OS/provider-specific probing
- Persisted discovered provider roots back into config only when the corresponding configured value is empty.

### API Cleanup

- Removed the leftover `NewSubscriberCommandWin` field from OsLib.
- Updated docs and diagrams to reflect the renamed backup property and API cleanup.

### RaiSystem Hardening

- Added robust parsing for quoted executable paths in `RaiSystem(string cmdLine)`.
- Improved constructor behavior for structured `RaiSystem(string cmd, string p)` usage.
- Added characterization tests for:
  - executable paths containing spaces
  - quoted executable paths in flat command-line mode
  - Windows `FileInfo` behavior with forward slashes

### Structured Process Invocation Migration

- Migrated `SysInfo` away from flat command strings toward structured executable-plus-arguments calls.
- Set the direction for external command execution ownership to remain in `RaiSystem` rather than `Os`.

## RaiImage Refactoring

### ImageMagick Extraction

- Removed the embedded `ImageMagick` implementation from `ImageFile.cs`.
- Added a standalone `RaiImage/ImageMagick.cs` file.
- Preserved the existing wrapper responsibilities while improving separation of concerns.

### winInternal Removal In RaiImage

- Removed the RaiImage-side dependency on `Os.winInternal`.
- Replaced the Windows retry-path file handling with normal path resolution inside `ImageMagick`.

### Recovery From Mid-Refactor Breakage

- Repaired a transient broken intermediate state in `ImageFile.cs` caused during extraction.
- Restored `ImageFile.cs` from committed structure and re-applied only the intended extraction delta.
- Revalidated both `ImageFile.cs` and `ImageMagick.cs` with clean diagnostics.

## Documentation And Diagram Updates

- Updated `OsLib/README.md` and `OsLib/API.md` for the backup-directory changes.
- Updated `OsLib/CLOUD_STORAGE_DISCOVERY.md` to document `Os.Config`, `osconfig.json`, nested cloud settings, cache behavior, and provider probing.
- Updated `JsonPit/GettingStarted.md` and `JsonPit/README.md` to reference `osconfig.json` instead of `OSLIB_CLOUD_ROOT_*` and `cloudstorage.json`.
- Updated `RaiUtils/README.md` and `RaiUtils/API.md` to reference the shared `osconfig.json` contract.
- Updated PlantUML diagrams to reflect current names and structure.
- Added this summary document to preserve the refactoring narrative in-repo.

## Test Migration And Validation

### Test Migration

- Added `OsLib/OsLib.Tests/OsTestEnvironment.cs` to isolate HOME, APPDATA, LOCALAPPDATA, and config-file setup for config-driven tests.
- Migrated OsLib cloud and environment-path tests away from custom `OSLIB_*` overrides and onto `osconfig.json`-backed setup.
- Updated `JsonPit/JsonPit.Tests/JsonPitTestEnvironment.cs` to configure the test cloud root through the new config file model.
- Updated `OsLib/OsLib.Tests/CloudStorageMachineStateTests.cs` to report the active config path rather than removed override variables.

### Validation Results

- Focused migration tests passed after the config refactor.
- Full solution validation passed after the config refactor.
- Latest solution result:
  - `dotnet test RAIkeep.slnx --nologo -v minimal`
  - `144` tests passed, `0` failed.

## Test And Validation Results

Validation completed successfully after the refactoring work.

### Targeted Validation

- OsLib focused tests passed.
- RaiImage focused tests passed.
- RaiImage source diagnostics were clean after extraction.
- No remaining `Os.winInternal` references were found in RaiImage.

### Full Solution Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- Result: 95 tests passed, 0 failed, 0 skipped.

### Updated Full Solution Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- Result after the reusable config refactor: 144 tests passed, 0 failed.

## Files Added Today

- `CURRENT-STATE.md`
- `Refactoring20260312.md`
- `OsLib/Os-ClassDiagram.puml`
- `OsLib/Os-ClassDiagram.svg`
- `RaiImage/ImageMagick.cs`

## Summary

The main technical outcomes from today were:

- command execution was made safer and more structured
- backup-path behavior in OsLib was made more portable and correct
- generated diagrams were repaired and standardized
- RaiImage command-wrapper responsibilities were separated more cleanly
- OsLib now has a reusable typed configuration layer centered on `Os.Config`
- cloud and backup configuration moved from ad hoc overrides into `osconfig.json`
- OsLib, JsonPit, and RaiUtils documentation now describe the same shared config contract
- the solution finished in a green, fully tested state