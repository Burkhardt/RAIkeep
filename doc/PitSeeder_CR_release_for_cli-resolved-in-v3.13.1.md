# PitSeeder: release finite CLI process windows

Status: resolved in `v3.13.1`.

## Request

We encountered a real concurrency/usability problem involving Nkosikazi-pits.flag.
I (RAI) first ran a pits command manually in a shell. Immediately afterward, I asked another agent on the same machine to run a read-only export such as:
pits -n -c OneDrive -r AIA -e <temporary-directory> --wwwa
The second execution failed with:
Access to the path '.../AIA/Person/Nkosikazi-pits.flag' is denied.
Both commands ran on the same machine within the access window guarded by RAIkeep/JsonPit. The earlier CLI execution apparently retained the guarded window long enough to block the following process, even though the first command had already completed from the user’s perspective.
Please investigate the lifecycle of Nkosikazi-pits.flag and the guarded access window.
Desired behavior:
A completed pits command should not unnecessarily prevent another command on the same machine from accessing the pits.
Existing concurrency protection must remain safe—do not simply disable the guard.
Determine whether the CLI can release its window/lease immediately after the operation has completed.
Consider adding an explicit CLI option for this behavior, for example:
pits ... --release
or a better name consistent with RAIkeep terminology.
The option should release only the window owned by the current CLI process. It must not delete or override another active process’s guard.
Please also consider whether immediate release should be the default for finite CLI operations, with an option to retain the current time-window behavior only when explicitly needed.
Suggested acceptance tests:
Run one finite pits --json or pits --export command, then immediately run another on the same machine: the second succeeds.
Two genuinely overlapping writers remain protected.
A read-only export does not leave a stale window after normal completion.
The window is released after an exception or cancellation when ownership can be verified.
One process cannot release a flag/window owned by another process.
Existing JsonPit concurrency and atomic-write tests remain green.
Document the exact semantics of the flag, its timeout, ownership, cleanup, and the new CLI option.
Please report the root cause before implementing the fix, including whether the observed denial comes from the logical RAIkeep guard, operating-system file sharing, OneDrive synchronization, or an interaction among them.

## Root cause

The denial was not a logical rejection by the RAIkeep master-ticket guard. Same-machine activity flags were excluded from the foreign-process check, and both CLI invocations used the same stable `Nkosikazi-pits` participant identity.

The failure occurred while updating the shared `Nkosikazi-pits.flag` path. The former save path deleted the flag and recreated it, while consecutive `pits` processes targeted that same filename. On the OneDrive-backed pit, the provider could still be reconciling the first delete/recreate cycle when the next process tried to recreate the same path, producing the observed `UnauthorizedAccessException`. There was no evidence of a long-lived application file handle; the observed behavior was an interaction between the shared filename, the delete/recreate write pattern, and OneDrive synchronization timing.

## Resolution

- Process activity flags are now named `{Machine}-{Subscriber}-{PID}.flag`; the stable `{Machine}-{Subscriber}` identity remains unchanged for the master writer ticket.
- Flag updates use `TextFile.SaveInPlace()` and no longer delete or rename the cloud-synced flag path before writing.
- `Pit.TryReleaseProcessWindow()` verifies the current process identity and expires only that process's activity flag by writing the Unix epoch in place. The flag remains as a diagnostic tombstone.
- Finite `pits` seed/export operations release their process activity windows by default after normal completion and exceptions. Ctrl+C and process exit also perform best-effort cleanup.
- `--retain-window` preserves the former timeout-based activity behavior when explicitly requested.
- Process-window release never releases `Master.flag`; overlapping writers remain governed by the existing master ticket and change-file fallback.
- JsonPit construction failures release any activity window created before the constructor failed.

The activity timeout remains 60 seconds by default through `MasterFlagFile.TicketDuration`.

## Acceptance evidence

- Two immediate consecutive read-only WWWA exports against the configured OneDrive `AIA` pit both succeeded.
- The four flags from each run were retained with distinct PIDs and an epoch timestamp, confirming process-specific ownership and immediate release without deletion.
- Automated coverage verifies immediate consecutive CLI success, the `--retain-window` behavior, exception cleanup, foreign-process ownership rejection, and master-ticket preservation.
- The PitSeeder suite passes all 7 tests and the OsLib suite passes all 65 tests. In JsonPit, 103 tests passed with the separately documented concurrency CR excluded; the external OneDrive remote-sync test then passed on its immediate isolated rerun.

The separate `CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md` request was not implemented as part of this change.
