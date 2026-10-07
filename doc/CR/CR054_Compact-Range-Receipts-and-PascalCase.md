# CR054 — Compact image import receipts and filename normalization

Status: implementation for RAIkeep 4.5.5. This public specification uses synthetic
examples; private source archives and domain models are not repository fixtures.

- Default `iorg organize --json` emits ReceiptVersion 2. A homogeneous contiguous
  run uses BaseItemId, existing convention enum names, and Range (Start, End,
  Count, Ext). Multiple runs use Ranges, each carrying its own stem/conventions.
- Successful singletons, skipped files, and failures appear in sparse Exceptions.
  Missing numbers split ranges; a range never claims a failed image succeeded.
- Explicit `--exif` adds detailed Files with requested metadata while retaining
  compact descriptors and Summary. Default output omits Files.
- No top-level lifecycle Status is persisted. ActivityId is a reference; the
  activity owns its lifecycle. Summary and process exit code report import results.
- The clean 193-image example is below 500 UTF-8 bytes, and the 500-image/two-range
  example is below 1 KB before Pit history metadata. Many disjoint ranges or
  exceptions naturally require more space; no information is silently truncated.
- `Customer-Order-Sheet-26-10.jpg` normalizes to CustomerOrderSheet / image 10.
  Terminal delimiter-separated numeric tokens are discarded except the final
  sequence number. `Order_SHEET_001.jpg` normalizes to OrderSheet / image 1.
- Structured output uses D3 minimum width. Legacy stays D2; stored files are not
  automatically renamed. Coordinate migration of existing paths and references.
- ImageTreeFile and existing enums remain authoritative for names and paths.
  CloudSafe temporary extraction, direct final-path writes, collision preflight,
  cleanup, and live-ID rejection remain intact.

Acceptance coverage: CompactReceiptTests, ImageImportTests, ImportCliTests,
FilenameNormalizationTests, and existing image-tree/rendering tests.
