# Release Notes: OsLib (OsLibCore) v3.13.2

**Date:** 2026-08-05  
**Author / Delivering Agent:** RAIkeep Dev Agent  
**Delivered Version:** v3.13.2  
**Target Consumers:** JsonPit, PitSeeder, AIA, AfricaStage  
**Status:** Implemented — coordinated 3.13.2 line; NuGet publication pending release authorization

---

## 1. Summary

OsLib supplies the shared filesystem primitives required by the coordinated JsonPit
concurrency contract: a no-delete/no-rename `TextFile.Save`, deterministic canonical
JSON with SHA-256 hashing, and generic create-once event files with stateless
directory aggregation. OsLib owns storage mechanics only; it imposes no event-content
schema and never interprets JsonPit fields.

## 2. Resolved Change Requests (CRs)

- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) — OsLib share of the coordinated v3.13.2 concurrency work (agreed `TextFile.Save` contract, canonical JSON, `EventFile`/`EventDirectory`).

## 3. Root Cause Analysis & Technical Resolution

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

## 4. Public Contract & API / Package Changes

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

## 5. Validation & Acceptance Evidence

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

## 6. Upgrade & Consumption Instructions

- Consume `OsLibCore 3.13.2`. No call-site changes are required.
- Callers that relied on `Save(backup: true)` *moving* the previous file must note it
  now copies; the original pathname always survives a save.
- Durable audit producers: construct `new EventFile(rootPath, logicalStem, contentObject)` —
  the constructor performs the create-once write. Consumers read via
  `EventDirectory.Events(rootPath)`.
