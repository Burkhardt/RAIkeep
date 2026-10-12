# OsLib Release Notes 3.x

## 3.13.2

**Date:** 2026-08-05  
**Author / Delivering Agent:** RAIkeep Dev Agent  
**Delivered Version:** v3.13.2  
**Target Consumers:** JsonPit, PitSeeder, AIA, AfricaStage  
**Status:** Implemented — coordinated 3.13.2 line; NuGet publication pending release authorization

---

### 1. Summary

OsLib supplies the shared filesystem primitives required by the coordinated JsonPit
concurrency contract: a no-delete/no-rename `TextFile.Save`, deterministic canonical
JSON with SHA-256 hashing, and generic create-once event files with stateless
directory aggregation. OsLib owns storage mechanics only; it imposes no event-content
schema and never interprets JsonPit fields.

### 2. Resolved Change Requests (CRs)

- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) — OsLib share of the coordinated v3.13.2 concurrency work (agreed `TextFile.Save` contract, canonical JSON, `EventFile`/`EventDirectory`).

### 3. Root Cause Analysis & Technical Resolution

- **`TextFile.Save` deleted the original pathname before rewriting.** `Save(backup: false)`
  previously called `rm()` and recreated the file, so a concurrent reader in another
  process could observe the pathname disappearing — one root cause of transient
  read failures on cloud-synced pits. `Save(backup: false)` now creates the pathname
  when absent or truncates and writes the existing pathname directly in place. It
  never deletes, renames, or uses temporary-file replacement.
- **`Save(backup: true)` moved the original to the backup location.** It now *copies*
  the previous content to the configured backup location before overwriting the
  original in place, so the original pathname never disappears. Existing
  materialization checks remain in both paths. `SaveInPlace()` is retained for
  patch-release source/binary compatibility and delegates to `Save(backup: false)`.
- In-place writing is deliberately **not** described as atomic reader visibility;
  JsonPit's validated candidate-load and bounded-retry behavior prevents incomplete
  content from becoming live state.

### 4. Public Contract & API / Package Changes

- `TextFile.Save(bool backup = false)` — no-delete/no-rename contract (behavioral change, same signature).
- `TextFile.SaveInPlace()` — compatibility alias delegating to `Save(backup: false)`.
- **New** `CanonicalJson` — `Canonicalize(JToken)`, `Sha256Hex(string)`, `CanonicalizeWithHash(JToken)`:
  recursive ordinal property ordering, preserved array order, compact invariant JSON,
  full lowercase SHA-256 of the UTF-8 canonical content.
- **New** `EventFile : TextFile` — one immutable canonical-JSON event written by the
  constructor (create-once): `{LogicalStem}_{Sha256}.event` under
  `rootPath / EventDirectory.Name`. Same stem + same canonical content is an
  idempotent success; same stem + different content resolves to a different
  hash-derived path; a different-content hash-path collision preserves the existing
  artifact and writes a nonce-suffixed sibling without interrupting the audited
  operation. Accepts a `JObject` or a dynamic object serializing to one top-level
  JSON object; exact file bytes are the canonical UTF-8 content without a trailing
  line terminator.
- **New** static `EventDirectory` — `public const string Name = "Events"`;
  `Events(RaiPath rootPath)` returns a fresh `Dictionary<string, JObject>` on every
  call (complete filename → unchanged parsed object), never creates the missing
  directory, and individually omits incomplete/unparseable/hash-invalid files.
- No breaking API changes; `Save(backup: true)` semantics changed from move-based to
  copy-based backup (the original path now always remains present).

### 5. Validation & Acceptance Evidence

- `OsLib.Tests`: 80 passed, 0 failed, 0 skipped (includes the new
  `TextFileSaveContractTests` and `EventFileTests`).
- Configured-cloud evidence (machine Nkosikazi, provider OneDrive under
  `Os.Config.Cloud`): a `FileSystemWatcher` observed 50 repeated in-place `Save`
  calls on a OneDrive-synced file — zero delete and zero rename events while the
  pathname remained continuously discoverable; copy-based backup verified against
  the configured `LocalBackupDir`.
