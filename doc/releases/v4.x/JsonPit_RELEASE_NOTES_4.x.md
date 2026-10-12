# JsonPit Release Notes 4.x

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
- Relaxes strict ID assertion in `PitItem.ExtendWith` to allow updates when the incoming payload specifies the matching `Id`.
- Preserves envelope protection against overwriting protected metadata (`Created`, `Modified`, `Deleted`).

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.8` line.

---

## 4.5.7

- Release version: `4.5.7`
- Coordination tag: `v4.5.7`

### Highlights
- Coordinated with the 4.5.7 platform line; no package-local behavior changes.

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
are introduced in JsonPit by this patch.

GettingStarted now explains shortcut-based cloud initialization and migration of existing configuration.

See [Amafu 4.5.4 release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/Amafu_RELEASE_NOTES_4.x.md#454) for the fix and
configuration migration instructions.

---

## 4.5.3

Coordinated 4.5.3 release aligning package dependencies with OsLibCore 4.5.3. Persistence, live references, and mutation tracking behavior are unchanged.

Validation and release handoff: [RAIkeep 4.5.3](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#453). Preparation does not publish this package.

---

## 4.5.2

Updates GettingStarted with recommended Amafu cloud shortcuts for new and existing configurations. Persistence, live references, and mutation tracking behavior are unchanged. Package and fallback dependencies align to 4.5.2.

Validation and release handoff: [RAIkeep 4.5.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#452). Preparation does not publish this package.

---

## 4.5.0

4.5.0 adds original live object references, sparse tracked mutations, and per-instance in-memory tracking modes.

`Pit.Add(item)` adopts the original item and nested objects for a new identity. Current accessors return those live references. Tracked edits append sparse fragments; history owns independent snapshots. Projection happens at acceptance/load/merge boundaries.

`Pit.DefaultMutationTrackingMode` defaults to `TrackedChangesWithFallback`. Each Pit captures this process-local policy for its in-memory lifetime; it is never persisted. Servers can choose `TrackedChangesOnly` at startup to disable boundary comparisons. **Unreported edits will receive their history timestamp when detected.** Multiple unreported edits may coalesce, and detection timestamps may affect conflict precedence.

GettingStarted documents live mutation and `people.ItemProperty = new { Id = "Max", ... }`. The mutation guide and agent guidance define supported operations, sparse-history isolation, and concurrency limits. Legacy filename regression tests now match the released naming formats and explicitly test real checksum collisions without overwriting.

All package and internal dependency versions are aligned to 4.5.0. Coordinates platform-wide with automated release consistency validation.

Validation and release handoff: [RAIkeep 4.5.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#450). Preparation does not publish this package.

---

## 4.4.8

4.4.8 adds original live object references, sparse tracked mutations, and per-instance in-memory tracking modes.

`Pit.Add(item)` adopts the original item and nested objects for a new identity. Current accessors return those live references. Tracked edits append sparse fragments; history owns independent snapshots. Projection happens at acceptance/load/merge boundaries.

`Pit.DefaultMutationTrackingMode` defaults to `TrackedChangesWithFallback`. Each Pit captures this process-local policy for its in-memory lifetime; it is never persisted. Servers can choose `TrackedChangesOnly` at startup to disable boundary comparisons. **Unreported edits will receive their history timestamp when detected.** Multiple unreported edits may coalesce, and detection timestamps may affect conflict precedence.

GettingStarted documents live mutation and `people.ItemProperty = new { Id = "Max", ... }`. The mutation guide and agent guidance define supported operations, sparse-history isolation, and concurrency limits. Legacy filename regression tests now match the released naming formats and explicitly test real checksum collisions without overwriting.

All package and internal dependency versions are aligned to 4.4.8. The version intentionally skips C# 4.4.7 to align the next coordinated release with jsonpit-python; Python implementation and publication remain with its maintainer.

Validation and release handoff: [RAIkeep 4.4.8](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#448). Preparation does not publish this package.

---

## 4.4.6

JsonPit v4.4.6 fulfills **Deliverable A** of [CR049](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md) (*Live ID Validation, ZIP Image Ingestion, and Receipt Persistence*) along with platform-ratified storage refinements for cloud-synchronized file integrity and naming hygiene.

### 1. Fulfillment of CR049 Deliverable A: Prohibit Template Markers in Live Entity IDs

- **Canonical Identity Enforcement (A01, A04):** Public write boundaries (`Pit.Add`, `Pit.AddRange`, and `PitItem.Id` property mutations) reject entity IDs containing unresolved template markers (`{` or `<`). Attempting to commit placeholder identities throws `ArgumentException` before mutating memory or disk. Missing, whitespace-only, or non-string IDs are rejected upfront.
- **Atomic Batch Preflight (A02):** Multi-record writes validate all entity IDs before mutating the in-memory store or staging change files. If any entity fails validation, zero records are committed.
- **Ordinary Fields Unrestricted (A03):** Template markers inside non-ID fields (`Name`, `Note`, payloads) remain unrestricted.
- **Historical Preservation & Clean Recovery (A05):** Legacy records containing placeholder IDs remain readable, exportable, and queryable. Tombstone deletions (`Deleted = true`) and `AddHistorical` remain permitted to allow operators to purge historical anomalies, while live re-insertion of invalid IDs is blocked.

### 2. Cloud-Safe 4-Character Checksum for ChangeFiles

- **Integrity Without Path Bloat:** Change files now use a concise 4-character hex checksum suffix: `{UtcTicks}_{ExactProcessIdentity}_{4charHex}.json`. Derived from the first 4 characters of the SHA-256 payload digest, this checksum reliably detects partial cloud synchronization (e.g. OneDrive, Dropbox, Google Drive, iCloud) without inflating path lengths or exceeding filesystem limits.
- **Backward-Compatible Readers:** The engine verifies the 4-character checksum upon reading, while continuing to load and validate legacy 64-character SHA-suffixed change files. Corrupted or truncated files fail cleanly before polluting engine state.

### 3. Clean EventFile Naming

- **Concise Logical Stems:** Event compaction archives no longer embed 64-character SHA-256 hashes in filenames. Events are emitted with clean logical stems: `{LogicalStem}.event` (e.g. `20261001-120000.event`), keeping directory entries short and cloud-friendly.

### 4. In-Place Legacy EventFile Migration

- **Automated Archive Migration:** Maintenance operations via `pits maintain --apply` (and `JsonPit.InspectLegacyExtensions`) locate legacy `{stem}_{sha256}.event` archives, verify their payload integrity, and rename them in-place to clean `{stem}.event` files on the same volume (honoring CR022 cloud-safe sibling guarantees).
- **Multi-Version Coexistence:** Unmigrated legacy event files continue to be recognized and replayed seamlessly by both C# `JsonPit` and Python `jsonpit`.

### 5. Architectural & API Cleanups

- **Removal of Obsolete `Item` Class:** The deprecated legacy `Item` class in `JsonPit.cs` has been completely deleted in favor of the strongly typed, polymorphic `PitItem` domain model.
- **Process-Monotonic Timestamps:** Enforces monotonic timestamps so high-frequency mutations within a process retain unique, ordered change file stems.

---

**Traceability:** This release formally closes Deliverable A of [CR049](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md). Package versions and fallback dependencies align at 4.4.6 across the entire platform. See [RAIkeep release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#446) for umbrella coordination.

---

## 4.4.5

JsonPit participates unchanged at the public library level in the synchronized RAIkeep v4.4.5 release for accepted [`CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md). PitSeeder uses JsonPit's existing unflagged read-only projection and `Contains(id, withDeleted: false)` APIs to validate strict patches without changing the persistence or coordination contracts.

