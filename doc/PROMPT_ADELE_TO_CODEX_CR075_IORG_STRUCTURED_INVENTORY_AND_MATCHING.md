# Dispatch Prompt: Adele (AIA PM) to Codex (RAIkeep Agent) — CR075

```text
You are Codex, Lead Systems Architect and Custodian for RAIkeep (Burkhardt/RAIkeep).

Adele, Product Manager for AIA, has ratified Change Request CR075 on behalf of AIA Platform Governance, Engenho, and Dr. Rainer Burkhardt (RAI).

Authoritative Specification:
doc/CR075_AIA_to_RAIkeep_Iorg_Structured_Inventory_and_Content_Matching.md
(Parent: CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md, CR067_AIA_to_RAIkeep_Support-Video-Extensions-and-Single-File-Organize-in-Iorg.md)

### Mission Objective:
Implement Deliverables in RAIkeep (OsLib, RaiImage, and ImgSeeder / iorg), targeting Release v4.5.16:

1. Structured Inventory in ImgSeeder (`iorg list --long --json`):
   - Add `--long` flag to `iorg list` when combined with `--json`.
   - Output an array of structured JSON objects:
     {
       "Name": string,
       "FullPath": string,
       "RelativePath": string,
       "CloudRelativePath": string?,
       "ItemTreePath": string?,
       "Extension": string,
       "MediaKind": "Image" | "Video" | null,
       "SizeBytes": long,
       "LastModifiedUtc": string,
       "Cloud": string?,
       "ResolvedRoot": string,
       "ExecutionHost": string,
       "Sha256": string?
     }
   - Support optional `--all-files` (metadata census of all files) and `--checksum sha256`.
   - Preserve zero-stdout-noise invariant: pure JSON on stdout, all diagnostics to stderr.
   - Preserve existing `list --json` (filename strings) backwards compatibility.

2. Content Discovery & Deduplication (`iorg duplicates`):
   - Implement `iorg duplicates <FileOrPattern> <root-options> [--match bytes|visual] [--ignore-case] [--json]`:
     - Default `--match bytes`: Streaming SHA-256 + streaming byte confirmation.
     - Opt-in `--match visual --visual-profile strict-v1`: Complete decoded sequence comparison via RaiImage pipes (FFmpeg/ImageMagick), reporting AudioCompared: false.
   - Output Contract:
     - Literal file source: returns JSON array of match records ([] if unique).
     - Wildcard pattern: returns JSON dictionary mapping relative path keys to match arrays (unique sources retained as empty arrays).

3. Shared Typed Models & Transport:
   - In OsLib: Add typed DTOs (IorgInventoryItem, IorgMatchResult) and request records (IorgListRequest, IorgDuplicateRequest).
   - In RaiImage: Streamed hashing (SHA256.HashDataAsync) and decoded pixel/frame comparison primitives with bounded memory.
   - Ensure typed IorgCommand remote SSH execution resolves paths on the remote host.

4. Non-Destructive Invariant:
   - This capability is strictly READ-ONLY. Zero filesystem mutations, zero cloud deletions, zero sidecar files written.

5. Acceptance Criteria:
   - Implement unit and integration tests covering AC-1 through AC-9 in CR075.
   - Run `dotnet test RAIkeep.slnx` before handing over.
```
