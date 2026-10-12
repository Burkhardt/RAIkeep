# OsLib Release Notes 4.x

## 4.5.10

- Release version: `4.5.10`
- Coordination tag: `v4.5.10`

### Highlights
- Coordinated 4.5.10 version alignment; no package-local behavior change.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.10` line.

---

## 4.5.9

- Release version: `4.5.9`
- Coordination tag: `v4.5.9`

### Highlights
- Coordinated 4.5.9 version alignment; no package-local behavior change.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.9` line.

---

## 4.5.8

- Release version: `4.5.8`
- Coordination tag: `v4.5.8`

### Highlights
- Adds typed `DenoCommand` supporting sandboxed local and `OverSsh` remote execution with `--context` / `--context-file` and explicit runtime permissions (`--allow-net`, `--allow-read`, `--deny-read`).
- Adds `CliCommand.OverSsh<T>` fluent remote routing and SSH target dispatch.
- Adds typed fleet CLI wrappers: `AmafuCommand`, `IorgCommand`, `JpitCommand`, `PitsCommand`, and `RaidCommand`.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.8` line.

---

## 4.5.7

- Release version: `4.5.7`
- Coordination tag: `v4.5.7`

### Highlights
- Adds SSH routing and remote availability probing to `CliCommand`.
- Adds typed Deno, Amafu, jpit, and expanded raid command request builders.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.7` line.

---

## 4.5.6

- Release version: `4.5.6`
- Coordination tag: `v4.5.6`

### Highlights
<!-- LLM / Author: summarize key architectural highlights and changes here -->

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.6` line.

---

## 4.5.5

- Release version: `4.5.5`
- Coordination tag: `v4.5.5`

### Highlights
Coordinated package/dependency alignment to 4.5.5. No independent runtime behavior change in this component.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.5` line.

---

## 4.5.4

Participates in the coordinated RAIkeep 4.5.4 patch release for the Amafu
`init --create-links` configuration-path fix. Package versions and applicable
internal dependency versions are aligned to 4.5.4. No runtime behavior changes
are introduced in OsLib by this patch.