---

## 4.4.4

JsonPit participates unchanged in the synchronized RAIkeep v4.4.4 release for accepted [`CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md). Persistence, lifecycle protection, clean change filenames, and cloud-safe maintenance semantics remain unchanged.

---

## 4.4.3

JsonPit 4.4.3 participates unchanged in the synchronized eight-package
delivery of accepted
[`CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md).

CR040 protected lifecycle attributes, CR041 clean dual-format change files,
receipt cleanup, event archives, temporal export, and finalizer behavior remain
unchanged. Fallback dependencies align to OsLibCore and RaiUtils 4.4.3.

---

## 4.4.2

JsonPit 4.4.2 implements accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md).

- `SetProperty`, `ExtendWith`, and `Merge` atomically reject top-level `Id`,
  `Modified`, or `Deleted`; property tombstones reject the same protected names.
- Live `Pit.Add(...)` rejects projected payloads carrying client lifecycle
  fields. Trusted canonical and change-fragment replay uses `AddHistorical(...)`.
- New change and receipt files use
  `{Modified.UtcTicks}_{ExactProcessIdentity}.{json|receipt}`. Discovery accepts
  both clean CR041 names and legacy SHA-suffixed CR003 names.
- Live mutations receive process-monotonic UTC ticks so concurrent writes retain
  distinct clean filenames despite ordinary OS clock resolution.
