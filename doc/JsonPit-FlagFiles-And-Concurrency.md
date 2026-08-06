# JsonPit flag files and concurrency

JsonPit uses two related but distinct flag-file concepts in every flagged pit directory:

| File | Scope | Identity | Purpose |
|---|---|---|---|
| `Master.flag` | One per pit | `{Machine}-{Subscriber}-{PID}` (exact process, since v3.13.2) | Timed lease identifying the exact process currently allowed to write the canonical `.pit` file |
| `{Machine}-{Subscriber}-{PID}.flag` | One per OS process and pit | `{Machine}:{ProcessName}:{PID}` | Activity window showing that a specific process recently used the pit |

Both files contain a value and an ISO-8601 timestamp separated by `|`. They use the same timestamped-file foundation in code, but they answer different questions:

- `Master.flag`: “Which exact process currently has the canonical-writer lease?”
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

Each pit has one `Master.flag`. Since v3.13.2 (CR003) it stores the exact process identity of the current owner:

```text
Nkosikazi-pits-4821|2026-08-03T19:10:00.0000000+00:00
```

The stable participant identity (`Nkosikazi-pits`) is contained in the exact identity; the trailing PID distinguishes concurrent processes of the same participant.

- Only the exact owning process may renew its active master lease directly.
- A different PID with the same stable participant must not inherit master authority while the recorded owner's process window remains active; it follows the non-master change-file path.
- When the recorded owner's process window has been explicitly released or has expired, a new PID with the same stable participant may inherit the still-protected participant lease.
- Different subscribers on one machine remain distinct stable participants.

PID-level collision detection and safe handover are JsonPit responsibilities; applications never invent unique subscribers merely to distinguish PIDs.

`Master.flag` is a timed writer lease, not an operating-system file lock and not a lock that a finite command returns immediately after every operation. It is a cooperative cloud-backed lease — not an atomic cross-machine compare-and-swap.

## Canonical write decision

Before JsonPit writes the canonical `.pit` file, `Pit.Save()` scans for master-conflict signals and calls `TryAcquireMaster()`:

1. If this exact process already owns a valid master lease, renew it.
2. If another exact process of the same participant owns a valid lease and its process window is active, do not write the canonical pit.
3. If the recorded owner's window was released or expired, the same participant's new PID inherits the lease.
4. If a different participant owns a valid lease, do not write the canonical pit.
5. If the lease is expired, check for recent foreign-machine process activity, then claim.
6. Write the canonical pit only when acquisition succeeds; otherwise write collision-safe change files.

`Save` captures one coherent point-in-time snapshot under a brief exclusive state gate, releases the gate before serialization and cloud I/O (concurrent `Add` calls continue), writes through OsLib's no-delete `TextFile.Save`, updates the flags from the snapshot facts, and validates only the fragments demonstrably included in the written snapshot. An addition accepted after the snapshot boundary stays dirty and is written by a later `Save`.

After a canonical write, JsonPit updates `Master.flag` with the exact process identity and the snapshot's change time. It does not clear or return the lease.

Keeping the lease for its timeout gives the canonical write time to propagate through the cloud provider. A different participant arriving during that period falls back to change files instead of immediately overwriting the canonical file.

## Change files and cleanup

Every ordinary change file — non-master persistence, split-master recovery, and graceful-shutdown export — uses the collision-safe identity `{Modified.UtcTicks}_{ExactProcessIdentity}_{Sha256}.json`, where `Sha256` is the full lowercase SHA-256 of the exact canonical UTF-8 JSON payload. Republishing the same fragment is filename-idempotent; distinct equal-timestamp fragments cannot suppress one another. A participant merges a change file only after its content matches the filename hash and parses completely.

Cleanup is a current-master-only two-stage operation: merge and successfully persist a canonical snapshot that accounts for the fragment, then retain the file for a ten-minute propagation grace measured from that save (never from original file age). Restart or master transfer resets eligibility; the new master merges, persists, and starts a fresh grace period.

## Split-master recovery and durable audit events

The cooperative lease can temporarily produce two apparent masters when two servers start from independently visible expired state. A provider-created longer `Master*.flag` (for example `Master (1).flag`) is the provider-independent conflict signal; the exact canonical `Master.flag` remains the sole authority record. Every live writable flagged `Pit` watches its directory for that signal and also rescans at construction, master acquisition, `Save`, and `Reload` — there is no polling loop and no provider API.

