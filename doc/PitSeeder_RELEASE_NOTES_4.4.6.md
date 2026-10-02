# Release Notes: PitSeeder v4.4.6

PitSeeder (`pits`) v4.4.6 fulfills **Deliverable A** (Whole-Batch Live ID Preflight) and **Deliverable C** (Receipt Ingestion via Stdin) of [CR049](CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md) (*Live ID Validation, ZIP Image Ingestion, and Receipt Persistence*), along with operational storage migration capabilities.

## 1. Fulfillment of CR049 Deliverable C: Standard Input Ingestion (`--source -`)

- **Piped Pipeline Ingestion (C01, C03):** Operators and automated pipelines can pipe JSON or JSON5 receipt documents directly into living pits via standard input:
  ```bash
  cat receipt.json | pits seed ImportRecords --source -
  iorg organize ... --json | pits seed ImageImports --source -
  ```
- **Strict Validation & Error Boundaries:** Standard input ingestion enforces complete schema validation. Empty or malformed input fails fast with non-zero exit and actionable diagnostics, leaving target storage untouched.
- **Typed OsLib Integration:** Native `OsLib` callers can invoke `PitsSeedRequest` with buffered streams without staging intermediate files.

## 2. Fulfillment of CR049 Deliverable A: Whole-Batch Live ID Preflight

- **Atomic Preflight (A01, A02):** `pits seed` validates the entity IDs of every record in an incoming batch before opening a writable Pit or acquiring lock flags. If any entity ID contains `{` or `<`, the entire operation is aborted with exit code `1` and a standard diagnostic to stderr:
  ```text
  error: Entity Id '{AdminPersonId}' contains a prohibited template marker ('{' or '<'). Resolve template placeholders before writing to a Pit.
  ```
- **Zero Partial Commits:** Zero change files, process flags, or destination directories are created when an invalid ID is detected in a batch.
- **Strict Patch Mode (CR047 Integration):** `--require-existing` and `--patch` preflight live ID validity before evaluating existence in the living store.

## 3. Storage Maintenance & Event Archive Migration (`pits maintain`)

- **Automated Archive Migration:** `pits maintain` discovers legacy compaction event files carrying 64-character SHA-256 hash suffixes (`{stem}_{sha256}.event`).
- **Safe In-Place Migration:**
  - `pits maintain`: Reports legacy event files needing migration during read-only inspection.
  - `pits maintain --apply`: Validates payload digests against embedded checksums and safely renames them in-place to clean `{stem}.event` files on the same volume (CR022 compliant).
- **Reduced Cloud Sync Latency:** Resolves synchronization stalls on OneDrive and other cloud drives by shortening file paths in `Events/`.

## 4. 4-Character Change Checksum & Clean Naming

- **Concise Change Signatures:** All mutations committed through `pits` emit change files with a 4-character hex checksum suffix (`{UtcTicks}_{ExactProcessIdentity}_{4charHex}.json`), guarding against partial cloud synchronization.

## 5. Tool & Runtime Alignment

- Aligned with `JsonPit 4.4.6`, `OsLibCore 4.4.6`, and `RaiUtils 4.4.6`.
- Reports `pits v4.4.6`.

---

**Traceability:** This release formally closes Deliverables A and C of [CR049](CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md). See [JsonPit release notes](JsonPit_RELEASE_NOTES_4.4.6.md) and [RAIkeep release notes](RAIkeep_RELEASE_NOTES_4.4.6.md) for platform coordination.