- Clean names use strict JSON validation; legacy names retain SHA verification.
  Receipt creation and the established ten-minute cleanup grace apply to both.
- Equal-time historical fragments using the same exact process identity fail
  explicitly instead of replacing an existing cloud artifact.

The finalizer remains free of recovery publication and filesystem I/O, and the
canonical path becomes reopenable after forced collection.

---

## 4.4.1

JsonPit 4.4.1 participates unchanged in the synchronized eight-package delivery
of accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
The coordinated release also carries accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).

Persistence, cleanup receipts, event archives, audit, temporal export, and
clean-exit process-flag behavior remain unchanged. Fallback dependencies align
to 4.4.1.

---

## 4.4.0

JsonPit 4.4.0 participates unchanged in the synchronized eight-package delivery
of accepted
[`CR036_AIA_to_RAIkeep_Raid_CLI.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR036_AIA_to_RAIkeep_Raid_CLI.md).

Existing persistence, finalizer, receipt, and process-flag invariants remain
unchanged.

---

## 4.3.2

JsonPit 4.3.2 participates unchanged in the coordinated seven-package RAIkeep
v4.3.2 delivery of accepted
[CR027](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR027_AIA_to_RAIkeep_ClassDiagram_Generalization_and_SetSuperClass.md).
Its CR024 disposal and persistence behavior is unchanged from 4.3.1; finalizers
remain strictly free of filesystem and recovery-publication I/O. Publication
remains behind RAI's manual release-chain gate.

---

## 4.3.1

JsonPit 4.3.1 participates unchanged in the coordinated seven-package RAIkeep
v4.3.1 delivery of accepted
[CR026](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR026_AIA_to_RAIkeep_Diagram_Builder_Revision_Fidelity_and_Reference_Stereotypes.md).
Its CR024 disposal and persistence behavior is unchanged from 4.3.0; finalizers
remain strictly free of filesystem and recovery-publication I/O. Publication
remains behind RAI's manual release-chain gate.

---

## 4.3.0

JsonPit 4.3.0 carries the accepted
[CR024 process-flag self-cleanup](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md)
implementation from the intentionally unpublished 4.2.11 preparation.

- Explicit `Pit.Dispose()` removes only its exact owned PID-specific flag after
  the established durability work through `RaiFile.rm()`.
- Read-only and writable pits share the same cleanup path.
- `Master.flag`, lease TTL, crash recovery, and maintenance pruning are unchanged.
- Finalizers remain strictly free of filesystem and recovery-publication I/O.

The package participates in the coordinated 4.3.0 dependency line. Publication
remains behind RAI's manual release gate.

---

## 4.2.11

> **Superseded before publication.** This prepared package line was not released;
> its changes are carried into v4.3.0.

JsonPit 4.2.11 implements accepted
[CR024](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md).

- `ProcessFlagFile.TryReleaseCurrentProcess()` ownership-checks and removes the
  exact PID-specific process flag through `RaiFile.rm()`.
- Explicit read-only and writable `Pit.Dispose()` therefore leave no process
  flag after their existing durability work completes.
- Process-window cleanup never changes or removes `Master.flag`; established
  master leases and TTL behavior are unchanged.
- Finalization remains strictly free of filesystem and recovery-publication I/O.
- Flags left by crashes remain discoverable and eligible for the existing
  explicit maintenance pruning path.

Tests cover owned and foreign flags, both disposal modes, master preservation,
and the existing finalizer/no-I/O contract.

---

## 4.2.10

JsonPit 4.2.10 implements the RAI-authorized recovery-event archive backlog while
preserving CR021 durable cleanup and CR022 cloud-storage invariants.

- `PitMaintenanceOptions.ArchiveEvents` previews or applies compaction of a
  stable snapshot of valid loose recovery events.
- Archive names use the oldest and newest validated event-content timestamps in
  UTC: `Events_yyyyMMdd-HHmm_to_yyyyMMdd-HHmm.zip`.
- Apply creates one immutable archive directly in the existing `Events`
  directory, validates every selected filename and byte payload, and only then
  retires the matching loose files individually.
- Interrupted/partial retirement is restart-safe: identical loose/archive copies
  are recognized on retry. Changed sources, corrupt evidence, and pathname
  collisions are retained and reported.
- `PitAudit.Read(...)` transparently combines loose and archived events and
  deduplicates them by `EventId`; `PitAudit.Inspect(...)` additionally returns
  physical integrity/conflict diagnostics.

Tests cover preview, apply, exact UTC range naming, retry, collisions, corrupt
sources and archives, logical audit continuity, and event-identity conflicts.

---

## 4.2.9

JsonPit 4.2.9 implements its incident correction under accepted
[CR022](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md)
while preserving accepted [CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md)
receipt-backed cleanup semantics.

- `Pit.Maintain(...)` checks the non-creating canonical parent directly.
- Report-only and apply maintenance against a missing pit return deferred
  evidence without creating a pit directory, canonical file, flag, or receipt.
- `PitMaintenanceResult` can represent a missing target without constructing a
  live `Pit` instance.
- Canonical persistence, recovery, receipt ordering, finalizer behavior, and
  explicit maintenance deletion semantics remain unchanged.

The investigation found no evidence that CR021 replaced the established AIA
`Activity`, `Person`, `Object`, or `Place` directories. Regression coverage now
protects the missing-target no-filesystem-mutation boundary explicitly.

---

## 4.2.8

JsonPit 4.2.8 implements accepted
[CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md),
narrowly superseding CR003's in-memory-only cleanup-eligibility rule.

- Adds immutable `ReceiptFile` evidence beside each canonically accounted hashed change file. The original UTC `Time` survives replay, restart, and master transfer without refresh.
- `Pit.Maintain(...)` provides report-only inventory or explicit application through the existing persistence/recovery gate.
- Eligible cleanup revalidates exact-master authority, change integrity, canonical health/accounting, and receipt age, then removes the change first and receipt second.
- Malformed, incomplete, unverifiable, or non-master work remains deferred and retained. Orphan receipts are safely retryable.
- `PitMaintenanceOptions` separately authorizes age-qualified PID-window pruning and content-validated extensionless flag/event repair. `Master.flag`, conflict evidence, active windows, unknown files, and recovery events are never implicitly removed.
- The finalizer contract remains unchanged: no recovery publication or filesystem I/O, and abandoned canonical paths become reopenable.

Verified by focused and package-level Release coverage, including the receipt
lifecycle on a real configured CloudDrive root, restart with unchanged receipt
time, grace-expiry cleanup, malformed/orphan evidence, explicit hygiene, legacy
repair, and the finalizer regression. The separate two-machine split-master
scenario still requires an active synchronizer on Mzansi.

---

## 4.2.7

JsonPit participates in the coordinated RAIkeep 4.2.7 release implementing
accepted [CR020](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md).

- Aligns fallback dependencies on `OsLibCore 4.2.7` and `RaiUtils 4.2.7`.
- JsonPit persistence, history, tombstone, point-in-time projection, and concurrency behavior are unchanged from 4.2.6.

Tagging and NuGet publication remain behind RAI's manual release gate.

---

## 4.2.6

Coordinated dependency release for accepted CR019. JsonPit adopts the
RaiUtils/OsLibCore 4.2.6 line; persistence behavior is unchanged from 4.2.5.

---

## 4.2.5

Historical projection alignment for accepted CR017.

- Keeps `Pit.GetAt(...)`, timestamped `Pit.ExportJson(...)`, and
  `PitItems.ProjectState(...)` as the authoritative point-in-time engine.
- Carries event ordering, nested tombstones, deletion walls, resurrection, and
  late/backdated-fragment semantics forward unchanged.
- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.5.

Release verification: all 156 JsonPit tests passed—154 local/configured cases
plus both isolated live Nkosikazi/Mzansi synchronization scenarios.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

---

## 4.2.4

Coordinated dependency release for accepted CR016.

- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.4.
- Preserves CR015 nested tombstones and explicit nested deletion unchanged.
- Introduces no JsonPit public API behavior change.

Release verification: all 156 JsonPit tests passed—154 local/configured cases
plus both isolated live Nkosikazi/Mzansi synchronization scenarios.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

---

## 4.2.3

Implements the JsonPit portion of accepted CR015.

- Treats JSON null as a property tombstone at arbitrary nested object depth.
- Recursively merges historical fragments so sibling properties survive nested
  deletions.
- Omits tombstoned properties and newly empty parent objects from projected
  reads and JSON exports.
- Adds `PitItem.Merge(JObject)` with tombstone-aware partial merge semantics.
- Adds `PitItem.DeletePropertyPath(...)` for explicit dot-delimited traversal.
- Preserves `DeleteProperty(...)` as a literal top-level property operation.
- Preserves append-only historical fragments, time travel, deletion barriers,
  and later property reintroduction.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

Release verification: 23 focused merge/property-deletion tests passed,
including ten added or tightened CR015 cases. The complete JsonPit Release suite
passed all 156 tests, including configured persistence and remote scenarios.

---

## 4.2.2

Coordinated dependency release for the RAIkeep 4.2.2 package line.

- Carries the abandoned-instance watcher ownership and finalizer regression fix
  forward unchanged.
- Forced collection can remove the weak registry target and make the canonical
  path reopenable.
- The finalizer performs no recovery publication, watcher disposal, or
  filesystem I/O.
- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.2.
- Keeps `UseLocalRAIkeepSources=false` as the package-only release boundary.
- CR014 remote integration helpers construct preferred `pits seed` arguments
  through `OsLib.PitsCommand` and execute SSH through `SshSystem`; no JsonPit
  production behavior is moved into the wrapper tests.

Released as part of the coordinated RAIkeep v4.2.2 release.

Release verification: the focused finalizer regression passed and the complete
JsonPit Release suite passed 146 tests, including configured cloud/remote
scenarios.

---

## 4.2.0

Coordinated release for the seven-package RAIkeep 4.2 line.

- Carries the 4.1.0 abandoned-instance watcher ownership fix forward.
- Forced collection can remove the weak registry target and make a canonical
  path reopenable.
- The finalizer remains deliberately free of recovery publication, watcher
  disposal, and filesystem I/O.
- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.0.
- Makes `UseLocalRAIkeepSources=false` force package references and removes
  duplicate direct OsLib/RaiUtils project references from the test project, so
  package-only release validation exercises the intended dependency graph.
- Stabilizes the real Nkosikazi-to-Mzansi client phase by renewing the exact
  owner lease after the initial cloud sync and waiting for that specific ticket
  timestamp before launching the remote CLI.

Release verification: the focused finalizer regression passed, and the complete
JsonPit Release suite passed 146 tests including configured cloud/remote
scenarios.

---

## 4.1.0

Aligns JsonPit with the CR008 OsLibCore/RaiUtils 4.1 boundaries and fixes the
abandoned-instance path-registration regression.

- `FileSystemWatcher` callbacks capture a weak `Pit` owner rather than retaining
  the instance through native watcher event handlers.
- Debounce work also reacquires weak ownership only when needed and does not keep
  an abandoned instance alive across its delay.
- Forced collection can therefore remove the weak registry target and make the
  canonical path reopenable.
- The finalizer remains deliberately free of watcher disposal, recovery
  publication, and filesystem I/O.
- The real OneDrive/SSH synchronization regression now waits for authoritative
  `Master.flag` contents to arrive on Mzansi, not merely a placeholder pathname.

Focused finalizer verification passed. The complete JsonPit Release suite is a
required release gate.

---

## 4.0.1

**Date:** 2026-08-10
**Author / Delivering Agent:** RAIkeep Dev Agent
**Delivered Version:** v4.0.1
**Target Consumers:** RAIkeep package family, AfricaStage, AIA
**Status:** Prepared — publication approval pending

### 1. Summary

JsonPit v4.0.1 is the synchronized persistence package for the coordinated
CR006 CLI patch line. It contains no JsonPit API, persistence, lease, recovery,
or concurrency behavior change from v4.0.0.

### 2. Resolved Change Requests (CRs)

- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — synchronized package participation only; CLI implementation is owned by ImgSeeder and PitSeeder.

### 3. Root Cause Analysis & Technical Resolution

JsonPit moves to v4.0.1 and aligns fallback dependencies on OsLibCore and
RaiUtils v4.0.1. The CR006 changes remain outside JsonPit's runtime contracts.

### 4. Public Contract & API / Package Changes

- Package version: `4.0.1`.
- Fallback dependencies: OsLibCore `4.0.1`, RaiUtils `4.0.1`.
- Public API and runtime behavior: unchanged from `4.0.0`.

### 5. Validation & Acceptance Evidence

- Current Release revalidation: **145 passed, 1 failed, 0 skipped**. The existing
  finalizer/GC ownership test
  `Finalizer_PerformsNoRecoveryPublicationOrFilesystemIO_AndPathBecomesReopenable`
  also fails in isolation because the generated unique path remains registered
  after forced collection. No JsonPit source or test changed in v4.0.1; only
  synchronized version and dependency metadata changed.

### 6. Upgrade & Consumption Instructions

Consume JsonPit v4.0.1 with the other five coordinated RAIkeep v4.0.1 packages.

---

## 4.0.0

**Date:** 2026-08-05  
**Author / Delivering Agent:** RAIkeep Dev Agent  
**Delivered Version:** v4.0.0  
**Target Consumers:** AIA, AfricaStage, PitSeeder  
**Status:** Implemented — coordinated 4.0.0 line; NuGet publication pending release authorization

---

### 1. Summary

JsonPit 4.0.0 makes RAIkeep's concurrency behavior explicit, testable, and enforceable
across threads in one process, processes on one machine, and machines sharing
cloud-synced pit files. It fixes the confirmed concurrent save-and-add persistence
race, introduces exact-process master ownership, one-live-instance path ownership,
validated candidate loads, collision-safe hashed change files, and live split-master
recovery with structured durable audit events.

### 2. Resolved Change Requests (CRs)

- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) — the governing concurrency contract, together with its accepted supporting design [`JsonPit-CONCEPT-Live-Split-Master-Recovery.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit-CONCEPT-Live-Split-Master-Recovery.md) and implementation companion `Details of CR003.md`.

