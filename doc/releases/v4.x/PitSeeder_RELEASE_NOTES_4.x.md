# PitSeeder Release Notes 4.x

## 4.5.11

- Release version: `4.5.11`
- Coordination tag: `v4.5.11`

### Highlights
- Coordinated 4.5.11 version alignment; no PitSeeder behavior change.

### Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.11` line.

---

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
- Coordinated release aligned with the 4.5.8 synchronized platform line.
- `pits` CLI list/ls commands, cloud decoupling, provenance tracing, and WWWA help screen parity (CR057/CR058).

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
are introduced in PitSeeder by this patch.

See [Amafu 4.5.4 release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/Amafu_RELEASE_NOTES_4.x.md#454) for the fix and
configuration migration instructions.

---

## 4.5.3

PitSeeder v4.5.3 delivers CR051 multi-account cloud provider resolution:

- **Qualified Cloud Provider Keys**: CLI provider resolution (`pits -c <name>`) accepts any configured cloud account key present in `Cloud` and `DefaultCloudOrder` (e.g. `GoogleDriveRainer`, `GoogleDriveYebo`, `OneDrivePersonal`), matching Amafu multi-account naming.
- **Dependency Alignment**: Aligned with the coordinated 4.5.3 line and updated OsLibCore / JsonPit package references.

Validation and release handoff: [RAIkeep 4.5.3](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#453). Preparation does not publish this package.

---

## 4.5.2

Coordinated 4.5.2 release; runtime behavior is unchanged. Internal package dependencies, where present, align to 4.5.2.

Validation and release handoff: [RAIkeep 4.5.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#452). Preparation does not publish this package.

---

## 4.5.0

4.5.0 uses live JsonPit property deletion and aligned dependencies; pits reports version 4.5.0.

Property deletion now calls the live item's `DeletePropertyPath` directly. JsonPit appends the sparse tombstone internally; CLI syntax and Save boundaries stay the same.

All package and internal dependency versions are aligned to 4.5.0, coordinating live object reference semantics, sparse mutation tracking, and automated release validation gating across the entire RAIkeep platform.

Validation and release handoff: [RAIkeep 4.5.0](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#450). Preparation does not publish this package.

---

## 4.4.8

4.4.8 uses live JsonPit property deletion and aligned dependencies; pits reports version 4.4.8.

Property deletion now calls the live item's `DeletePropertyPath` directly. JsonPit appends the sparse tombstone internally; CLI syntax and Save boundaries stay the same.

All package and internal dependency versions are aligned to 4.4.8. The version intentionally skips C# 4.4.7 to align the next coordinated release with jsonpit-python; Python implementation and publication remain with its maintainer.

Validation and release handoff: [RAIkeep 4.4.8](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#448). Preparation does not publish this package.

---

## 4.4.6

PitSeeder (`pits`) v4.4.6 fulfills **Deliverable A** (Whole-Batch Live ID Preflight) and **Deliverable C** (Receipt Ingestion via Stdin) of [CR049](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md) (*Live ID Validation, ZIP Image Ingestion, and Receipt Persistence*), along with operational storage migration capabilities.

### 1. Fulfillment of CR049 Deliverable C: Standard Input Ingestion (`--source -`)

- **Piped Pipeline Ingestion (C01, C03):** Operators and automated pipelines can pipe JSON or JSON5 receipt documents directly into living pits via standard input:
  ```bash
  cat receipt.json | pits seed ImportRecords --source -
  iorg organize ... --json | pits seed ImageImports --source -
  ```
- **Strict Validation & Error Boundaries:** Standard input ingestion enforces complete schema validation. Empty or malformed input fails fast with non-zero exit and actionable diagnostics, leaving target storage untouched.
- **Typed OsLib Integration:** Native `OsLib` callers can invoke `PitsSeedRequest` with buffered streams without staging intermediate files.

### 2. Fulfillment of CR049 Deliverable A: Whole-Batch Live ID Preflight

- **Atomic Preflight (A01, A02):** `pits seed` validates the entity IDs of every record in an incoming batch before opening a writable Pit or acquiring lock flags. If any entity ID contains `{` or `<`, the entire operation is aborted with exit code `1` and a standard diagnostic to stderr:
  ```text
  error: Entity Id '{AdminPersonId}' contains a prohibited template marker ('{' or '<'). Resolve template placeholders before writing to a Pit.
  ```
- **Zero Partial Commits:** Zero change files, process flags, or destination directories are created when an invalid ID is detected in a batch.
- **Strict Patch Mode (CR047 Integration):** `--require-existing` and `--patch` preflight live ID validity before evaluating existence in the living store.

### 3. Storage Maintenance & Event Archive Migration (`pits maintain`)

- **Automated Archive Migration:** `pits maintain` discovers legacy compaction event files carrying 64-character SHA-256 hash suffixes (`{stem}_{sha256}.event`).
- **Safe In-Place Migration:**
  - `pits maintain`: Reports legacy event files needing migration during read-only inspection.
  - `pits maintain --apply`: Validates payload digests against embedded checksums and safely renames them in-place to clean `{stem}.event` files on the same volume (CR022 compliant).
- **Reduced Cloud Sync Latency:** Resolves synchronization stalls on OneDrive and other cloud drives by shortening file paths in `Events/`.

### 4. 4-Character Change Checksum & Clean Naming

- **Concise Change Signatures:** All mutations committed through `pits` emit change files with a 4-character hex checksum suffix (`{UtcTicks}_{ExactProcessIdentity}_{4charHex}.json`), guarding against partial cloud synchronization.

### 5. Tool & Runtime Alignment

- Aligned with `JsonPit 4.4.6`, `OsLibCore 4.4.6`, and `RaiUtils 4.4.6`.
- Reports `pits v4.4.6`.

---

**Traceability:** This release formally closes Deliverables A and C of [CR049](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md). See [JsonPit release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/JsonPit_RELEASE_NOTES_4.x.md#446) and [RAIkeep release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#446) for platform coordination.

---

## 4.4.5

PitSeeder v4.4.5 implements accepted [`CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md).

### Strict patch mode

- `pits seed <PitName> --source <file> --require-existing` rejects every missing or tombstoned entity ID.
- `--patch` is an exact alias of `--require-existing`.
- The complete payload is parsed and validated before an unflagged, read-only living-state projection is opened.
- Every ID is checked before the normal writable `Pit` is constructed, so rejection creates no process flag, master lease, target directory, or partial write.
- Without either flag, existing upsert behavior remains unchanged.

### Operator feedback and verification

- Successful seeds report `[pits] Successfully committed {N} entity(ies) to Pit '{PitName}'.`
- Strict empty batches fail with a non-zero exit and an explicit diagnostic.
- Sipho's TC-01 through TC-05 are permanent CLI integration tests, supplemented by tombstoned-ID and byte-for-byte no-mutation regressions.

---

## 4.4.4

PitSeeder participates in accepted [`CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR/CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md).

When standard RAIkeep configuration is absent, storage commands now stop before cloud-provider resolution and direct the operator to run `amafu init`. PitSeeder does not duplicate Amafu detection or configuration-writing logic. Existing seed, export, audit, delete, and maintenance behavior remains unchanged.

---

## 4.4.3

PitSeeder and `pits` 4.4.3 implement accepted
[`CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md).

- `pits seed` accepts a single root JSON/JSON5 entity when it contains an exact,
  non-empty string `Id`; `Kind` alone and differently cased `id` fields do not
  satisfy the entity identity contract.
- Existing entity arrays and keyed entity maps remain supported.
- Invalid roots explain all three accepted forms. Non-object array/map entries
  and entities without valid identifiers receive specific diagnostics.
- Parsing, shape checks, entity-identity validation, and protected-attribute
  validation all finish before the destination `Pit` is opened, so rejected
  payloads create no pit directory, process flag, or partial state.

Seed comments, export, audit, deletion, maintenance, event archiving, and clean
process-flag release remain intact. Dependencies align to JsonPit and OsLibCore
4.4.3.

---

## 4.4.2

PitSeeder and `pits` 4.4.2 implement the CLI boundary of accepted
[`CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
and interoperate with accepted
[`CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR041_jsonpit_to_RAIkeep_Restore-Clean-Change-Filenames.md).

- `pits seed` parses and validates every input object before opening the target
  pit, rejecting client-supplied `Modified` or `Deleted` without flags,
  directories, or partial state.
- `pits delete-property` emits a sparse tombstone fragment and rejects `Id`,
  `Modified`, or `Deleted`; callers use `delete-item` for lifecycle deletion.
- Domain exceptions produce concise CLI errors and nonzero exit status.
- Maintenance discovers, merges, receipts, and cleans both clean CR041 and
  legacy SHA-suffixed change artifacts during rolling upgrades.

Seed, export, audit, temporal projection, event archiving, and clean process-flag
release remain intact. Dependencies align to JsonPit and OsLibCore 4.4.2.

---

## 4.4.1

PitSeeder and `pits` 4.4.1 participate in the synchronized eight-package
delivery of accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
They implement accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).

Seed, export, audit, delete, maintenance, JSON5-comment, and clean-exit
process-flag behavior remain intact. Fallback dependencies and CLI version
output align to 4.4.1. A misplaced reserved verb now exits `2` with an
actionable command-first correction before pit/filesystem access, and version
flags take immediate precedence.

---

## 4.4.0

PitSeeder and `pits` 4.4.0 join the synchronized CR036 suite. In response to
the accompanying Zébio/Vesco request, `pits seed` now accepts JSON5 line or
block comments before the root array/map. Malformed payloads remain failures.

Fallback dependencies align to `JsonPit 4.4.0` and `OsLibCore 4.4.0`.

---

## 4.3.2

PitSeeder and `pits` 4.3.2 participate unchanged in the coordinated
seven-package RAIkeep v4.3.2 delivery of accepted
[CR027](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR027_AIA_to_RAIkeep_ClassDiagram_Generalization_and_SetSuperClass.md).
Fallback dependency and CLI versions align on 4.3.2. CR024 clean-exit process
flag behavior remains unchanged. Publication remains behind RAI's manual
release-chain gate.

---

## 4.3.1

PitSeeder and `pits` 4.3.1 participate unchanged in the coordinated
seven-package RAIkeep v4.3.1 delivery of accepted
[CR026](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR026_AIA_to_RAIkeep_Diagram_Builder_Revision_Fidelity_and_Reference_Stereotypes.md).
Fallback dependency and CLI versions align on 4.3.1. CR024 clean-exit process
flag behavior remains unchanged. Publication remains behind RAI's manual
release-chain gate.

---

## 4.3.0

PitSeeder and `pits` 4.3.0 deliver accepted
[CR024 process-flag self-cleanup](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md).

- Finite normal, exceptional, Ctrl+C, and process-exit paths converge on
  deterministic disposal of the exact owned PID-specific flag.
- `--retain-window` remains a documented 4.x compatibility exception and is
  scheduled for removal in the next major release.
- Master leases and crash/TTL maintenance behavior are unchanged.

The unpublished 4.2.11 preparation is superseded. Package and CLI versions align
on 4.3.0. Publication remains behind RAI's manual release gate.

---

## 4.2.11

> **Superseded before publication.** This prepared package line was not released;
> its changes are carried into v4.3.0.

PitSeeder 4.2.11 implements the CLI portion of accepted
[CR024](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md).

- Every default finite `pits` call disposes its tracked pits and removes the
  exact PID-specific process flags it owns after the JsonPit durability boundary.
- Normal completion, exception unwind, Ctrl+C, and process-exit cleanup converge
  on the same ownership-safe release path.
- `--retain-window` remains an explicit v4.2.11 compatibility exception and is
  scheduled for removal in the next major release.
- `Master.flag` remains untouched; crashes and forced termination continue to
  rely on TTL detection and explicit maintenance pruning.

Command-level tests prove normal and exceptional cleanup, twenty sequential
finite invocations with zero residual flags, deliberate retention, and master
lease preservation.

---

## 4.2.10

PitSeeder 4.2.10 exposes JsonPit's RAI-authorized recovery-event compaction
through the operational CLI.

- `pits maintain (<PitName> | --wwwa) --archive-events --json` is a strictly
  non-mutating preview of the exact archive name, UTC range, selected count, and
  deferred evidence.
- Adding `--apply` creates the immutable same-directory archive and retires only
  exact validated loose copies.
- `pits audit` transparently reads remaining loose events and archive entries
  with its established machine/severity filters and deterministic ordering.
- Corrupt archives, invalid events, and conflicting event identities produce
  diagnostics and a nonzero audit result without deleting evidence.

Single-pit and WWWA command-level tests cover preview, apply, missing-pit
non-creation, archive visibility through audit, and exact JSON reporting.
Fallback references align to `JsonPit 4.2.10` and `OsLibCore 4.2.10`; the CLI
reports `pits v4.2.10`.

---

## 4.2.9

PitSeeder 4.2.9 implements the CLI correction required by accepted
[CR022](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md)
while retaining accepted [CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md)
maintenance behavior.

- `pits maintain` validates the resolved subscriber root before constructing any
  `Pit` and fails without mutation when that root is absent.
- Single-pit maintenance requires the canonical `<PitName>.pit` file to exist.
- WWWA maintenance requires at least one canonical pit; missing peers are
  reported as deferred and are not materialized.
- Report-only maintenance of a wrong or partial tree leaves directory inventory
  and timestamps unchanged.

An applied maintenance run that includes `--prune-process-flags` or
`--repair-legacy-extensions` may intentionally retire many obsolete files.
OneDrive can present its mass-deletion confirmation for that explicit cleanup;
operators should compare the reported removal counts with the `pits maintain`
result before confirming the provider action. Canonical `.pit` files and
unexpired/unvalidated evidence are not cleanup targets.

Fallback references align to `JsonPit 4.2.9` and `OsLibCore 4.2.9`; the CLI
reports `pits v4.2.9`.

---

## 4.2.8

PitSeeder 4.2.8 implements the CLI portion of accepted
[CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md).

- Adds `pits maintain (<PitName> | --wwwa)` with a non-mutating report-only default.
- `--apply` performs JsonPit's validated receipt-backed maintenance and emits human or `--json` results.
- Aged process-window removal requires the additional `--prune-process-flags --older-than <duration>` authorization.
- Content-valid extensionless process-flag/event repair requires the additional `--repair-legacy-extensions` authorization.
- Maintenance handles WWWA in `Person`, `Object`, `Place`, `Activity` order and suppresses disposal recovery publication so retired changes are not recreated.
- Existing seed, export, point-in-time export, audit, and delete behavior remains compatible.

Fallback references align to `JsonPit 4.2.8` and `OsLibCore 4.2.8`; the CLI reports
`pits v4.2.8`.

---

## 4.2.7

PitSeeder participates in the coordinated RAIkeep 4.2.7 release implementing
accepted [CR020](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md).

- Aligns fallback dependencies on `JsonPit 4.2.7` and `OsLibCore 4.2.7`.
- The `pits` CLI behavior is unchanged from 4.2.6.
- The CLI reports `pits v4.2.7` through its existing version boundary.

Tagging and NuGet publication remain behind RAI's manual release gate.

---

## 4.2.6

Coordinated dependency release for accepted CR019. `pits` adopts the complete
4.2.6 package line; CLI behavior is unchanged from 4.2.5.

---

## 4.2.5

Implements accepted CR017 point-in-time export.

- Adds `--at <timestamp>` to single-pit and WWWA exports through both `--json`
  and `--out-dir`.
- Requires an explicit `Z` or numeric UTC offset and evaluates history
  inclusively at the requested instant.
- Uses JsonPit's established historical projection, tombstone, deletion-wall,
  resurrection, and ordering rules rather than introducing a second algorithm.
- Emits strict `{ "_export": { "at", "exported" }, "data": ... }` JSON only
  when `--at` is present; no-`--at` output retains its established root shape.
- Projects the four WWWA pits independently, then performs existing one-level
  resolution. Missing targets are omitted from the lookup while source
  references remain safely unresolved.
- Keeps established output filenames unchanged and reports `pits v4.2.5`.
- Aligns fallback dependencies on JsonPit and OsLibCore 4.2.5.

Release verification: 37 PitSeeder Release tests passed, including 14 focused
CR017 cases covering parsing, temporal boundaries, deletion, resurrection,
late history, filenames, envelopes, and WWWA resolution.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

---

## 4.2.4

Coordinated dependency release for accepted CR016.

- Aligns fallback dependencies on JsonPit and OsLibCore 4.2.4.
- Preserves CR015 `delete-property` and `delete-item` behavior unchanged.
- CLI syntax and Nerd Font help behavior remain unchanged.
- Reports `pits v4.2.4` through the CLI version boundary.

Release verification: 23 PitSeeder Release tests passed.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

---

## 4.2.3

Implements the PitSeeder portion of accepted CR015.

- Adds `pits delete-property <PitName> <ItemId> <PropertyPath>` with explicit
  dot-delimited nested paths.
- Adds `pits delete-item <PitName> <ItemId>` using JsonPit's established item
  tombstone.
- Both commands use the existing pit-root/configured-cloud resolution,
  persistence, and process-window release boundaries.
- `-n` remains `--nologo`; it does not suppress saving or flushing.
- Missing pits/items, malformed paths, unknown options, and invalid positional
  counts return nonzero results with contextual command guidance.
- Reports `pits v4.2.3` through the CLI version boundary.

RAI retains the manual coordinated release gate; no tag or publication is
authorized by these notes.

Release verification: 23 PitSeeder Release tests passed, including three added
CR015 live-CLI deletion and validation scenarios.

---

## 4.2.2

Coordinated dependency release for the seven-package RAIkeep 4.2.2 line.

- Aligns fallback dependencies on JsonPit and OsLibCore 4.2.2.
- Retains the 4.2.1 Nerd Font provider and numbered-option glyphs, Blink
  stylesheet guidance, and clipping tolerance.
- Retains the command-first and compatible 4.x legacy `pits` behavior.
- Reports `pits v4.2.2` through the CLI version boundary.
- Its package-owned entry-point tests invoke the managed CLI through
  `OsLib.PitsCommand.ForManagedAssembly(...)`; its `--version` case is the
  CR014.1 real-CLI smoke check. OsLib tests the transport contract and does not
  duplicate pit behavior.

Released as part of the coordinated RAIkeep v4.2.2 release.

Release verification: 20 PitSeeder Release tests passed.

---

## 4.2.1

CLI-only maintenance release based on the published RAIkeep 4.2.0 libraries.

- Uses cloud-provider initials and numbered-option glyphs that are embedded in
  `JetBrainsMonoNLNerdFontPropo-Regular`, avoiding fallback-font width
  differences in help output.
- Reserves two terminal cells at the end of help lines to tolerate proportional
  Nerd Font metrics and renderers such as Blink.
- Reports `pits v4.2.1` through the CLI version boundary.

Package dependencies remain `JsonPit 4.2.0` and `OsLibCore 4.2.0`. No library
package or umbrella version is changed by this release.

Release verification: 20 PitSeeder Release tests passed, and the package-only
build and package metadata were verified against the published 4.2.0
dependencies.

---

## 4.2.0

Coordinated dependency release for the seven-package RAIkeep 4.2 line.

- Aligns fallback package dependencies on JsonPit and OsLibCore 4.2.0.
- Retains the command-first and compatible 4.x legacy `pits` behavior.
- Reports `pits v4.2.0` through the CLI version boundary.

No other PitSeeder CLI behavior change is introduced after 4.1.0.

Release verification: 20 PitSeeder Release tests passed.

---

## 4.1.0

Coordinated dependency release for the CR008 RAIkeep 4.1 line.

- Aligns fallback package dependencies on JsonPit and OsLibCore 4.1.0.
- Retains the command-first and compatible 4.x legacy `pits` behavior introduced
  in 4.0.1.
- No PitSeeder CLI behavior changes are introduced by this release.

---

## 4.0.1

**Date:** 2026-08-10
**Author / Delivering Agent:** RAIkeep Dev Agent
**Delivered Version:** v4.0.1
**Target Consumers:** AfricaStage, AIA
**Status:** Prepared — publication approval pending

### 1. Summary

PitSeeder v4.0.1 adds command-first `seed`, `export`, and `audit` interfaces to
`pits`. Established flat seed/export invocations continue to work during the
`4.x` transition, while the recent audit flag family moves directly to the new
command surface.

### 2. Resolved Change Requests (CRs)

- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — implements contextual subcommands and isolated operation options for `pits`.

### 3. Root Cause Analysis & Technical Resolution

The flat parser inferred its operation from combinations of `-s`, `-e`,
`--json`, `--wwwa`, and `--events`. That made unrelated options appear together
and allowed invalid combinations to reach late execution-intent checks.

The v4.0.1 entry point now selects the command parser only when the first token
is `seed`, `export`, or `audit`. All other input follows the established parser.
Both paths normalize into the existing execution handlers; no second seeding,
exporting, or auditing implementation was introduced.

Command validation now rejects unknown, missing, mutually exclusive, and
out-of-scope options before filesystem or JsonPit work begins. Contextual help is
available through `pits <command> --help`.

### 4. Public Contract & API / Package Changes

Preferred syntax:

```text
pits seed (<PitName> | --wwwa) --source <file-or-directory>
pits export (<PitName> | --wwwa) (--out-dir <dir> | --json)
pits audit (<PitName> | --wwwa) [--machine <filter>] [--level <severity>] [--json]
```

- `--json` remains available for machine-readable audit output.
- `-c`/`--cloud` accepts only providers present in `Os.Config.DefaultCloudOrder`
  with a non-empty `Os.Config.Cloud` path. A provider path alone no longer makes
  that provider selectable, and matching remains case-insensitive.
- Top-level help presents those providers in configured order, marks the first
  as the configured default, and uses the filled number glyph for the selected
  provider. The resolved root appears once on `-r`/`--pitroot`; the redundant
  second PitRoot status line was removed.
- `audit --wwwa` aggregates the four WWWA event directories and preserves
  deterministic machine/time/event ordering.
- `--events`, `--event-machine`, and `--event-level` are intentionally not part
  of legacy compatibility. They fail with guidance to `audit`, `--machine`, and
  `--level`.
- Existing flat seed/export syntax remains supported throughout `4.x`.
- The legacy parser is scheduled for removal in `5.x.x`; see
  [`CLI-PARSER-TRANSITION-4.x-TO-5.x.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CLI-PARSER-TRANSITION-4.x-TO-5.x.md).
- Startup banner rules no longer use repeated equals characters.

### 5. Validation & Acceptance Evidence

- `PitSeeder.Tests`: **20 passed, 0 failed, 0 skipped**.
- Executable-process coverage proves command seed/export routing, legacy export
  equivalence, target/output mutual exclusion, contextual help, command-only
  audit migration, WWWA audit aggregation, JSON filtering, and zero audit
  filesystem side effects.
- Process-level version coverage proves `pits --version` emits `pits v4.0.1`.
- Debug builds complete with zero warnings and zero errors.

### 6. Upgrade & Consumption Instructions

1. Update the coordinated RAIkeep tool line to v4.0.1 after publication approval.
2. Prefer the command syntax above for new scripts.
3. Existing seed/export scripts may migrate during `4.x`.
4. Replace audit flags immediately:
   `--events` → `audit`, `--event-machine` → `--machine`, and
   `--event-level` → `--level`.
5. Independently validate operational scripts and record the requester-led
   CR006 Accepted/Rejected evaluation.

---

## 4.0.0

**Date:** 2026-08-05  
**Author / Delivering Agent:** RAIkeep Dev Agent  
**Delivered Version:** v4.0.0  
**Target Consumers:** AIA, AfricaStage, RAIkeep operators  
**Status:** Implemented — coordinated 4.0.0 line; NuGet publication pending release authorization

---

### 1. Summary

`pits` 4.0.0 aligns the CLI with the coordinated JsonPit concurrency contract: it adds
the strictly read-only `--events` audit mode for JsonPit recovery events and routes
finite CLI shutdown through JsonPit's full durability boundary.

### 2. Resolved Change Requests (CRs)

- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) — PitSeeder share of the coordinated v4.0.0 work (`pits --events` audit mode; CR003 disposal boundary for finite CLI runs).

### 3. Root Cause Analysis & Technical Resolution

- Recovery diagnostics were previously invisible to operators. `pits --events` now
  reads a pit's durable audit events through JsonPit's `PitAudit` (backed by OsLib's
  `EventDirectory`) **without** opening a `Pit`, creating a process flag, touching
  `Master.flag`, merging change files, or writing an audit event. Audit routing runs
  before any `Pit` construction.
- Finite CLI runs previously only tombstoned their activity window. They now dispose
  each opened `Pit` through the CR003 durability boundary (change-file export first,
  optional canonical save while still exact master, then window/watcher/registry
  release). `--retain-window` still opts out and keeps the activity window until its
  normal timeout.

### 4. Public Contract & API / Package Changes

- New: `pits -r <root> <PitName> --events`
  - `--event-machine all|local|<machine>` (default `all`)
  - `--event-level <level>` — case-insensitive inclusive minimum
    (`Trace|Debug|Information|Warning|Error|Critical`, default `Trace`)
  - with `--json`: emits the filtered events as a JSON array; otherwise human-readable
    lines ordered deterministically by machine, UTC time, and event identity.
  - Audit mode requires one positional pit name; `--wwwa --events` is rejected
    (outside CR003). Invalid levels and missing values produce clear CLI errors with
    zero side effects.
- Package/tool version 4.0.0; consumes `JsonPit 4.0.0` and `OsLibCore 4.0.0`.

### 5. Validation & Acceptance Evidence

- `pits.Tests`: 13 passed, 0 failed, 0 skipped — including the new
  `EventsAuditModeTests` (all/local/named-machine filters, inclusive severity,
  case-insensitivity, deterministic ordering, JSON parseability, and before/after
  filesystem snapshots proving zero side effects) and the updated
  `LocalCliTicketWindowTests`, which exercise real separate CLI processes and prove
  exact-PID master inheritance after the previous CLI process released its window.
- Deployed and verified on the configured remote node Mzansi (`pits v4.0.0`,
  self-contained linux-x64), including seeding against the OneDrive-backed root.

### 6. Upgrade & Consumption Instructions

- Install/update the `pits` tool to 4.0.0 on **every** machine sharing a pit
  (pre-4.0.0 binaries can fail when merging 4.0.0 hashed change files).
- Inspect recovery activity with, for example:
  `pits -n -r <root> Person --events --event-level warning`
  or `pits -n -r <root> Person --events --json | jq`.
