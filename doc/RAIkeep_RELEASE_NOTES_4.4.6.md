# Release Notes: RAIkeep v4.4.6

RAIkeep v4.4.6 implements [CR049](CR/CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md), incorporating Rainer's live-ID validation, ZIP ingestion, EXIF inspection, and storage filename optimization decisions.

## Live IDs and stdin receipts

JsonPit rejects `{` and `<` inside IDs at live write boundaries, including direct library calls and complete batches. Ordinary field values remain unrestricted by this rule. Historical records remain readable/exportable and can be explicitly deleted, while live re-insertion fails. PitSeeder validates the whole input before writable Pit creation, including strict patch mode. `pits seed <PitName> --source -` accepts explicit standard input.

## Storage Filename Refinements & Cloud Sync Optimization

- **ChangeFiles (4-Character Checksum):** Restored a concise 4-character hex checksum suffix (`{UtcTicks}_{ExactProcessIdentity}_{4charHex}.json`). This provides reliable cloud-sync integrity against partial writes without inflating path lengths or causing synchronization bottlenecks on cloud providers like OneDrive.
- **EventFiles (Clean Logical Naming):** Removed the 64-character SHA-256 hash suffix from compaction event filenames, standardizing on clean `{LogicalStem}.event` files.
- **Automated Event Migration:** `pits maintain --apply` automatically discovers legacy `{stem}_{sha256}.event` archives, verifies payload digests, and migrates them in-place to clean names.
- **Engine Hygiene:** Removed the obsolete `Item` class from `JsonPit` in favor of polymorphic `PitItem`.

## ZIP image imports

`iorg organize` accepts local ZIP files or direct HTTPS URLs and returns an authoritative `Class: "ImageImport"` receipt. Complete preflight protects final destinations from invalid paths/IDs and naming collisions. Existing identical bytes are `Unchanged`; different content is never silently overwritten. Partial copy failures report their actual outcomes.

On macOS/Ubuntu, native Info-ZIP extraction runs through asynchronous `RaiSystem` execution into temporary storage. The .NET import API dispatches the entire operation off the calling thread. Missing tools, insufficient temporary disk space, corrupt archives, and cancellation fail explicitly. Final images are written directly into their ImageTree paths, never moved from temp into a CloudDrive. Size/count/download-time limits are optional and have no application-imposed defaults.

## EXIF and downstream processing

Both `iorg list` and `organize` support `--exif '*'` and comma-separated selectors. Matching embedded date/offset pairs become `DateTimeOffset` values under the original date names. Thumbnail, lens, focal-plane, and exposure fields are grouped; rationals retain exact numerator/denominator and numeric value. Missing/invalid conversion inputs remain in `Unconverted` with diagnostics. No `Captured` alias or file/local-timezone fallback is introduced.

The [ImgSeeder README](https://github.com/Burkhardt/ImgSeeder/blob/main/README.md) documents ZIP ingestion, actual filename normalization, jq inspection, and buffering/checking the receipt before `pits` or `jpit` ingestion.

## Validation and release coordination

Native extraction has been exercised on macOS and Ubuntu/Mzansi. Automated coverage includes core/CLI marker validation, historical compatibility, empty/malformed stdin, receipt persistence, ZIP traversal and collisions, repeated imports, partial failures, HTTPS error handling, strict JSON stdout, native cancellation, and EXIF conversion/selection.

Final full-stack test results are recorded in the release handoff. This document does not itself assert that validation or publication has completed. All nine package versions and fallback dependencies align at 4.4.6. Rainer runs `scripts/release-chain.sh 4.4.6`; no tags, pushes, or publication are performed during preparation. Adele owns Python implementation/parity and its release.
