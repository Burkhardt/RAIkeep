# CR075: Structured iorg Inventory and Content Matching

> **Naming Schema:** `CR075_AIA_to_RAIkeep_Iorg_Structured_Inventory_and_Content_Matching.md`  
> **Parent CR:** `CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md`, `CR067_AIA_to_RAIkeep_Support-Video-Extensions-and-Single-File-Organize-in-Iorg.md`  
> **Immutability Rule:** The provider agent must NEVER rename or modify this document filename.

**Date:** 2026-11-02  
**Requesting Agent / PM:** Adele (`7010`, PM AIA Platform) on behalf of AIA Platform and Engenho consumers  
**Target Provider / Repo:** Codex (`7001`, Custodian & Systems Architect) / `Burkhardt/RAIkeep`  
**Status:** Ratified & Dispatched to RAIkeep  
**Target Release:** RAIkeep `v4.5.16`

---

## 1. Objective & Context

### The Consumer Problem
AIA's video ingestion and streaming pipeline (`VideoBakeController`, `ImageController`, and Engenho's `ListVideos` and `ImportVideo` runners) currently encounters fundamental limitations during media reconciliation:
1. `iorg list --json` returns a simple array of filename strings (`["clip1.mov", "clip2.mp4"]`). It supplies no file size, UTC modification timestamp, media classification, or content hash.
2. Consequently, consumers must execute secondary metadata passes (e.g. `Deno.stat` in Engenho). In `VideoBakeController.Bake`, AIA currently compares an existing master's byte size with a remotely listed source's byte size to deduce if they are the same file (violating analyzer rule `RAI002` regarding raw `System.IO.File.Length`).
3. Equal file sizes do **not** prove equal content, and local mirror paths cannot be naively equated across hosts. Furthermore, when re-encoded deliverables or camera imports enter the cloud tree, consumers have no non-destructive way to discover existing duplicates or equivalent visual assets across folder hierarchies.

### The Requested Capabilities
AIA formally adopts and ratifies the two read-only capabilities specified in the draft:

1. **Structured Inventory (`iorg list --long --json`):**
   - Emits structured metadata per file: `Name`, `FullPath`, `RelativePath`, `CloudRelativePath`, `ItemTreePath`, `Extension`, `MediaKind`, `SizeBytes`, `LastModifiedUtc`, `Cloud`, `ResolvedRoot`, `ExecutionHost`, and optional `Sha256`.
   - Directly pipeable to `jq` with zero stdout banner or ANSI pollution.
   - Includes optional `--all-files` (metadata-only census of non-media files) and `--checksum sha256` (streaming hash calculation).

2. **Content Discovery & Duplicate Matching (`iorg duplicates`):**
   - Finds matching media files regardless of filename or extension.
   - Distinct, explicit match modes:
     - `--match bytes` (default): Cryptographically and byte-verified identical (`MatchMode: "Bytes"`, `ByteComparisonVerified: true`).
     - `--match visual` (explicit opt-in, versioned profile `strict-v1`): Visual equivalence across containers/encodings with complete decoded frame comparison; reports `AudioCompared: false`. **Must never be treated as proof of byte identity or authorize replacing canonical masters.**
   - Predictable output contracts:
     - Literal file source $\rightarrow$ JSON array of match records (`[]` if unique).
     - Wildcard selector $\rightarrow$ JSON dictionary mapping root-relative paths to match arrays (unique sources retained as empty arrays).

---

## 2. Desired Behavior & Architectural Constraints

### 2.1 Scope & Path Resolution
- **Explicit Cloud & Root Support:**
  - `--cloud <name> --root <path>` resolves against configured cloud roots from `Os.Config`.
  - `--cloud <name> --app <app> --tenant <subscriber>` preserves standard ImageTree layout.
  - `--root <absolute-directory>` allows offline filesystem testing without a cloud provider.
- **RaiPath / RaiFile Boundary:**
  - All path resolution, metadata inspection, and streaming reads must use `RaiPath` and `RaiFile`.
  - Zero raw `System.IO.File` operations; zero `Os.Config` bypass in integration tests.
  - Remote execution must flow through the typed `IorgCommand` SSH transport.

