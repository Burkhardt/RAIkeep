# JsonPit flag files and concurrency

JsonPit uses two related but distinct flag-file concepts in every flagged pit directory:

| File | Scope | Identity | Purpose |
|---|---|---|---|
| `Master.flag` | One per pit | `{Machine}-{Subscriber}` | Timed lease identifying the participant currently allowed to write the canonical `.pit` file |
| `{Machine}-{Subscriber}-{PID}.flag` | One per OS process and pit | `{Machine}:{ProcessName}:{PID}` | Activity window showing that a specific process recently used the pit |

Both files contain a value and an ISO-8601 timestamp separated by `|`. They use the same timestamped-file foundation in code, but they answer different questions:

- `Master.flag`: “Which stable participant currently has the canonical-writer lease?”
- `ProcessFlagFile`: “Which exact OS process is or was active?”

The default validity window is 60 seconds through `MasterFlagFile.TicketDuration`.

## ProcessFlagFile

`ProcessFlagFile` is the API and class name for the per-process activity file. Its filename includes the PID:

```text
Nkosikazi-pits-4821.flag
```

Its content identifies the process more explicitly:

```text
Nkosikazi:dotnet:4821|2026-08-03T19:10:00.0000000+00:00
```

A process updates its activity flag after a successful flagged load and during flagged persistence activity. Separate processes receive separate filenames, even when they run on the same machine with the same subscriber.

### Explicit release

`TryReleaseProcessWindow()` releases only the current process activity window:

1. Read the activity flag.
2. Verify that its content still equals the current machine, process name, and PID.
3. If ownership matches, write the Unix epoch as its timestamp.
4. Leave the file in place as an expired diagnostic tombstone.

The file is not deleted or renamed. This avoids the delete/recreate pattern that caused trouble when consecutive CLI processes updated the same OneDrive-backed flag path.

An old tombstone can therefore remain in the pit directory. Accumulating these small files is an accepted trade-off for process-specific diagnostics and safer cloud synchronization.

PitSeeder performs this release by default when a finite command completes. `--retain-window` keeps the normal timeout-based activity window instead.

## Master.flag

Each pit has one `Master.flag`. It stores a stable participant identity such as:

```text
Nkosikazi-pits|2026-08-03T19:10:00.0000000+00:00
```

The master identity intentionally omits the PID. A later `pits` process on the same machine is still the same stable `Nkosikazi-pits` participant even though its activity flag has a new PID.

`Master.flag` is a timed writer lease, not an operating-system file lock and not a lock that a finite command returns immediately after every operation.

## Canonical write decision

Before JsonPit writes the canonical `.pit` file, `Pit.Save()` calls `TryAcquireMaster()`:

1. If the current participant already owns a valid master lease, renew it.
2. If another participant owns a valid lease, do not write the canonical pit.
3. If the lease is expired, check for recent foreign-machine process activity.
4. If no foreign process blocks acquisition, claim `Master.flag` for the current participant.
5. Write the canonical pit only when acquisition succeeds.
6. Otherwise, write mergeable change files.

After a canonical write, JsonPit updates `Master.flag` again with the stable participant identity and the latest logical change time. It does not clear or return the lease.

Keeping the lease for its timeout gives the canonical write time to propagate through the cloud provider. A different participant arriving during that period falls back to change files instead of immediately overwriting the canonical file.

## Why CLI process cleanup does not release master

The PitSeeder cleanup added in `3.13.1` expires only:

```text
{Machine}-pits-{PID}.flag
```

It deliberately leaves `Master.flag` untouched. The two operations have different meanings:

- Releasing the process window says that this specific CLI process has finished.
- Retaining the master lease says that the participant's canonical write remains protected during the lease and propagation window.

Consequently, a completed CLI command no longer blocks the next command through a stale process activity window, while the master-writer protocol continues to direct other participants to change files.

## What the current mechanism guards

The flag protocol currently provides these protections:

- A participant without the current master lease does not directly overwrite the canonical pit through the normal `Save()` path.
- Non-master writes are represented as mergeable change files.
- Recent activity on another machine can prevent an expired master lease from being claimed prematurely.
- Master leases recover through timeout rather than permanent lock files.
- Per-PID activity flags prevent consecutive processes from sharing and replacing one process-flag filename.
- Ownership verification prevents one process from explicitly releasing another process's activity flag.

## Operational interpretation

For a long-running application such as Kestrel, keep one in-memory `Pit` instance per distinct pit path in the process and share it through the application's singleton/container mechanism. Multiple threads may use that shared instance according to JsonPit's supported in-process APIs.

Different applications should use meaningful subscriber identities, for example `AfricaStage` and `AIA`. Their master identities are then distinct even on the same machine, and the current master lease determines which participant writes the canonical pit.

A restarted application process receives new per-PID activity flags. It retains the same stable master participant identity when it uses the same machine and subscriber.

## Current boundary

The files are coordination records, not cross-process atomic file locks. Processes with the same machine and subscriber have distinct activity flags but share one master participant identity. The detailed supported behavior for genuinely overlapping same-identity processes and the stable persistence snapshot for concurrent in-process `Add`/`Save` activity remain subjects of the separate annotated concurrency CR.

That CR should define and test those boundaries without changing configuration loading or replacing real cloud-root behavior. It is intentionally not expanded here.

## Related documentation

- [`JsonPit_CR_concurrency-for-next-release-RAI-commented.md`](JsonPit_CR_concurrency-for-next-release-RAI-commented.md)
- [`PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md`](PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md)
- [`JsonPit_RELEASE_NOTES_3.13.1.md`](JsonPit_RELEASE_NOTES_3.13.1.md)
- [`PitSeeder_RELEASE_NOTES_3.13.1.md`](PitSeeder_RELEASE_NOTES_3.13.1.md)
