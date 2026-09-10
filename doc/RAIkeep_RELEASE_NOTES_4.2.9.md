# RAIkeep 4.2.9 Release Notes

RAIkeep 4.2.9 is the coordinated seven-package incident-correction delivery of
accepted [CR022 — Cloud-Safe In-Place Filesystem Invariant](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md).
It carries forward accepted [CR021 — JsonPit Durable Cleanup Receipts and `pits` Coordination](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md).

## Incident finding

The investigation found no evidence that JsonPit replaced the four established
AIA pit directories. The mass-deletion prompt was consistent with the explicitly
requested removal of expired process flags and repaired legacy files. It did,
however, expose one report-only path-construction defect and independent
TempDir-staging patterns elsewhere in the product line. This release corrects
those defects and turns the cloud rule into a tested, reusable boundary.

## Delivered

- `RaiFile` rejects TempDir-to-cloud moves before mutation and overwrites an
  existing cloud file without deleting or renaming its established pathname.
- `RaiPath` rejects TempDir-to-cloud directory moves and replacement of existing
  cloud directories.
- Cloud backups copy established files instead of moving them away.
- JsonPit report-only maintenance no longer materializes a missing pit directory.
- `pits maintain` validates its configured root and canonical pit files before
  constructing any `Pit`; partial WWWA trees are reported without being created.
- ImgSeeder writes directly to the final ItemTree pathname instead of staging a
  subscriber tree in `Os.TempDir`.
- `ImageMagick.JpegTran` uses isolated temporary input/output files and copies
  successful bytes into the continuously present destination pathname.
- The cloud-storage invariant is documented and covered by configured-cloud
  success, failure, and no-mutation regressions.

All seven package versions and fallback dependency properties align on 4.2.9.
Tagging, GitHub labeling, and NuGet publication remain behind RAI's manual
`scripts/release-chain.sh 4.2.9` gate.