### 3. Root Cause Analysis & Technical Resolution

#### Confirmed regression — concurrent save and add

`Store()` applied LINQ ordering and materialization directly to live `HistoricItems`
while concurrent `Add` operations mutated the same `ConcurrentDictionary`
(`IndexOutOfRangeException`, `ArgumentException` from `CopyTo`). It then validated the
*live latest* fragments after I/O, so a fragment accepted after the written snapshot
could be marked persisted prematurely — a silent-loss window.

**Resolution — the agreed v4.0.0 persistence boundary:**
- A `ReaderWriterLockSlim` state/snapshot gate: concurrent `Add` calls enter shared
  mode (never serialized behind cloud I/O); `Save` takes brief exclusive access,
  captures a byte-stable snapshot (fragments cloned inside the gate) plus the exact
  set of included dirty fragments and the snapshot change time, and releases the gate
  before serialization, cloud-file I/O, and flag updates.
- Only fragments demonstrably included in the persisted snapshot are validated; flag
  metadata is computed from snapshot facts, never newer live state. A later addition
  keeps its existing per-fragment dirty state until a snapshot containing it persists.
  No second pending-write queue was introduced.
- The regression test `SaveInterleavedWithAdds_SubsequentSavePersistsEveryAcceptedItem`
  passes repeatedly.