See [Amafu 4.5.4 release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/Amafu_RELEASE_NOTES_4.x.md#454) for the fix and
configuration migration instructions.

---

## 4.5.3

OsLib v4.5.3 delivers CR051 configuration compatibility for multi-account cloud roots and symbolic shortcuts:

- **Unrestricted Cloud Roots**: `Os.Config` reads every nonempty string root declared in `Cloud`, eliminating the previous restriction to four legacy provider names. Roots are normalized and deduplicated.
- **Symbolic Link Resolution**: `ConfiguredCloudPaths` resolves symbolic shortcuts (such as `~/.CloudStorage/*`) and existing ancestors of new candidate paths, ensuring cloud-safe atomic in-place file handling across shortcuts.
- **Dependency Alignment**: Internal package dependencies align to 4.5.3.

Validation and release handoff: [RAIkeep 4.5.3](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#453). Preparation does not publish this package.

---

## 4.5.2

Coordinated 4.5.2 release; runtime behavior is unchanged. Internal package dependencies, where present, align to 4.5.2.

Validation and release handoff: [RAIkeep 4.5.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#452). Preparation does not publish this package.

---

## 4.5.0

Coordinated 4.5.0 foundation dependency; public behavior is unchanged.

All package and internal dependency versions are aligned to 4.5.0, coordinating live object reference semantics, sparse mutation tracking, and automated release validation gating across the entire RAIkeep platform.

Validation and release handoff: [RAIkeep 4.5.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#450). Preparation does not publish this package.

---

## 4.4.8

Coordinated 4.4.8 foundation dependency; public behavior is unchanged.

All package and internal dependency versions are aligned to 4.4.8. The version intentionally skips C# 4.4.7 to align the next coordinated release with jsonpit-python; Python implementation and publication remain with its maintainer.

Validation and release handoff: [RAIkeep 4.4.8](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#448). Preparation does not publish this package.

---

## 4.4.6

OsLib (`OsLibCore`) v4.4.6 introduces key infrastructure enhancements supporting CR049 and JsonPit storage refinements, including clean EventFile naming, asynchronous native archive decompression, streaming process execution, and buffered standard input support.

### 1. Clean EventFile Naming & Legacy Validation

- **Clean Logical Stems:** `EventFile.ComposeNameFor` emits `{LogicalStem}.event` without SHA-256 hash suffixes, reducing directory path lengths across cloud file systems.
- **Legacy Hash Support:** `EventFile` retains full recognition and validation for legacy `{stem}_{sha256}.event` filenames, verifying payload digests on read for seamless rolling upgrades.

### 2. Asynchronous Native Archive Decompression

- **Native Unzip Harness:** Introduces asynchronous `UnzipCommand` leveraging the OS native `unzip` utility on macOS and Linux/Ubuntu.
- **Asynchronous Process Execution:** `RaiSystem` dispatches extraction off the main thread with explicit timeout, exit-code validation, and standard error capture.

### 3. Piped Standard Input Support

- **Buffered Stdin for Pits:** `PitsSeedRequest` adds direct support for streaming standard input, enabling CLI tools and callers to pipe JSON/JSON5 payloads without disk staging.

### 4. Exclusive File Writes & System Hygiene

- Provides streaming exclusive file writing and per-process environment overrides.
- Aligns dependencies on .NET 10 across all platforms.

---

This release is part of the coordinated nine-package [CR049](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md) release. See [RAIkeep release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#446) for umbrella coordination.

---

## 4.4.5

OsLibCore participates in the synchronized RAIkeep v4.4.5 release for accepted [`CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md). `PitsSeedRequest.RequireExisting` exposes strict patch mode through the typed process boundary and emits the canonical `--require-existing` token. An incompatible WWWA target is rejected before process start; cloud-safe filesystem behavior remains unchanged.

---

## 4.4.4

OsLibCore participates unchanged in the synchronized RAIkeep v4.4.4 release for accepted [`CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md).

Cloud discovery and configuration generation live exclusively in standalone Amafu. OsLib gains no mutable configuration API, dynamic reload seam, or provider probing behavior; its startup configuration boundary remains immutable.

---

## 4.4.3

OsLibCore 4.4.3 participates unchanged in the synchronized eight-package
delivery of accepted
[`CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md).

The public file, path, and typed CLI boundaries remain unchanged. This package
aligns the coordinated dependency line at 4.4.3.

---

## 4.4.2

OsLibCore 4.4.2 participates unchanged in the synchronized eight-package
delivery of accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md).

The public file and typed CLI boundaries remain unchanged. This package aligns
the coordinated dependency line at 4.4.2.

---

## 4.4.1

OsLibCore 4.4.1 implements the public command boundary requested by accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
It also implements accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).

It adds typed `RaidCommand` requests for `import`, `export`, `refresh`, and
`validate`; separate ItemId/Number/NameExt identity; cloud and ItemTree options;
hydratable/plain SVG selection; token-safe execution through
`CliCommand`/`RaiSystem`; and serialized process-wide invocation. Controlled
fake-executable tests verify exact argument boundaries and execution results.
The shared `CliVerbDispatch` boundary detects reserved verbs outside argument
zero and produces deterministic corrected command lines before product I/O.

---

## 4.4.0

OsLibCore 4.4.0 participates unchanged in the synchronized eight-package
delivery of accepted
[`CR036_AIA_to_RAIkeep_Raid_CLI.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR036_AIA_to_RAIkeep_Raid_CLI.md).

The new CLI consumes `RaiPath`, `TextFile`, and `RaidFile`-backed boundaries;
no direct filesystem implementation is introduced in RaidCli.

---

## 4.3.2

OsLibCore 4.3.2 participates unchanged in the coordinated seven-package
RAIkeep v4.3.2 delivery of accepted
[CR027](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR027_AIA_to_RAIkeep_ClassDiagram_Generalization_and_SetSuperClass.md).
Its public filesystem, CloudDrive, and typed-command behavior is unchanged from
4.3.1. Publication remains behind RAI's manual release-chain gate.

---

## 4.3.1

OsLibCore 4.3.1 participates unchanged in the coordinated seven-package
RAIkeep v4.3.1 delivery of accepted
[CR026](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR026_AIA_to_RAIkeep_Diagram_Builder_Revision_Fidelity_and_Reference_Stereotypes.md).
Its public filesystem, CloudDrive, and typed-command behavior is unchanged from
4.3.0. Publication remains behind RAI's manual release-chain gate.

---

## 4.3.0

OsLibCore 4.3.0 is the coordinated foundation for accepted
[CR023](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR023_AIA_to_RAIkeep_PlantUml_Relationship_Rendering.md),
[CR024](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md), and
[CR025](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR025_AIA_to_RAIkeep_Typed_Raid_Builders_and_Deterministic_ItemTree_Emission.md).

- Public behavior is unchanged from 4.2.10.
- CR024 consumes the existing cloud-aware `RaiFile.rm()` boundary.
- CR025 artifact storage continues to inherit the CR022 in-place CloudDrive invariant.
- Package and fallback dependency versions align on 4.3.0.

The unpublished 4.2.11 preparation is superseded by this release. Publication
remains behind RAI's manual `scripts/release-chain.sh 4.3.0` gate.

---

## 4.2.11

> **Superseded before publication.** This prepared package line was not released;
> its changes are carried into v4.3.0.

OsLibCore participates unchanged in the coordinated RAIkeep 4.2.11 release.
CR024 process-flag cleanup consumes the established `RaiFile.rm()` cloud-aware
disappearance boundary; no new OsLib API or filesystem behavior is introduced.

---

## 4.2.10

OsLibCore 4.2.10 supplies the reusable storage and typed-command boundaries for
RAIkeep's RAI-authorized recovery-event archive and `iorg` addressing work.

- Adds `RaiZipFile`, `RaiZipEntry`, `RaiZipWriteResult`, and
  `RaiZipWriteStatus` for immutable collection archives.
- Archives are created directly at their final pathname in an existing parent;
  there is no TempDir staging, directory creation, extraction, overwrite, or
  delete/recreate of an established archive.
- Same-name retries reuse only a fully filename-and-byte-identical archive.
  Different or invalid existing content is preserved and reported.
- `EventDirectory.Inspect(...)` combines valid loose `.event` files and
  `Events_*.zip` entries without extraction and reports retained invalid or
  conflicting evidence.
- `PitsMaintainRequest.ArchiveEvents` emits `--archive-events` through the
  process-coordinated `PitsCommand` boundary.
- `IorgCommandOptions.RootIsApplicationRoot` emits `--app`;
  `IorgCommandOptions.Tenant` emits `--tenant`, while `Subscriber` remains a
  source-compatible alias.

Regression coverage verifies create-once behavior, identical retry, collision
and corruption retention, missing-parent non-creation, exact typed tokens, and
the absence of temporary archive files.

---

## 4.2.9

OsLibCore 4.2.9 implements the reusable filesystem boundary required by accepted
[CR022](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md)
and carries forward the typed maintenance coordination introduced by accepted
[CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md).

- Adds `RaiCloudStorageException` with operation, source, and destination context.
- `RaiFile.mv` and `RaiPath.mv` reject TempDir-to-cloud moves before mutation.
- Existing cloud files are overwritten in place; the source of an explicit move
  is removed only after the destination write succeeds.
- Existing cloud directories cannot be replaced through `mv` or `cp`.
- Cloud backup requests preserve the live source and create a copy.
- Missing-copy sources and operating-system failures surface through the typed
  `RaiFileIOException` boundary.

Regression coverage verifies rejection before mutation, continuously present
cloud pathnames, safe same-tree semantic renames, and non-destructive backups on
a real configured CloudDrive root.

---

## 4.2.8

OsLibCore 4.2.8 implements its share of accepted
[CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md).

- Explicit non-default `TextFile` extensions now preserve dotted logical stems such as `Nkosikazi-AIA.Api-93455.flag`; implicit complete-filename parsing remains compatible.
- Adds the unambiguous `(Name, Ext)` `TextFile` constructor.
- Adds `PitsMaintainRequest`, deterministic argument construction, and sync/async `Maintain` execution.
- Typed `PitsCommand` calls now share a process-local provider/root/pit gate. Same-target calls queue, unrelated targets may overlap, WWWA takes `Person`, `Object`, `Place`, `Activity` in fixed order, and queued cancellation launches no child.
- No `Os.Config` mutation or new direct consumer filesystem dependency was introduced.

Verified by the full OsLibCore Release suite and focused CR021 argument, transport,
dotted-name, concurrency, and cancellation tests.

---

## 4.2.7

Implements the OsLibCore portion of accepted
[CR020](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md).

- Adds typed `IorgListRequest` and `IorgMoveRequest` forms, deterministic argument builders, and sync/async `IorgCommand` execution.
- Aligns `IorgCleanRequest` with exact-ItemId cleanup and explicit subscriber-wide cache cleanup.
- Adds `PathConventionType.Flat` after all existing values, preserving numeric compatibility.
- Adds `RaiPath.EnumerateFiles(searchPattern, recursive)` so consumers can request recursive traversal without referencing the underlying platform traversal enum.
- Verifies argument-token fidelity, option forwarding, validation, and async process execution.

Tagging and NuGet publication remain behind RAI's manual release gate.

---

## 4.2.6

Coordinated dependency release for accepted CR019. OsLib runtime and public API
behavior are unchanged from 4.2.5.

---

## 4.2.5

Typed command-boundary support for accepted CR017.

- Adds optional `PitsExportRequest.At` for point-in-time exports.
- Emits `--at` and a canonical UTC timestamp as separate exact argument tokens.
- Supports the same request through synchronous and asynchronous `PitsCommand`
  execution and managed-assembly test entry points.
- Omitting `At` preserves the established export argument list.

Release verification: 111 OsLibCore Release tests passed.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

---

## 4.2.4

Coordinated dependency release for accepted CR016.

- Retains the existing `RaiPath.EnumerateDirectories(...)` and
  `RaiPath.EnumerateFiles(...)` boundary used by RaiImage's normalization-
  resilient resolver.
- Adds no new direct filesystem API or OsLib runtime behavior.
- Carries CR008, CR014, and CR015 boundaries forward unchanged.

Release verification: 110 OsLibCore Release tests passed.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

---

## 4.2.3

Coordinated CR015 patch release.

- Adds public `PitsDeletePropertyRequest` and `PitsDeleteItemRequest` contracts.
- Adds exact token builders for `pits delete-property` and `pits delete-item`.
- Adds synchronous and asynchronous typed execution through `PitsCommand`.
- Validates mandatory pit, item, and dot-delimited property-path values before
  process execution.
- Retains the CR014 `CliCommand`/`RaiSystem` tokenized execution and result
  boundary unchanged.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

Release verification: 110 OsLib Release tests passed, including six added
CR015 typed-delete token and validation cases.

---

## 4.2.2

Coordinated patch release completing the accepted
`CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md` boundary.

This release also implements the OsLibCore portion of accepted
`CR014_RAI_to_RAIkeep_Typed_CLI_Command_Wrappers.md` and its accepted
`CR014.1_test-concept.md` testing guidance.

- `RaiFile.ReadAllBytesAsync(...)` wraps operating-system `IOException` and
  `UnauthorizedAccessException` failures in `RaiFileIOException`.
- `RaiFileIOException` retains `IOException` compatibility, exposes the affected
  `FileName`, and preserves the original failure as `InnerException`.
- Cancellation remains `OperationCanceledException` and is not wrapped.
- The validated configured `Os.TempDir`, immutable `Os.Config`, `RaiPath`
  exceptions, and stream-free ingestion contracts remain unchanged.
- Adds public `PitsCommand` and `IorgCommand` wrappers for installed-binary and
  managed-DLL invocation from servers, agents, and package-owned tests.
- Adds typed request/option contracts for preferred 4.x `seed`, `export`,
  `audit`, `organize`, and `clean` command forms.
- Validates mandatory, mutually exclusive, numbered, and path-like parameters
  before process start.
- Adds tokenized `CliCommand.Run(...)` / `RunAsync(...)` overloads backed by
  `ProcessStartInfo.ArgumentList`, plus safe POSIX serialization for explicit
  SSH command boundaries.
- `RaiSystemResult` now exposes the exact original `ArgumentList` and derived
  `Succeeded` state. Timeout kills the process tree and returns `TimedOut`;
  caller cancellation kills the process tree and remains cancellation.
- CR014.1 coverage uses capture executables for edge-case argument forwarding,
  output/error/exit handling, timeout, cancellation, and startup failures;
  package-owned `--version` smoke checks invoke the real managed CLIs.
- Extends `SshSystem` with tokenized SSH options; JsonPit's remote scenarios no
  longer hand-build SSH process invocations.

Released as part of the coordinated RAIkeep v4.2.2 release.

Release verification: 104 OsLib Release tests passed, including 21 focused
CR014/CR014.1 wrapper-contract tests.

---

## 4.2.0

Coordinated release for the seven-package RAIkeep 4.2 line.

- Preserves the CR008 `Os.TempDir` contract introduced in 4.1.0: the configured
  `RaiPath` is validated once with an OsLib `TmpFile` probe and initialization
  fails fast when it cannot be written.
- Preserves `Os.Config` as the immutable runtime source of truth without a
  fallback to a different temporary directory.
- Carries `RaiPathException`, `RaiPathNotFoundException`, and asynchronous byte
  chunk ingestion forward for RaiImage and RaiDiagram consumers.
- Updates package metadata and documentation for the coordinated 4.2.0 line.

No intentional OsLib runtime behavior change is introduced after 4.1.0.

Release verification: 81 OsLib Release tests passed.

---

## 4.1.0

Implements the OsLib portion of
`CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md`.

- `Os.TempDir` remains the configured runtime `RaiPath` and is documented as a
  public boundary.
- First Os initialization validates the configured directory by creating,
  observing, and removing an OsLib `TmpFile`.
- Initialization fails fast when the probe cannot be written. `Os.Config` is not
  mutated and the configured path is not silently replaced by a fallback.
- Adds `RaiPathException` and `RaiPathNotFoundException` for explicit missing-path
  failures.
- Adds `RaiFile.WriteFromAsync(IAsyncEnumerable<byte[]>, CancellationToken)` for
  consumers that should not receive a `System.IO.Stream` boundary.

Release verification: 81 OsLib Release tests passed.

---

## 4.0.1

**Date:** 2026-08-10
**Author / Delivering Agent:** RAIkeep Dev Agent
**Delivered Version:** v4.0.1
**Target Consumers:** RAIkeep package family, AfricaStage, AIA
**Status:** Prepared — publication approval pending

### 1. Summary

OsLibCore v4.0.1 is the synchronized foundation package for the coordinated
CR006 CLI patch line. It contains no OsLibCore API or behavior change from
v4.0.0.

### 2. Resolved Change Requests (CRs)

- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — synchronized package participation only; implementation is owned by ImgSeeder and PitSeeder.

### 3. Root Cause Analysis & Technical Resolution

RAIkeep packages are released as one coordinated version line. OsLibCore moves
to v4.0.1 so downstream fallback dependencies remain exact and deterministic;
no source-level resolution was required in this component.

### 4. Public Contract & API / Package Changes

- Package version: `4.0.1`.
- Public API and runtime behavior: unchanged from `4.0.0`.

### 5. Validation & Acceptance Evidence

- OsLib.Tests: **80 passed, 0 failed, 0 skipped** in the coordinated run.

### 6. Upgrade & Consumption Instructions

Consume OsLibCore v4.0.1 with the other five coordinated RAIkeep v4.0.1 packages.

---

## 4.0.0

**Date:** 2026-08-05  
**Author / Delivering Agent:** RAIkeep Dev Agent  
**Delivered Version:** v4.0.0  
**Target Consumers:** JsonPit, PitSeeder, AIA, AfricaStage  
**Status:** Implemented — coordinated 4.0.0 line; NuGet publication pending release authorization

---

### 1. Summary

OsLib supplies the shared filesystem primitives required by the coordinated JsonPit
concurrency contract: a no-delete/no-rename `TextFile.Save`, deterministic canonical
JSON with SHA-256 hashing, and generic create-once event files with stateless
directory aggregation. OsLib owns storage mechanics only; it imposes no event-content
schema and never interprets JsonPit fields.

### 2. Resolved Change Requests (CRs)

- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) — OsLib share of the coordinated v4.0.0 concurrency work (agreed `TextFile.Save` contract, canonical JSON, `EventFile`/`EventDirectory`).

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

- Consume `OsLibCore 4.0.0`. No call-site changes are required.
- Callers that relied on `Save(backup: true)` *moving* the previous file must note it
  now copies; the original pathname always survives a save.
- Durable audit producers: construct `new EventFile(rootPath, logicalStem, contentObject)` —
  the constructor performs the create-once write. Consumers read via
  `EventDirectory.Events(rootPath)`.