- The live losing claimant publishes the union of its master-tenure recovery write set and its dirty fragments as ordinary small change files, then deletes only the longer conflict flag naming itself. It never deletes or alters exact `Master.flag`.
- Only the exact current master persists the reconciled canonical pit and completes cleanup; an orphaned longer flag (no active claimant window) is retired only by the exact current master after window expiry plus a ten-minute grace and a locally validated `Critical` evidence event.
- A live transfer of master authority to another exact process exports the completed tenure's write set as change files even without a conflict flag; same-process lease reacquisition does not.
- Explicit disposal of a writable `Pit` is a durability boundary: it publishes the write set plus dirty fragments as change files first, optionally completes a canonical save, and only then releases process authority and its watcher.

Recovery diagnostics are structured: each live `Pit` exposes `LastRecoveryStatus` and the optional `RecoveryStatusChanged` event, and every meaningful stage is written durably as a canonical-JSON `.event` file under the pit's `Events` child directory (OsLib `EventFile`/`EventDirectory`). `pits -r <root> <PitName> --events` reads that audit without opening a `Pit`, creating flags, or writing events.

## Accepted limitation

An abrupt crash, forced termination, or power loss before in-memory recovery-write-set entries have been exported remains outside the live recovery guarantee. Provider-created noncanonical `Object*.pit` copies are not recovery inputs and remain untouched. Unsupported external delete/rename interference remains an operational condition that may require human repair.

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

The flag protocol provides these protections:

- A process without the current exact master lease does not directly overwrite the canonical pit through the normal `Save()` path.
- Non-master writes are represented as hash-validated, collision-safe, mergeable change files.
- Recent activity on another machine can prevent an expired master lease from being claimed prematurely.
- Master leases recover through timeout rather than permanent lock files.
- Per-PID activity flags prevent consecutive processes from sharing and replacing one process-flag filename.
- Ownership verification prevents one process from explicitly releasing another process's activity flag.
- Two concurrent PIDs of the same participant cannot both exercise master authority; the refused PID writes change files.
- Reads never publish corrupt, partial, or transiently empty pit state: loads build a validated candidate, retry transient read-during-write failures, and throw a descriptive `JsonPitPersistenceException` when the bounded retry window is exhausted.
- No more than one live public in-memory `Pit` instance may own a distinct canonical pit path in a process (writable or read-only); a duplicate constructor throws `PitInstanceConflictException` before it can load or mutate state, and `Dispose` releases the path for a legitimate reopen.

## Operational interpretation

For a long-running application such as Kestrel, keep one in-memory `Pit` instance per distinct pit path in the process and share it through the application's singleton/container mechanism. Multiple threads may use that shared instance according to JsonPit's supported in-process APIs.

Different applications should use meaningful subscriber identities, for example `AfricaStage` and `AIA`. Their master identities are then distinct even on the same machine, and the current master lease determines which participant writes the canonical pit.

A restarted application process receives new per-PID activity flags. It retains the same stable master participant identity when it uses the same machine and subscriber.

## Current boundary

The files are coordination records, not cross-process atomic file locks. CR003's concurrency contract — exact PID-specific master ownership, dynamic handoff, stable concurrent `Add`/`Save` snapshots, validated candidate loads, collision-safe change-file recovery, and the longer-`Master*.flag` split-master response — is implemented in the coordinated v3.13.2 line and proven by explicit in-process, multi-instance, multi-process, and configured-cloud/SSH test suites.

CR003 retains the established configuration model: the machine's configuration file is the sole source of truth for cloud roots and runtime paths, and concurrency tests run against real configured cloud roots.

## Related documentation

- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md)
- [`JsonPit-CONCEPT-Live-Split-Master-Recovery.md`](JsonPit-CONCEPT-Live-Split-Master-Recovery.md)
- [`JsonPit_RELEASE_NOTES_3.13.2.md`](JsonPit_RELEASE_NOTES_3.13.2.md)
- [`OsLib_RELEASE_NOTES_3.13.2.md`](OsLib_RELEASE_NOTES_3.13.2.md)
- [`PitSeeder_RELEASE_NOTES_3.13.2.md`](PitSeeder_RELEASE_NOTES_3.13.2.md)
- [`PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md`](PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md)