#### Deterministic equal-timestamp and replay behavior

- Live `Add` refreshes `Modified` from real `DateTimeOffset.UtcNow` once at the
  insertion boundary (not restamped on CAS retries); `AddHistorical` preserves supplied
  timestamps; uniqueness is not promised and nothing depends on it. No monotonic clock
  or injected time source was added.
- History order: `Modified` descending → fewer JSON properties first → canonical
  content ordinal tie-break (computed only for the double-tie case). Exact replay of a
  fragment already in history is idempotent and consumes no bounded-history slot.
  Projection keeps first-seen precedence; every participant computes the same result
  from the same fragments in any arrival order (`PitItems.CompareFragments` is public).

#### One live public `Pit` per canonical path per process

- A process-wide registry reserves the canonical path before the constructor performs
  observable pit work; a duplicate (writable or read-only) throws the descriptive
  `PitInstanceConflictException`. `Dispose` releases the reservation; constructor
  failure never leaves a stale one. Internal comparison/merge paths use private
  snapshot readers — the former internal `new Pit(...)` constructions are gone.

#### Read-during-write contract

- `Load`/`Reload` build a complete validated candidate and replace live state only
  after the entire canonical snapshot parsed successfully; fragments from a validated
  canonical enter clean. Transient absence, emptiness, or unparseable content during a
  known rewrite is retried without clearing state; bounded exhaustion throws the
  descriptive `JsonPitPersistenceException`. Initial absence remains a valid no-data
  case. The former `Reload` "changed without permission" exception is obsolete under
  exact-PID ownership: a master-time advance while this exact process is the recorded
  owner is its own earlier write, handled by reloading.

