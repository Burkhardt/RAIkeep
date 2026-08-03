# JsonPit 3.13.1 Release Notes

## Summary

`JsonPit 3.13.1` separates per-process activity windows from the stable master-writer lease and adds ownership-verified cleanup for finite clients such as PitSeeder.

## Flag-file lifecycle

- Process activity files now use `{Machine}-{Subscriber}-{PID}.flag`, giving each OS process its own activity window in every pit it opens.
- The stable `{Machine}-{Subscriber}` participant identity remains the value used in the single `Master.flag` writer lease for each pit.
- Added `ProcessFlagFile.CurrentFlagName(...)`, `IsOwnedByCurrentProcess`, and `TryReleaseCurrentProcess()`.
- Added `Pit.TryReleaseProcessWindow()`. It expires only a flag whose content still identifies the current process and never modifies `Master.flag`.
- Explicit release writes the Unix epoch in place. The expired flag remains as a diagnostic tombstone instead of causing a cloud-sensitive delete/recreate cycle.
- Successful flagged loads refresh process activity with the current time.
- Constructor failures attempt to release any process activity window created before construction failed.

## File handling

- Master and process flag updates now use `TextFile.SaveInPlace()` through OsLib.
- Canonical pit modification time is read through `RaiFile.LastWriteTimeUtc`; JsonPit no longer performs a direct `System.IO.FileInfo` read.
- Physical last-write time remains the real filesystem/cloud write time and is not rewritten to a logical item timestamp.

## Other carried-forward behavior

- Fallback dependencies are aligned to `OsLibCore 3.13.1` and `RaiUtils 3.13.1`.
- `PitItem.DeleteProperty(...)` retains its top-level tombstone projection behavior.
- Corrected the XML API reference for historical replay to `AddHistorical(PitItem)`.

## Compatibility and operational notes

- Process flag filenames change from a stable subscriber filename to a per-PID filename. Monitoring or cleanup tools that inspect flag names must account for the PID suffix.
- Expired process flag tombstones can accumulate; this is an accepted trade-off to avoid delete/recreate synchronization races.
- `Master.flag` remains a timed participant lease, not a per-PID mutex. Releasing a process activity window does not return or release master ownership.
- The existing flag mechanism and its current concurrency boundary are documented in [`JsonPit-FlagFiles-And-Concurrency.md`](JsonPit-FlagFiles-And-Concurrency.md).
- The separate annotated concurrency CR remains open and is not implemented by this release work.

## Validation

- Umbrella `RAIkeep.slnx` build succeeds with `0` warnings and `0` errors after the XML reference correction.
- JsonPit local selection: `103` passed, `0` failed, excluding the test owned by the separate open concurrency CR and the external remote-sync scenario.
- The external OneDrive remote-sync scenario passed on its immediate isolated rerun.
- Master-ticket coverage verifies per-PID naming, ownership rejection, epoch release, and preservation of `Master.flag`.

## Release sequencing

`JsonPit` is fourth in the coordinated release chain. Its GitHub push/tag must wait for RaiImage workflow success, flat-container visibility, and the full `330`-second hold. `ImgSeeder` must wait for the same checks after JsonPit publishes.