- Event mechanics verified on the configured cloud root: constructor-write,
  idempotent republication, hash-derived divergence, nonce collision handling,
  fresh schema-agnostic aggregation, and individual omission plus later
  reconsideration of incomplete/hash-invalid files.

### 6. Upgrade & Consumption Instructions

- Consume `OsLibCore 3.13.2`. No call-site changes are required.
- Callers that relied on `Save(backup: true)` *moving* the previous file must note it
  now copies; the original pathname always survives a save.
- Durable audit producers: construct `new EventFile(rootPath, logicalStem, contentObject)` —
  the constructor performs the create-once write. Consumers read via
  `EventDirectory.Events(rootPath)`.

---

## 3.13.1

### Summary

`OsLibCore 3.13.1` adds the file primitives required by JsonPit coordination files while preserving the existing path and cloud-configuration model.

### Changes

- Added `TextFile.SaveInPlace()` for small coordination files that must be updated without a preceding delete or rename.
- Retained `AwaitMaterializing(...)` after an in-place write so cloud-backed callers keep the existing materialization check.
- Added the read-only `RaiFile.LastWriteTimeUtc` property for consumers that need physical file modification time without direct `System.IO.FileInfo` access.
- Did not add a last-write-time setter. Physical modification time remains the real filesystem/cloud write time; callers should keep logical timestamps in their own data model.
- Updated API documentation, README entries, package metadata, and the RaiFile hierarchy diagram for `3.13.1`.

### Compatibility

- The new APIs are additive.
- No configuration-loading or environment-variable behavior changed.
- Existing `TextFile.Save(...)`, backup, and cloud-path behavior remain available unchanged.

### Validation

- Umbrella `RAIkeep.slnx` build succeeds.
- `OsLib.Tests`: `66` passed, `0` failed.

### Release sequencing

`OsLibCore` is first in the coordinated release chain. Do not begin the `RaiUtils` release until the OsLibCore publish workflow succeeds, the `3.13.1` flat-container package returns HTTP `200`, and the required `330`-second hold has completed.

---

## 3.12.1

### Summary

- Releases `OsLibCore` version `3.12.1`.
- Carries forward the coordinated `RAIkeep` package line with refreshed package metadata, README links, and diagram release markers.
- No public API changes from `3.12.0`.

### Validation

- `dotnet test OsLib.Tests/OsLib.Tests.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.12.0

### Summary

- Releases `OsLibCore` version `3.12.0`.
- Carries forward the coordinated `RAIkeep` package line with refreshed package metadata, README links, and diagram release markers.
- No public API changes from `3.11.5`.

### Validation

- `dotnet test OsLib.Tests/OsLib.Tests.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.4

### Summary

- Releases `OsLibCore` version `3.11.4`.
- Carries forward the coordinated `RAIkeep` package line with refreshed package metadata, README links, and diagram release markers.
- No public API changes from `3.11.3`.

### Validation

- `dotnet build OsLib.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.2

### Summary

- Releases `OsLibCore` version `3.11.2`.
- Carries forward the coordinated `RAIkeep` package line with refreshed package metadata, README links, and diagram release markers.
- No public API changes from `3.11.1`.

### Validation

- `dotnet build OsLib.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.1

### Summary

- Releases `OsLibCore` version `3.11.1`.
- Carries forward the coordinated `RAIkeep` package line with refreshed package metadata, README links, and diagram release markers.
- No public API changes from `3.11.0`.

### Validation

- `dotnet build OsLib.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.0

### Summary

- Releases `OsLibCore` version `3.11.0`.
- Carries forward the coordinated `RAIkeep` package line with refreshed package metadata, README links, and diagram release markers.
- No public API changes from `3.10.2`.

### Validation

- `dotnet build OsLib.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.2

