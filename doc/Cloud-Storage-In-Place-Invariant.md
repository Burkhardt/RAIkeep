# RAIkeep Cloud-Storage In-Place Invariant

RAIkeep treats an established pathname inside any configured CloudDrive as a
durable synchronization identity.

## Mandatory rules

1. Never create a file or directory in `Os.TempDir` and then move, rename, or
   swap that filesystem object into a configured cloud tree.
2. Never replace an existing cloud directory as an implementation detail.
3. Updating an existing cloud file must keep its pathname continuously present.
   Open that path and write the new bytes in place through `RaiFile`/`TextFile`.
4. A temporary workspace may be used by an external tool only when it remains
   outside the cloud tree. Copy the resulting bytes into the final established
   pathname; delete only the temporary workspace afterward.
5. Explicit user-visible semantic operations—such as moving an ItemTree
   artifact to a new ItemId—may rename or remove paths only when that change is
   the requested result, never as a hidden persistence technique.
6. Inspection, report-only, validation, and failed operations must not create
   directories or files.
7. All product code uses the `RaiPath`, `RaiFile`, `TextFile`, and typed tool
   boundaries. A new direct `System.IO` use requires an explicit design review.

`RaiFile.mv` and `RaiPath.mv` reject TempDir-to-cloud moves before mutation.
Existing cloud directories cannot be replaced through `mv(... replace: true)`
or `cp(... replace: true)`. Cloud-file replacement preserves the destination
pathname and removes a source only after the in-place write succeeds.

This invariant was formalized by
[CR022](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md)
after the 2026-09-09 OneDrive incident investigation.