#### Exact-process master ownership and handoff

- `Master.flag` records `{Machine}-{Subscriber}-{PID}`; only the exact owner renews.
  A second PID of the same participant is refused while the owner's process window is
  active (change-file fallback) and inherits the still-protected lease after explicit
  release or expiry. Different subscribers remain distinct participants. No
  operating-system or distributed file lock was added.

#### Collision-safe change files, merge, and cleanup

- Every ordinary change file uses `{Modified.UtcTicks}_{ExactProcessIdentity}_{Sha256}.json`
  with the hash over the exact canonical UTF-8 payload (no trailing terminator);
  republication is filename-idempotent, equal-time fragments cannot suppress one
  another, and merge requires hash+parse validation. Legacy `{ticks}_{identity}.json`
  files are still ingested (parse-validated) for upgrade compatibility but are never
  credited with the hash guarantee.
- Cleanup is a current-master-only two-stage protocol: merge → successful canonical
  save accounting for the fragment → in-memory eligibility → ten-minute grace measured
  from that save (settable `Pit.ChangeFileCleanupGrace`, production default 10 min).
  Original file age no longer counts; restart or master transfer resets eligibility.
  The former age-based delete-before-store path is removed.

#### Live split-master recovery (concept)

- Per-tenure in-memory recovery write set: fragments newly persisted by a master save
  are recorded before being marked clean; entries transfer out per fragment once an
  ordinary change file is locally written, materialized, hash-verified, and parsed.
