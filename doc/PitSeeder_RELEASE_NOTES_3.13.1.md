# PitSeeder 3.13.1 Release Notes

## Summary

`PitSeeder 3.13.1` prevents a completed finite `pits` command from unnecessarily retaining its JsonPit process activity window while preserving the separate master-writer lease.

## CLI lifecycle

- Finite seed, single-pit export, JSON stdout, and WWWA export operations track every `Pit` they open.
- On normal completion, each tracked pit attempts an ownership-verified release of the current CLI process activity window.
- Exception unwinding performs the same cleanup.
- Ctrl+C and process exit perform best-effort cleanup of any pits still tracked by the CLI.
- Cleanup expires only `{Machine}-pits-{PID}.flag`; it never releases or modifies `Master.flag`.
- Cleanup failures do not turn an otherwise successful command into a failed export; process-exit cleanup retains an opportunity to retry.

## New option

- Added `--retain-window` to keep the CLI process activity window until the normal JsonPit timeout.
- Immediate ownership-verified release is the default for finite CLI operations.
- The option is included in `pits --help` and documented in the PitSeeder README.

## Cloud behavior and writer safety

- Per-PID activity flags prevent consecutive CLI processes from targeting the same process-flag filename.
- Release writes an expired Unix-epoch tombstone in place instead of deleting and recreating the OneDrive-backed path.
- A successful writer retains its timed `Master.flag` lease. A participant that cannot acquire that lease continues to write mergeable change files rather than overwriting the canonical pit.
- The resolved lifecycle CR is [`PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md`](PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md).

## Dependency alignment

- Package version is `3.13.1`.
- Fallback package references are aligned to `JsonPit 3.13.1` and `OsLibCore 3.13.1`.
- PitSeeder remains last in the coordinated release order.

## Validation

- `PitSeeder.Tests`: `7` passed, `0` failed.
- Two immediate consecutive read-only WWWA exports against the configured OneDrive `AIA` pit succeeded.
- The resulting process flags used distinct PIDs and contained expired epoch timestamps after completion.
- Coverage includes immediate consecutive execution, `--retain-window`, exception cleanup, foreign-process ownership rejection, and master-ticket preservation.

## Release sequencing

`PitSeeder` is sixth and last in the coordinated release chain. Its GitHub push/tag must wait for ImgSeeder workflow success, flat-container visibility, and the full `330`-second hold. After PitSeeder publishes, perform the final flat-container verification for all six packages before declaring the chain complete.
