# OsLibCore 4.2.9 Release Notes

OsLibCore 4.2.9 implements the reusable filesystem boundary required by accepted
[CR022](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md)
and carries forward the typed maintenance coordination introduced by accepted
[CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md).

- Adds `RaiCloudStorageException` with operation, source, and destination context.
- `RaiFile.mv` and `RaiPath.mv` reject TempDir-to-cloud moves before mutation.
- Existing cloud files are overwritten in place; the source of an explicit move
  is removed only after the destination write succeeds.
- Existing cloud directories cannot be replaced through `mv` or `cp`.
- Cloud backup requests preserve the live source and create a copy.
- Missing-copy sources and operating-system failures surface through the typed
  `RaiFileIOException` boundary.

Regression coverage verifies rejection before mutation, continuously present
cloud pathnames, safe same-tree semantic renames, and non-destructive backups on
a real configured CloudDrive root.