- Native `FileSystemWatcher` per live writable flagged pit for `Master*.flag`
  (provider-independent longer-name signal, no suffix parsing, no provider API);
  callbacks only debounce and queue one recovery evaluation; construction, master
  acquisition, `Save`, and `Reload` also scan — no polling loop.
- Live loser: stops canonical writes, publishes the write-set/dirty union as ordinary
  small change files, and deletes only the longer flag naming itself after all files
  validate locally. Exact `Master.flag` is never deleted or altered.
- Orphaned signal: only the exact current master retires it, after claimant window
  expiry plus `Pit.OrphanedConflictFlagGrace` (default 10 min) and a locally validated
  `Critical` evidence event. Noncanonical `Object*.pit` copies are never inspected.
- Live authority transfer to another exact process exports the completed tenure's
  write set as change files; same-process reacquisition does not.
- Explicit disposal is a durability boundary: change files first, optional canonical
  save if still exact master, then release of process authority, watcher, and path
  registration. Failure to make accepted fragments durable during explicit shutdown is
  `Critical` and throws. Finalizers perform no filesystem I/O; crash/power loss before
  export remains the explicitly accepted data-loss gap.

#### Recovery diagnostics

- Immutable `Pit.LastRecoveryStatus` plus optional `RecoveryStatusChanged` event; no
  subscriber is required for correctness. Stages: ConflictDetected(Warning),
  RoleDetermined(Information), ChangeFilesPublished(Information),
  Canonicalized(Information), CleanupPending(Debug), Completed(Information),
  DeferredForRetry(Warning), Failed(Error); explicit-shutdown durability failure is
  Critical; `None` is never written.
- Durable events are canonical-JSON `.event` files under the pit's `Events` child via
  OsLib `EventFile`, stem `{UtcTicks}_{ExactProcessIdentity}_{Stage}`. `PitAudit.Read`
  provides filtered read-only access (machine all/local/named; inclusive minimum
  `LogLevel`), ordered by machine, UTC time, and event identity.

### 4. Public Contract & API / Package Changes

- New: `PitInstanceConflictException`, `JsonPitPersistenceException`,
  `RecoveryStage`, `RecoveryRole`, `RecoveryStatus`, `PitAuditEvent`, `PitAudit`,
  `ChangeFile` (naming/validation), `Pit.LastRecoveryStatus`,
  `Pit.RecoveryStatusChanged`, `Pit.ExactProcessIdentity` (public, with
  `ParticipantIdentity` now public), `Pit.ChangeFileCleanupGrace`,
  `Pit.OrphanedConflictFlagGrace`, `Pit.RecoveryDebounce`,
  `PitItems.CompareFragments` (public deterministic comparator),
  `MasterFlagFile.ParticipantOf/IsExactProcessIdentity/ConflictFlags`,
  `ProcessFlagFile.IsProcessWindowActive/ProcessWindowTime`.