### Summary

- Releases `OsLibCore` version `3.10.2`.
- Includes cloud-path wiring refinements with matching docs/diagram refreshes.
- Updates path-convention test coverage around current cloud-path behavior.

### Validation

- `dotnet build OsLib.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.1

### Summary

- Releases `OsLibCore` version `3.10.1`.
- Carries forward the coordinated `3.10.0` package baseline with refreshed current docs and PlantUML release markers.
- No public API changes from `3.10.0`.

### Validation

- `dotnet build OsLib.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.0

### Summary

- Releases `OsLibCore` version `3.10.0`.
- Refreshes package metadata, markdown docs, and PlantUML release markers for the coordinated minor line.
- No public API changes from `3.9.1`.

### Validation

- `dotnet build OsLib.csproj --nologo -v minimal`
- NuGet publishing remains wired through the tag-triggered `publish-nuget.yml` workflow.

---

## 3.9.1

### Summary

- Releases `OsLibCore` version `3.9.1`.
- Refreshes package metadata, markdown docs, and PlantUML release markers for the coordinated patch line.
- No public API changes from `3.9.0`.

### Validation

- `dotnet build OsLib.csproj --nologo -v minimal`
- NuGet publishing is handled by the tag-triggered `publish-nuget.yml` workflow.

---

## 3.9.0

### Summary

- Releases `OsLibCore` version `3.9.0`.
- Aligns package metadata, markdown docs, and PlantUML release markers for the coordinated minor line.
- No public API changes from `3.8.15`.

### Validation

- `dotnet build OsLib.csproj --nologo -v minimal`
- NuGet publishing is handled by the tag-triggered `publish-nuget.yml` workflow.

---

## 3.8.15

### Summary

- Releases `OsLibCore` version `3.8.15`.
- Aligns package metadata, markdown docs, and PlantUML release markers for the coordinated release chain.
- No public API changes from `3.8.14`.

### Validation

- `dotnet build OsLib.csproj --nologo -v minimal`
- NuGet publishing is handled by the tag-triggered `publish-nuget.yml` workflow.

---

## 3.8.14

### Summary

- Releases `OsLibCore` version `3.8.14`.
- Aligns package metadata, markdown docs, and PlantUML release markers for the coordinated release chain.
- No public API changes from `3.8.13`.

### Validation

- `dotnet build OsLib.csproj --nologo -v minimal`
- NuGet publishing is handled by the tag-triggered `publish-nuget.yml` workflow.

---

## 3.8.12

### Summary

