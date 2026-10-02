# Release Notes: JsonPit v4.4.6

JsonPit v4.4.6 fulfills **Deliverable A** of [CR049](CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md) (*Live ID Validation, ZIP Image Ingestion, and Receipt Persistence*) along with platform-ratified storage refinements for cloud-synchronized file integrity and naming hygiene.

## 1. Fulfillment of CR049 Deliverable A: Prohibit Template Markers in Live Entity IDs

- **Canonical Identity Enforcement (A01, A04):** Public write boundaries (`Pit.Add`, `Pit.AddRange`, and `PitItem.Id` property mutations) reject entity IDs containing unresolved template markers (`{` or `<`). Attempting to commit placeholder identities throws `ArgumentException` before mutating memory or disk. Missing, whitespace-only, or non-string IDs are rejected upfront.
- **Atomic Batch Preflight (A02):** Multi-record writes validate all entity IDs before mutating the in-memory store or staging change files. If any entity fails validation, zero records are committed.
- **Ordinary Fields Unrestricted (A03):** Template markers inside non-ID fields (`Name`, `Note`, payloads) remain unrestricted.
- **Historical Preservation & Clean Recovery (A05):** Legacy records containing placeholder IDs remain readable, exportable, and queryable. Tombstone deletions (`Deleted = true`) and `AddHistorical` remain permitted to allow operators to purge historical anomalies, while live re-insertion of invalid IDs is blocked.

## 2. Cloud-Safe 4-Character Checksum for ChangeFiles

- **Integrity Without Path Bloat:** Change files now use a concise 4-character hex checksum suffix: `{UtcTicks}_{ExactProcessIdentity}_{4charHex}.json`. Derived from the first 4 characters of the SHA-256 payload digest, this checksum reliably detects partial cloud synchronization (e.g. OneDrive, Dropbox, Google Drive, iCloud) without inflating path lengths or exceeding filesystem limits.
- **Backward-Compatible Readers:** The engine verifies the 4-character checksum upon reading, while continuing to load and validate legacy 64-character SHA-suffixed change files. Corrupted or truncated files fail cleanly before polluting engine state.

## 3. Clean EventFile Naming

- **Concise Logical Stems:** Event compaction archives no longer embed 64-character SHA-256 hashes in filenames. Events are emitted with clean logical stems: `{LogicalStem}.event` (e.g. `20261001-120000.event`), keeping directory entries short and cloud-friendly.

## 4. In-Place Legacy EventFile Migration

- **Automated Archive Migration:** Maintenance operations via `pits maintain --apply` (and `JsonPit.InspectLegacyExtensions`) locate legacy `{stem}_{sha256}.event` archives, verify their payload integrity, and rename them in-place to clean `{stem}.event` files on the same volume (honoring CR022 cloud-safe sibling guarantees).
- **Multi-Version Coexistence:** Unmigrated legacy event files continue to be recognized and replayed seamlessly by both C# `JsonPit` and Python `jsonpit`.

## 5. Architectural & API Cleanups

- **Removal of Obsolete `Item` Class:** The deprecated legacy `Item` class in `JsonPit.cs` has been completely deleted in favor of the strongly typed, polymorphic `PitItem` domain model.
- **Process-Monotonic Timestamps:** Enforces monotonic timestamps so high-frequency mutations within a process retain unique, ordered change file stems.

---

**Traceability:** This release formally closes Deliverable A of [CR049](CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md). Package versions and fallback dependencies align at 4.4.6 across the entire platform. See [RAIkeep release notes](RAIkeep_RELEASE_NOTES_4.4.6.md) for umbrella coordination.