- Changed behavior: `Master.flag` owner value is the exact process identity
  (legacy participant-only values are handled during upgrade); `CreateChangeFile`
  returns the created `RaiFile` and writes hashed names; a second live public `Pit`
  per canonical path throws; `Load` throws on bounded retry exhaustion instead of
  returning false; `Reload` no longer throws the "changed without permission"
  exception; `Dispose` performs the full durability sequence.
- Fallback dependency alignment: `OsLibCore 4.0.0`, `RaiUtils 3.13.1`.

### 5. Validation & Acceptance Evidence

Machine configuration is the sole source of truth; all concurrency suites run on real
configured cloud roots (no local substitutes, DI, or environment overrides). Ordinary
suites remain non-parallel (`CollectionBehavior(DisableTestParallelization = true)`).

- Umbrella `RAIkeep.slnx` (excluding the two SSH remote scenarios): **359 passed, 0 failed, 0 skipped**
  (RaiUtils 21, OsLib 80, ImgSeeder 8, pits 13, RaiImage 94, JsonPit 143).
- Recorded full acceptance run (all suites including both SSH scenarios): 361 passed,
  1 failed, 0 skipped. The single failure was `RemoteSyncTests` exhausting its 600 s
  OneDrive propagation window for the Mzansi-bound merged pit while the remaining
  suites concurrently churned the same cloud root — an environmental propagation
  variance, not a contract violation; the scenario passed standalone immediately
  before (1 m 26 s) and immediately after (2 m 0 s), and the split-master scenario
  passed inside the combined run as well.
- New explicit suites (provider OneDrive, machine Nkosikazi):
  `InProcessConcurrencyTests`, `MultiPitInstanceConcurrencyTests`,
  `MultiProcessConcurrencyTests`, `EqualTimestampOrderingTests`,
  `ReadDuringWriteTests`, `SplitMasterRecoveryTests` — 39 passed, 0 failed, 0 skipped.
- Two-server split-master scenario
  (`RemoteCloudConcurrencyTests.TwoServerSplitMaster_LiveLocalLoser_RecoversThroughProviderSyncedConflictSignal`),
  provider OneDrive, machines Nkosikazi (local claimant `Nkosikazi-cr003-82853`) and
  Mzansi (remote claimant `Mzansi-cr003-777777`): local claim reached Mzansi in 6.1 s;
  remote conflict artifacts (`Master.flag` + `Master (1).flag`) written at +9.3 s;
  conflict signal materialized locally and the live loser published its recovery write
  set as validated ordinary change files
  (`639215809514405680_Nkosikazi-cr003-82853_424fbd….json`,
  `639215809514602540_Nkosikazi-cr003-82853_715a00….json`), retired only its longer
  conflict flag, left canonical `Master.flag` naming the remote winner, and wrote 6
  durable audit events — total scenario time 19.3 s. **Passed.**
- Dynamic master/non-master remote scenario (`RemoteSyncTests.RemoteSync_MasterClient_FullScenario`,
  provider OneDrive, Nkosikazi + Mzansi running pits v4.0.0): **passed in 1 m 26 s** —
  pit creation and master claim on Nkosikazi; Mzansi as non-master producing hashed
  change files (canonical→Mzansi sync 5.8 s, change files back 0.0–13.6 s); master
  merge of both entries; exact-PID master transfer to `Mzansi-pits-1978308` after
  simulated ticket expiry (observed locally in 10.0 s); Nkosikazi reading all three
  entries; and the two-stage current-master-only cleanup (files retained through the
  post-save grace, deleted only on the later pass, data integrity preserved).
- Cross-process exact-PID inheritance proven with real separate CLI processes in
  `pits.Tests.LocalCliTicketWindowTests`.

### 6. Upgrade & Consumption Instructions

- Consume `JsonPit 4.0.0` together with `OsLibCore 4.0.0`.
- Applications must hold **one** live `Pit` per canonical pit path per process (via
  their singleton/keyed container) and `Dispose()` it before reopening; a duplicate
  now throws `PitInstanceConflictException` instead of silently misbehaving.
- `Dispose()` of a writable pit now performs the durability export; call it on
  shutdown paths (finalizers intentionally do nothing).
- Treat `JsonPitPersistenceException` from `Load`/`Reload`/`Save`/`Dispose` as an
  operational signal — prior in-memory state is preserved when loading fails.
- Mixed-version fleets: 4.0.0 reads legacy change files, but pre-4.0.0 processes can
  fail on 4.0.0 hashed change files; upgrade all participants of a shared pit
  together (the coordinated release requirement).