### 2.2 Byte Comparison Pipeline
1. Enumerate files, collect typed metadata once, reject mismatched lengths before reading bytes.
2. Stream candidate groups through SHA-256 in bounded buffers (no full-file caching in memory).
3. If size and SHA-256 match, perform streaming byte-by-byte confirmation before asserting `ByteComparisonVerified: true`.
4. Output cleanly to stdout; diagnostics to stderr; exit 0 on clean scan (even if 0 matches).

### 2.3 Visual Comparison Pipeline (`strict-v1`)
1. Requires explicit `--match visual --visual-profile strict-v1`.
2. Compares complete decoded sequences (not posters or sampled keyframes).
3. Evaluates normalized decoded fingerprints, followed by SSIM/perceptual metrics where re-encoding occurred.
4. Audio is strictly excluded (`AudioCompared: false`).
5. Memory must be bounded; pipes only; no temporary video files persisted to disk.

### 2.4 Invariants & Guarantees
- **Strictly Read-Only:** Zero writes, renames, deletes, or hardlinks. A match result does not mutate files.
- **Fail-Closed & Truthful:** Incomplete scans, permission failures, or missing tools return non-zero exit codes. Never disguise an aborted scan as an empty match set.
- **Zero Stdout Noise:** JSON output on stdout must be 100% valid JSON with zero banner text or progress spinners. All telemetry goes to stderr.

---

## 3. Requirer Acceptance Criteria & Test Scenarios

| Scenario | Input / Action | Expected Result |
| :--- | :--- | :--- |
| **AC-1: Backward Compatibility** | `iorg list '*.mov' --json` | Returns standard array of filename strings (`["IMG_5443.MOV"]`), unmodified. |
| **AC-2: Structured Inventory** | `iorg list '*.mov' --cloud ICloudDrive --root . --ignore-case --long --json` | Returns JSON array of objects with `Name`, `FullPath`, `RelativePath`, `SizeBytes`, `LastModifiedUtc`, `MediaKind: "Video"`. Pipes cleanly to `jq`. |
| **AC-3: All-Files Census** | `iorg list '*' --all-files --long --json` | Inventories regular files including unrecognized extensions with metadata only; rejects combination with `--checksum`. |
| **AC-4: Single Source Byte Match** | `iorg duplicates 'PLVanguard/IMG_5443.MOV' --cloud ICloudDrive --root . --match bytes --json` | Returns JSON array of matches (`MatchMode: "Bytes"`, `ByteComparisonVerified: true`, `Algorithm: "SHA-256"`). Empty array `[]` if unique. |
| **AC-5: Wildcard Dictionary Output** | `iorg duplicates '*' --cloud OneDrive --app AfricaStage --tenant Nomsa --match bytes --json` | Returns dictionary mapping relative paths to match arrays. Sources with no duplicates appear with empty arrays `[]`. Never collapses to a flat array. |
| **AC-6: Cross-Extension Detection** | File `clip.mov` duplicated as `Archive/clip.mp4` with identical bytes | Matches with `MatchMode: "Bytes"`, ignoring filename and extension differences. |
| **AC-7: Collision / Guard Test** | Files with identical byte size but different content | Size match initiates SHA-256; differing digests reject candidates without byte-compare; returns no match. |
| **AC-8: Visual Strict Isolation** | `iorg duplicates 'clip.mov' --match visual --visual-profile strict-v1 --json` | Reports visual match evidence with `AudioCompared: false` and `ByteComparisonVerified: false`. |
| **AC-9: Error Truthfulness** | Source file missing or path escaping root (`../../`) | Returns non-zero exit code and error on stderr; stdout does not report false `[]`. |

---

## 4. Implementation & Package Target

- **Shared Models:** `OsLib` (`IorgListRequest`, `IorgDuplicateRequest`, typed inventory DTOs).
- **Core Primitives:** `RaiImage` (stream-based hashing, image/video decoding pipes).
- **CLI & Dispatch:** `ImgSeeder` (`iorg list`, `iorg duplicates`, `IorgCommand`).
- **Release Target:** RAIkeep `v4.5.16`.

— Ratified on 2026-11-02 by Adele (`7010`, PM AIA Platform)