- Releases `OsLibCore` version `3.8.12`.
- Aligns package metadata, live README links, and PlantUML release markers with the coordinated `RAIkeep` patch line.
- No public API or behavior changes from `3.8.11`.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`: 243 passed, 0 failed, 1 skipped.
- NuGet publishing and tag-triggered release workflows were intentionally not run.

---

## 3.8.11

### Summary

- Releases `OsLibCore` version `3.8.11`.
- Fixes `RaiFile`'s new-file completion check to compare UTC timestamps consistently.
- Refreshes live markdown release-line references and tracked PlantUML release markers for the `3.8.11` line.

### Validation

- Release published through GitHub Actions tag workflow.
- NuGet visibility is verified in the sequential release chain.

---

## 3.8.6

### Summary

- Coordinated release for `OsLibCore` version `3.8.6`.
- Refreshes markdown release-line references (including `README.md`) via automated scan.
- Refreshes all tracked PlantUML (`.puml`) release/version markers found in scope.

### Validation

- Release published through GitHub Actions tag workflow.
- NuGet visibility is verified in the sequential release chain.

---

## 3.8.1

### Summary

- Makes `RaiFile.mkdir()` virtual so base-class methods use standard polymorphic dispatch for derived file types.
- Preserves the existing `RaiFile.mkdir()` implementation logic.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- Result: 223 passed, 0 failed, 0 skipped.

---

## 3.8.0

### Summary

- Coordinated release for `OsLibCore` version `3.8.0`.
- Carries forward the async `RaiFile` APIs introduced in `3.7.10`.
- Refreshes current OsLib docs, release pointers, and PlantUML source headers for the `3.8.0` package line.

### API Status

- No new OsLib API changes relative to `3.7.11`.
- Public API continues to include:
  - `Task WriteFromAsync(Stream source, CancellationToken ct = default)`
  - `Task<byte[]> ReadAllBytesAsync(CancellationToken ct = default)`
  - `void BackdateCreationTime(DateTime utc, int? propagationDelayMs = null)`

### Documentation

- Updated `README.md`, `API.md`, `CLOUD_STORAGE_DISCOVERY.md`, and `ARCHITECTURE-ALIGNMENT.md` for the `3.8.0` package line.
- Refreshed the active PlantUML sources `Os-ClassDiagram.puml`, `Os-verboseCD.puml`, and `RaiFile-Hierarchy.puml` so current diagrams are labeled consistently with the live release.

### Validation

- `dotnet test OsLib/OsLib.Tests/OsLib.Tests.csproj --nologo -v minimal`
- Result: 64 passed, 0 failed, 0 skipped.

---

## 3.7.11

### Summary

- Patch release for `OsLibCore` version `3.7.11`.
- Carries forward the async `RaiFile` APIs introduced in `3.7.10`.
- Refreshes the packaged README and release-facing metadata so NuGet shows the current OsLib feature line.

### Package README Refresh

- Updated the packaged `README.md` from the stale `3.7.9` summary to the current release line.
- Added `RaiFile.WriteFromAsync(Stream, CancellationToken)` and `RaiFile.ReadAllBytesAsync(CancellationToken)` to the README API summary.
- Updated the README release-notes pointer and example release tag to the current patch line.

### API Status

- No code changes relative to `3.7.10`.
- Public API remains:
  - `Task WriteFromAsync(Stream source, CancellationToken ct = default)`
  - `Task<byte[]> ReadAllBytesAsync(CancellationToken ct = default)`

### Validation

- `dotnet pack OsLib/OsLib.csproj --nologo -v minimal`
- Result: package builds successfully with the refreshed README and `3.7.11` metadata.

---

## 3.7.10

### Summary

- Patch release for `OsLibCore` version `3.7.10`.
- Adds two async `RaiFile` APIs for stream-based writes and byte-array reads.
- Preserves existing `RaiFile` path resolution, trailing slash handling, and filename normalization behavior.

### New API

- `Task WriteFromAsync(Stream source, CancellationToken ct = default)`
  - Ensures the target directory exists using the existing `mkdir()` flow.
  - Creates or overwrites the target file and copies the source stream asynchronously.
- `Task<byte[]> ReadAllBytesAsync(CancellationToken ct = default)`
  - Reads the full file contents asynchronously via `System.IO.File.ReadAllBytesAsync`.

### Tests

- Added `RaiFile_WriteFromAsync_WritesStreamToDisk`.
- Added `RaiFile_ReadAllBytesAsync_ReturnsFileContents`.

### Validation

- `dotnet test OsLib/OsLib.Tests/OsLib.Tests.csproj --nologo -v minimal`
- Result: 64 passed, 0 failed, 0 skipped.

---

## 3.7.9

### Summary

- Patch release for `OsLibCore` version `3.7.9`.
- Carries forward the `3.7.8` RaiPath filesystem fixes.
- Refreshes current release docs, package metadata, and active PlantUML headers for the live package line.

### Documentation

- Updated `README.md`, `API.md`, `CLOUD_STORAGE_DISCOVERY.md`, and `ARCHITECTURE-ALIGNMENT.md` to the `3.7.9` package line.
- Refreshed the active OsLib PlantUML headers so current diagrams are labeled consistently with the live release.

### Validation

- `dotnet test OsLib.slnx --nologo -v minimal`
- Result: 62 passed, 0 failed, 0 skipped.

---

## 3.7.8

### Summary

- Patch release for `OsLibCore` version `3.7.8`.
- Focused on directory-level filesystem operations in `RaiPath`: `mv()`, `cp()`, and a new `backup()` method symmetrical to `RaiFile.backup`.
- No public API removals; signature additions only (`cp` gains an optional `keepBackup` parameter, new `RaiPath.backup` method).

### Bug Fixes — `RaiPath.mv()`

- Fixed `replace: true, keepBackup: false`: the prior implementation called `Directory.Move` over an existing target without first removing it, causing `IOException("Cannot create '<target>/' because a file or directory with the same name already exists.")`.
- Fixed `replace: true, keepBackup: true`: the prior implementation composed the backup name as `Path + "_backup_" + id`. Because `RaiPath.Path` always carries a trailing directory separator, the resulting path was a *child* of the target rather than a *sibling*, so `Directory.Move` failed with `IOException("Invalid argument")`.

### Behavior Changes — Backup Semantics

- `RaiPath.mv()` and `RaiPath.cp()` no longer create ad-hoc `_backup_<id>` siblings.
- When `keepBackup: true`, both methods now delegate to the new `RaiPath.backup()` method, which mirrors the source path under `Os.LocalBackupDir` and appends a UTC timestamp (`Os.DATEFORMAT`) to the leaf segment — symmetrical to `RaiFile.backup`.

### New API

- `RaiPath RaiPath.backup(bool copy = false)` — moves (or copies) the directory tree into `Os.LocalBackupDir`, mirroring the original absolute path under that root and appending a UTC timestamp to the leaf. Returns the resulting backup path, or `null` if the source does not exist. Throws `InvalidOperationException` when `Os.LocalBackupDir` is not configured.
- `RaiPath.cp(RaiPath from, bool replace, bool keepBackup = false)` — added optional `keepBackup` parameter for symmetry with `mv()`.

### Implementation Notes — `RaiPath.cp()`

- Reimplemented to traverse purely via `RaiPath.EnumerateFiles`, `RaiPath.EnumerateDirectories`, `RaiPath.mkdir()`, and `RaiFile.cp()` — no direct `System.IO` calls in the recursion. This removes the dependency on the previously-missing `CopyDirectory` helper.

### Tests

- Added six `RaiPath_Mv_*` tests in `OsLib.Tests/PathConventionsTests.cs` covering: move into empty target, throw on existing target without `replace`, replace without backup, replace with backup (verifies the backup landing point under `Os.LocalBackupDir`), missing source, and null source.
- The keep-backup test cleans up the mirrored backup subtree after the assertion.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- Result: all OsLib.Tests pass (62/62 in the OsLib.Tests project; full solution suite green).

---

## 3.7.7

### Summary

- Patch release for `OsLibCore` version `3.7.7`.
- Keeps the current `RAIkeep.json5`, `CloudPathWiring`, and sync-propagation contract unchanged.
- Refreshes the live docs and PlantUML diagrams so the current release surface matches the current codebase state.

### Documentation And Diagram Updates

- Refreshed `README.md`, `API.md`, `CLOUD_STORAGE_DISCOVERY.md`, and `ARCHITECTURE-ALIGNMENT.md` for the `3.7.7` package line.
- Updated active umbrella and OsLib PlantUML headers to `3.7.7` so current diagrams are distinct from historical artifacts.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- Result: 214 passed, 0 failed, 0 skipped.

---

## 3.7.6

### Summary

- Adds `RaiFile.BackdateCreationTime(...)` for deterministic file-age manipulation in cloud-sync scenarios.
- Adds `RaiFile.DefaultSyncPropagationDelayMs` as a static override point for metadata propagation waits.
- Supports `SyncPropagationDelayMs` in `RAIkeep.json5` so machines can tune the default delay without recompilation.

### API Additions

- `RaiFile.FileAge` continues to measure age from `CreationTimeUtc`.
- `RaiFile.BackdateCreationTime(DateTime utc, int? propagationDelayMs = null)` now:
  - sets `CreationTimeUtc`
  - writes a best-effort `{name}.backdate.tmp` sentinel next to the file
  - waits using explicit parameter, then `Os.Config.SyncPropagationDelayMs`, then `RaiFile.DefaultSyncPropagationDelayMs`
  - removes the sentinel after the delay
- `RaiFile.DefaultSyncPropagationDelayMs` defaults to `10_000` milliseconds and is settable in-process.

### Configuration

- Current config naming in code is `RAIkeep.json5`.
- `SyncPropagationDelayMs` is optional and can be tuned per machine.
- This is especially useful when sync latency differs between native OneDrive and rclone/Google Drive setups.

### Documentation And Diagram Updates

- Refreshed `README.md`, `API.md`, and `CLOUD_STORAGE_DISCOVERY.md` to document the new backdate helper and delay configuration.
- Updated OsLib class diagrams that surface `RaiFile` methods to include the new API.

### Validation

- `dotnet test OsLib/OsLib.Tests/OsLib.Tests.csproj --configuration Release --nologo -v minimal`
- Result: 56 passed, 0 failed.

---

## 3.7.5

### Summary

- Documentation and diagram alignment release for the current OsLib architecture.
- Clarifies the live `osconfig.json5` contract and removes outdated guidance that still described removed cloud-selection and observer APIs as current.
- Captures the current cloud-path model around `CloudPathWiring`, `RaiPath.CloudEvaluator`, and buffered `RaiPath.Cloud`.

### Documentation Changes

- Refreshed current OsLib docs: `README.md`, `API.md`, and `CLOUD_STORAGE_DISCOVERY.md`.
- Marked older design and test setup notes as historical where they still describe superseded API shapes.
- Updated cross-package guidance in JsonPit and RaiUtils to the current `osconfig.json5` / `Cloud.*` contract.
- Updated `CURRENT-STATE.md` and `CURRENT-STATUS.md` so they no longer advertise `CloudStorageRootDir` and public `LoadConfig(...)` as current OsLib behavior.

### Diagram Changes

- Updated `Os-ClassDiagram.puml` and `Os-verboseCD.puml` release markers to `3.7.5`.
- Kept touched PlantUML files on the `Os-verboseCD` visual style baseline.

### Architecture Notes

- `Os.Config` remains lazy, internal-load, and `dynamic`.
- `UserHomeDir` and `AppRootDir` remain intrinsic runtime values.
- `TempDir` and `LocalBackupDir` remain config-driven.
- Directory wait logic belongs to `RaiPath`.
- File wait logic belongs to `RaiFile`.

### Validation

- The latest directly verified command in this workspace state is:

```bash
dotnet test OsLib/OsLib.Tests/OsLib.Tests.csproj --nologo -v minimal
```

- Result: 50 passed, 0 failed.

---

## 3.7.3

### Summary

- Patch release for `OsLibCore` version `3.7.3`.
- Includes path-handling and release-alignment updates for the 3.7.3 line.

### Breaking Change Warning

- This is a breaking change for positional constructor calls.
- `TextFile(RaiPath path, string name, string ext = "txt", string content = null)` interprets the third positional string argument as `ext`, not `content`.
- `Script(RaiPath path, string name, string ext = "sh", string content = null)` follows the same parameter order, so the third positional string is also interpreted as `ext`.
- Previous positional usage that passed content as the third argument is now parsed as file extension and will not work as intended.

```csharp
new TextFile(new RaiPath("~"), "test.txt", "First line of textfile")
```

```csharp
new Script(new RaiPath("~"), "deploy.sh", "#!/bin/sh\necho ok")
```

- Use a named argument for content instead:

```csharp
new TextFile(new RaiPath("~"), "test.txt", content: "First line of textfile")
```

```csharp
new Script(new RaiPath("~"), "deploy.sh", content: "#!/bin/sh\necho ok")
```

### Notes

- Keep release order: publish `OsLibCore` before downstream packages (`RaiUtils`, `RaiImage`, `JsonPit`).

---

## 3.7.2

### Highlights

- Includes the RaiPath bug fix from commit `RaiPath fix`.
- Bumps `OsLibCore` package version to `3.7.2`.
- Updates release metadata and README release references for the 3.7.2 line.

### Notes

- Keep release order: publish `OsLibCore` before downstream packages (`RaiUtils`, `RaiImage`, `JsonPit`).

---

## 3.7.1

### Summary

- Patch release to restore NuGet publishing after solution migration from `.sln` to `.slnx`.
- Updates GitHub Actions publish workflow restore/build steps to use `OsLib.slnx`.
- Keeps package API and runtime behavior unchanged from `3.7.0`.

### Package

- NuGet package version: `3.7.1`
- Package id: `OsLibCore`

### Compatibility

- Backward compatible with `3.7.0` consumers.

---

## 3.7.0

### Summary

- Minor release focused on path/canonicalization alignment with current JsonPit integration workflows.
- Improves consistency of pit-directory and change-directory path handling across cloud-backed scenarios.
- No breaking API changes for existing OsLib consumers.

### Package

- NuGet package version: `3.7.0`
- Package id: `OsLibCore`

### Compatibility

- Backward compatible with `3.6.x` API usage.
- Existing `RaiPath`, `RaiFile`, and canonical path conventions remain supported.

---

## 3.6.1

### Highlights

- Patch release following `3.6.0`.
- Corrects the NuGet publish order: OsLibCore is now published first so downstream packages (`RaiUtils`, `RaiImage`, `JsonPit`) can resolve their fallback `PackageReference` against a live NuGet version.
- No API or behavioral changes beyond `3.6.0`.

### Validation

- All `OsLib.Tests` pass green with this release.

---

## 3.6.0

### Highlights

- `CanonicalFile` constructor crash fixed: eliminated infinite recursion in the `Name` getter and setter overrides.
- `CanonicalFile` constructor is now safe when called with directory-style paths (trailing `/`).
- `PathConventionsTests` updated with new constructor tests covering the `RaiPath` and string overloads for real-world cloud-storage paths.
- Aligns the `OsLib` package version with the shared `3.6.0` `RAIkeep` package line.

### Bug Fix: CanonicalFile recursion

The `Name` getter in `CanonicalFile` checked `string.IsNullOrEmpty(Name)`, which called itself
recursively and caused a `StackOverflowException` on .NET (a process-terminating crash/core dump).
The setter contained a symmetric problem.  Both are resolved by routing internal reads through `base.Name`.

The constructor also crashed when passed a directory-style path (trailing `/`) because
`new RaiFile(fullName).NameWithExtension` returns an empty string in that case, and the
subsequent canonicalization then called `Name` before it had been initialised.

### Tests Adjusted

- `CanonicalFile_StringConstructor_WithNomsaNetDirectoryPath_PreservesDirectoryPath`
- `CanonicalFile_RaiPathConstructor_WithNomsaNetDirectoryPathAndName_KeepsCanonicalByStem`

Both tests exercise the previously crashing constructor paths with the
`/Users/RSB/Library/CloudStorage/OneDrive/OneDriveData/Nomsa.net/` path family.

### Validation

- All `OsLib.Tests` pass green with this release.

---

## 3.5.3

### Highlights

- Documentation patch release for the OsLib package surface.
- Advances the published documentation line from `3.5.2` to `3.5.3`.
- Documents `CanonicalPath` as deprecated legacy API surface and directs new usage toward `RaiPath` composition.

### Documentation

- Updated `README.md`, `API.md`, and `ARCHITECTURE-ALIGNMENT.md` for the `3.5.3` documentation line.
- Updated hierarchy and dependency diagrams to reflect the deprecated status of `CanonicalPath` while keeping the type visible because it still exists in source.
- Repointed the main package documentation to these `3.5.3` release notes.

### Runtime And API Surface

- No implementation changes are included in this documentation patch.
- `CanonicalPath` still exists in source for compatibility, but the recommended path-composition model is direct `RaiPath` usage.
- Existing `CanonicalFile` behavior remains documented as compatibility-oriented canonical-by-name support.

### Validation

- Validation for this patch is documentation consistency: version references, release-note links, and diagram wording were updated together.

---

## 3.5.2

### Highlights

- Version bumped to `3.5.2`.
- Refreshes the packaged NuGet icon asset to a square `128x128` PNG.
- Establishes the next upstream `OsLibCore` patch release before later downstream package migrations.

### Packaging

- `OsLib.csproj` continues to publish as `OsLibCore`.
- Package metadata points at the tracked `HardCastle.png` asset used for the NuGet icon.
- This release is intended to settle on NuGet before later `RaiUtils`, `RaiImage`, and `JsonPit` fallback package updates.

### Runtime And API Surface

- No public API behavior was intentionally changed in this patch.
- The current documented path, config, and cloud-discovery semantics from `3.5.0` remain in effect.

### Validation

- Local validation for this patch uses the `OsLib` test suite before tagging and publishing.

---

## 3.5.0

### Highlights

- Version bumped to `3.5.0`.
- OsLib now documents the supported cloud-backed provider claim as `OneDrive`, `GoogleDrive`, and `Dropbox`.
- The shared `osconfig.json` contract and `defaultCloudOrder` documentation were aligned with the current implementation.
- Os path semantics were clarified around intrinsic runtime paths versus config-driven directories.
- Startup-critical configuration diagnostics now use structured logging and explicit degraded-mode console diagnostics.

### Configuration And Discovery

- The documented default cloud order is now consistent with the current implementation: `OneDrive`, `Dropbox`, `GoogleDrive`.
- `UserHomeDir` and `AppRootDir` are now documented as intrinsic runtime paths and no longer config-driven.
- `TempDir`, `LocalBackupDir`, and `CloudStorageRootDir` are documented as `RaiPath`-based directory properties.
- Missing, unreadable, or malformed `osconfig.json` now degrades startup without silently creating configuration.

### Path And Backup Semantics

- `CloudStorageRootDir` is the primary API; the string-based `CloudStorageRoot` remains only as an obsolete compatibility wrapper.
- `GetBackupRelativeDirectoryPath(...)` now returns `RaiPath`.
- `RaiFile.backup(copy)` now composes its destination through `Os.LocalBackupDir / relativePath` instead of string concatenation.

### Cross-Package Alignment

- OsLib documentation now explicitly aligns with JsonPit's `Id`-based identifier contract.
- Legacy JsonPit payloads that only contain `Name` are documented as normalizing to `Id` in the framework layer.

### Validation

- Full workspace validation passed after the `3.5.0` version bump: `200` tests total, `193` passed, `7` skipped, `0` failed.

---

## 3.3.0

### Highlights

- Version bumped to `3.3.0`.
- Introduced `Os.Config` as the top-level typed configuration entry point.
- Added reusable `ConfigFile<TData>` infrastructure for JSON-backed configuration files.
- Standardized machine-local configuration on `osconfig.json`.

### Configuration Model

- Cloud roots now live in a nested `cloud` object.
- Configurable directories now include:
  - `homeDir`
  - `tempDir`
  - `localBackupDir`
- Default provider precedence is configurable through `defaultCloudOrder`.

### Discovery And Runtime Behavior

- Cloud-root discovery now prefers configured values first, then provider probing.
- Discovered roots are cached for runtime efficiency.
- Missing provider roots can be persisted back into config when the corresponding config entry is empty.
- Local backup resolution now rejects cloud-backed configured backup paths and falls back to a local path.

### Validation

- Full solution validation remained green after the refactor and version bump.
