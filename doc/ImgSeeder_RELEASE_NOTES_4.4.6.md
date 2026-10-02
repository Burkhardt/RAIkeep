# Release Notes: ImgSeeder v4.4.6

ImgSeeder (`iorg`) v4.4.6 fulfills **Deliverable B** of [CR049](CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md) (*ZIP Image Ingestion and JSON Receipts*), implementing automated media ingestion, machine-readable receipt emission, asynchronous native decompression, and structured EXIF inspection.

## 1. Fulfillment of CR049 Deliverable B: ZIP Archive Ingestion (`iorg organize`)

- **Local & HTTPS Ingestion (B01, B05):** Ingests photo collections directly from local `.zip` files (`--source`) or HTTPS URLs (`--source-url`) into designated tenants and ImageTree structures.
- **Path-Traversal Defense (B02):** Rejects any archive containing path traversal sequences (`..`), absolute paths, or symbolic links during archive preflight before extracting any files.
- **Non-Silent Collision Defense (B03):** Compares candidate targets against existing files. Identical bytes are marked `Unchanged`; differing content generates a collision error. Files are never silently overwritten.
- **Asynchronous Native Extraction:** On macOS and Linux/Ubuntu, decompression is dispatched to the native `unzip` tool asynchronously through `OsLib` (`RaiSystem`), executing into OS temporary storage without blocking caller threads.
- **Preserved Archives:** The source ZIP archive remains untouched after ingestion.

## 2. Authoritative `Class: "ImageImport"` Receipts (B04, B06)

- **Machine-Readable JSON Output:** When `--json` is specified, `iorg organize` outputs strictly valid JSON on `stdout` (with logging and diagnostics sent to `stderr`).
- **Complete Ingestion Manifest:** The receipt documents overall status (`Completed`, `Partial`, `Failed`), summary counts (`Copied`, `Unchanged`, `Skipped`, `Failed`), source metadata, and per-file mappings:
  - Source entry path in the archive
  - Derived entity identity (`ItemId`)
  - Target relative path within `ItemIdTree8x2`
  - Extracted EXIF metadata and final copy status
- **Piped JsonPit Ingestion (CR049 Deliverable C):** Receipts can be piped directly into `pits seed` or `jpit` via standard input (`--source -`).

## 3. Structured EXIF Metadata Extraction

- **Selective & Comprehensive Selectors:** Supports `--exif '*'` or specific tag/group selectors across both `iorg list` and `iorg organize`.
- **Typed DateTimeOffset:** Embedded date and offset pairs are normalized to ISO-8601 `DateTimeOffset`.
- **Field Grouping & Exact Rationals:** Exposure, lens, focal plane, and camera settings are grouped into structured properties while retaining exact rational values.

## 4. Cloud-Safe CR022 Placement

- All final image writes occur in-place on the destination drive, strictly observing CR022 rules against moving temporary files across volume boundaries into cloud folders.

---

**Traceability:** This release formally closes Deliverable B of [CR049](CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md). See [PitSeeder release notes](PitSeeder_RELEASE_NOTES_4.4.6.md) and [RAIkeep release notes](RAIkeep_RELEASE_NOTES_4.4.6.md) for platform coordination.
