# CR021 — JsonPit Durable Cleanup Receipts and `pits` Coordination

**Requesting product:** RAIkeep

**Requester and acceptance owner:** RAI

**Receiving product:** RAIkeep

**Provider / implementation lead:** Codex (Owner and Lead Custodian, RAIkeep)

**Affected packages:** `OsLibCore`, `JsonPit`, `PitSeeder` (`pits`)

**Target release:** RAIkeep v4.2.8

**Date proposed:** 2026-09-09

**Status:** Accepted and authorized by RAI on 2026-09-09; implementation approved

---

## 1. Request and observed operational problem

RAIkeep shall make JsonPit change-file cleanup progress durable across process
restart and master transfer, provide an explicit `pits` maintenance surface, and
prevent one host application from launching overlapping typed `pits` commands
against the same pit.

The request follows inspection of a live AIA `Activity` pit directory containing:

- many PID-specific process-window tombstones;
- many validated, hash-correct change files whose fragments were already present
  in the healthy canonical pit;
- repeated equivalent change-file content published under successive process
  identities;
- recovery events reporting a cleanup-pending count that grew across process
  lifetimes; and
- extensionless process flags and recovery events whose logical stems contained
  the dotted process name `AIA.Api`.

The retained change files were not corrupt and had not been ignored during
projection. They had been merged successfully, but their cleanup eligibility was
held only in memory. Every finite process or server restart lost that evidence and
started a new ten-minute grace period. A sequence of processes that did not stay
alive long enough to perform a later merge pass could consequently postpone
cleanup forever.

This CR fixes that liveness defect without weakening the existing
canonical-save-before-delete durability rule.

## 2. Governing principles

1. A change file is never deleted merely because it is old.
2. A current exact-process master must first persist or validate a healthy
   canonical snapshot that accounts for the change fragment.
3. The ten-minute propagation grace begins once, at the first successful
   canonical accounting represented by an immutable receipt.
4. Restart, master transfer, or replay must not refresh an existing valid
   receipt's time.
5. Cleanup must fail safe: missing, malformed, conflicting, or unverifiable
   evidence leaves the change file untouched.
6. Exact worker PID identity remains the concurrency authority. A parent shell,
   terminal, Kestrel host, DI scope, or wrapper instance is not substituted for
   an actual `pits` child PID.
7. Local call serialization supplements JsonPit's cloud-backed cooperative
   protocol; it does not replace it or claim distributed mutual exclusion.
8. All filesystem work uses the `RaiPath` / `RaiFile` / `TextFile` boundary.
   No new direct `System.IO` use is authorized by this CR.
9. `Os.Config` remains unchanged and is never rewritten, replaced, or used as a
   mutable coordination store.
10. RAIkeep capabilities are implemented and verified before any downstream AIA
    integration recommendation or AIA code change is made.

## 3. Explicit amendment to CR003

CR003 deliberately specified that restart or master transfer loses in-memory
change-file cleanup eligibility, forcing the next master to merge, persist, and
start a new ten-minute grace period. CR003 also stated that no acknowledgement
sidecar was required.

CR021 supersedes only that cleanup-eligibility persistence decision:

- cleanup eligibility becomes durable in one immutable `ReceiptFile` per change
  file;
- restart and master transfer require revalidation but retain the original valid
  receipt time; and
- a missing receipt is created only after successful canonical accounting and
  begins a new conservative grace period.

All other CR003 rules remain in force, including exact-process master identity,
hash validation, deterministic merge behavior, canonical-save-before-delete,
current-master-only cleanup, the ten-minute propagation grace, durable recovery
events, and the prohibition on finalizer filesystem I/O.

## 4. `ReceiptFile`

### 4.1 Package and type

`JsonPit` shall add:

```csharp
public sealed class ReceiptFile : TextFile
{
    public const string Extension = "receipt";

    public ReceiptFile(string changeFileFullName);

    public DateTimeOffset Time { get; }
}
```

`ReceiptFile` belongs to JsonPit because it represents JsonPit cleanup evidence
and uses JsonPit's timestamp semantics. It inherits `TextFile` from OsLibCore.
OsLibCore must not gain knowledge of change fragments, canonical pits, master
leases, or JsonPit cleanup rules.

### 4.2 Naming and placement

The constructor's only parameter is the associated change file's complete
`FullName`. The receipt derives its path and logical stem from that value, replaces
the `.json` extension with `.receipt`, and remains beside the change file:

```text
639245160038875300_Nkosikazi-AIA-26748_<sha>.json
639245160038875300_Nkosikazi-AIA-26748_<sha>.receipt
```

The receipt does not append a compound `.json.receipt` extension. Its `Name` is
identical to the change file's `Name`; only `Ext` differs.

### 4.3 Content

The complete receipt content is one UTC ISO-8601 round-trip timestamp:

```text
2026-09-09T18:45:00.0000000Z
```

This is the locally observed time immediately after the first successful
canonical persistence or validated canonical accounting of the associated change
file. The public property is named `Time`, consistent with `TimestampedValue.Time`
and `MasterFlagFile.Time`.

No JSON envelope or additional metadata is stored. In particular, the receipt
does not duplicate a schema name, change filename, change hash, canonical
filename, canonical hash, or master identity. The containing directory, matching
stem, hash-bearing change filename, canonical pit, flags, and audit events already
provide those facts at their proper boundaries.

### 4.4 Create-once behavior

- When no receipt exists and canonical accounting has succeeded, construction
  creates the receipt with the current UTC time and awaits local materialization.
- When a valid receipt already exists, construction reads its original `Time` and
  performs no write, timestamp refresh, delete, rename, or replacement.
- Concurrent or repeated observation of the same valid receipt is idempotent.
- A malformed, incomplete, or unreadable receipt is not overwritten and never
  authorizes deletion. Maintenance reports it as deferred for operator review or
  a later materialization retry.
- Receipt creation is normal explicit-operation I/O. A finalizer never creates,
  updates, validates, or deletes a receipt.

## 5. Restart-safe change-file cleanup

The in-memory cleanup dictionary may remain an optimization, but it is no longer
the authority for deletion eligibility. The durable receipt is authoritative.

For every valid merged change file, the exact current master shall:

1. merge and hash/parse-validate the change fragment;
2. successfully persist a canonical snapshot that accounts for it, or prove that
   an existing healthy canonical snapshot already contains the exact fragment;
3. create its missing `ReceiptFile`, or read its existing valid receipt without
   changing `Time`;
4. retain both files until `ReceiptFile.Time + ChangeFileCleanupGrace`;
5. on a later maintenance pass, revalidate exact-master authority, change-file
   integrity, canonical health, exact canonical accounting, and receipt validity;
6. delete the change file first; and
7. only after successful local deletion/materialization handling, delete its
   receipt.

Two independent files cannot be physically deleted atomically on ordinary or
cloud-backed filesystems. Steps 6 and 7 form one logical, crash-safe cleanup
transaction under JsonPit's persistence/recovery gate:

- failure to remove the change file retains the receipt for retry;
- interruption after change-file removal may leave an orphan receipt, which a
  later maintenance pass can safely remove after confirming the change file is
  absent; and
- reappearance of a cloud-synchronized change file without a receipt starts a
  new conservative grace after canonical revalidation rather than permitting
  immediate deletion.

A receipt never proves replication by itself. It proves only when the local
canonical-accounting grace began. The existing grace remains an operational
safety margin under an eventually synchronized CloudDrive.

## 6. Explicit JsonPit maintenance API

JsonPit shall expose an explicit object-oriented maintenance operation on the
already-live `Pit` instance. It shall reconcile valid change files, persist when
authorized and necessary, create/read receipts, and retire eligible change-file /
receipt pairs. It must use the same persistence/recovery gate as `Save`,
`MergeChanges`, and recovery evaluation.

The final public result type and member names shall remain small and report at
least:

- valid change files observed and merged;
- receipts created, retained, malformed, or orphaned;
- change files and receipts removed;
- operations deferred because the process was not current master;
- validation or filesystem failures; and
- whether canonical persistence occurred.

No hidden timer, background thread, finalizer work, or automatic `Os.Config`
mutation is introduced in JsonPit. Long-running hosts decide when to call the
explicit operation. Finite tools use the CLI operation in section 7.

## 7. `pits maintain`

PitSeeder shall add:

```text
pits maintain (<PitName> | --wwwa) [--apply]
  [--prune-process-flags --older-than <duration>]
  [--repair-legacy-extensions]
  [--json] [global options]
```

Behavior:

- without `--apply`, inspect and report the maintenance plan without deleting
  change files, receipts, flags, events, or canonical data;
- with `--apply`, perform the JsonPit maintenance operation described above;
- ordinary `--apply` concerns only validated change-file / receipt cleanup;
- `--prune-process-flags` additionally authorizes removal of proven expired
  PID-specific process-window tombstones and requires an explicit
  `--older-than` duration;
- `--repair-legacy-extensions` additionally authorizes repair of recognizable,
  content-valid extensionless process flags and recovery events through a
  materialize-and-validate-before-source-removal sequence;
- `--wwwa` processes Person, Object, Place, and Activity in deterministic order;
- `--json` emits a stable machine-readable result suitable for agents and
  scheduled administration;
- a non-master invocation may merge for projection/reporting but must not create
  canonical cleanup evidence or delete artifacts;
- invalid or unverifiable artifacts are reported and retained; and
- normal maintenance uses subscriber `pits` and the existing exact child PID.

The current commands retain their existing responsibilities:

- `audit` reads durable events without opening a `Pit` or mutating artifacts;
- `export` projects data and is not a cleanup command;
- `seed`, `delete-property`, and `delete-item` mutate domain data and are not
  repurposed as maintenance commands; and
- `--retain-window` remains unrelated to cleanup eligibility.

A cron or scheduler is useful only after `pits maintain --apply` exists. Repeated
invocation of today's finite `pits` commands must not be documented as a cleanup
solution.

## 8. Process-window hygiene

### 8.1 Identity remains exact

JsonPit continues to distinguish:

- stable participant identity: `{Machine}-{Subscriber}`; and
- exact worker identity: `{Machine}-{Subscriber}-{PID}`.

A `pits` child process keeps its own PID even when launched by a long-running
Kestrel server or terminal shell. Parent process or shell PID may later be added
as diagnostic metadata, but it must not become master authority, process-window
ownership, or change-file authorship identity under CR021.

Direct server use of one shared JsonPit `Pit` already uses the server process PID.
CR021 does not add an identity-management subsystem and does not rename any AIA
project.

### 8.2 Expired process flags

The maintenance report shall inventory:

- active process windows;
- epoch-released tombstones;
- naturally expired windows;
- canonical `Master.flag`;
- longer `Master*.flag` conflict evidence; and
- malformed or extensionless candidates.

CR021 does not authorize implicit deletion of `Master.flag`, live windows, longer
conflict evidence, unknown files, or recovery events. Removal of old PID-specific
process tombstones requires `--apply --prune-process-flags --older-than
<duration>`; there is no implicit retention default. Before deletion,
maintenance must re-read and prove that
the file is a non-master, non-conflict, expired process-window tombstone. The
default report-only operation deletes none.

No parent-PID identity reuse is introduced merely to reduce file count.

## 9. OsLibCore corrections and typed wrapper coordination

### 9.1 Explicit extension with dotted logical stems

OsLibCore shall correct the `TextFile` construction path in which a dotted logical
stem can consume the requested extension. Supplying an explicit extension must
preserve the complete logical stem:

```text
Name = Nkosikazi-AIA.Api-93455
Ext  = flag
FullName = Nkosikazi-AIA.Api-93455.flag
```

The correction must preserve established implicit parsing such as
`new TextFile("settings.json")`. It shall cover `TextFile`, `MasterFlagFile`,
`ProcessFlagFile`, and `EventFile`, including audit enumeration of events whose
logical stems contain `AIA.Api`. This is the same dotted-name ambiguity already
covered for `RaiFile` by the `otw.software` tests; CR021 extends the contract to
the affected typed text-file paths.

Existing malformed extensionless files are not silently interpreted as arbitrary
data. `pits maintain` reports recognizable legacy process-window and event
candidates. Any repair/removal requires explicit apply behavior, successful
content validation, and preservation of the source until the correctly named
destination has materialized and validated.

### 9.2 Same-parent `PitsCommand` serialization

`PitsCommand` shall serialize typed calls targeting the same resolved pit within
one mother process. A target key includes the configured provider/root routing
and pit name. All `PitsCommand` instances in that process share the keyed gate, so
correctness does not depend on consumers registering the wrapper itself as a DI
singleton.

- same-target calls queue rather than overlap;
- unrelated pit targets may execute concurrently;
- WWWA operations acquire the four canonical pit keys in a fixed order and
  release them in reverse order;
- synchronous and asynchronous calls use the same gate;
- waiting honors cancellation and does not launch a child after cancellation;
- gate entries are retired when unused so arbitrary tenant names do not create
  an unbounded process-global dictionary; and
- stdout, stderr, exit code, timeout, cancellation, and original argument-vector
  behavior from CR014/CR014.1 remains unchanged.

This is process-local scheduling only. Direct shell invocations, direct
`RaiSystem` construction, other host processes, and other machines do not share
the in-memory gate. JsonPit's exact-process and CloudDrive protocol remains the
correctness boundary for those cases.

## 10. RAIkeep-first implementation boundary

CR021 initially changes only RAIkeep repositories:

1. OsLibCore fixes explicit extension handling and adds typed-wrapper
   serialization.
2. JsonPit adds `ReceiptFile`, durable cleanup eligibility, maintenance behavior,
   and recovery reporting.
3. PitSeeder adds typed `maintain` parsing, human/JSON reporting, and explicit
   apply behavior.
4. OsLibCore's `PitsCommand` adds the corresponding typed maintenance request.
5. RAIkeep documentation and release notes describe the amended CR003 cleanup
   contract.

Only after these capabilities are provider-verified will RAIkeep issue guidance
to AIA about explicit subscriber names, hosted maintenance cadence, direct
JsonPit use, CLI integration tests, or consolidation of CLI invocations. No AIA
source change is part of CR021.

## 11. Required verification

### 11.1 OsLibCore

- Explicit `RaiFile` and `TextFile` extensions preserve `otw.software`, `AIA.Api`,
  and other dotted logical stems.
- Process and event filenames end in `.flag` and `.event` respectively.
- `EventDirectory.Events` sees a valid event whose logical stem contains a dot.
- Concurrent same-target `PitsCommand` calls never overlap in a capture child.
- Different-target calls may overlap.
- WWWA acquisition is deterministic and deadlock-free.
- Cancellation while queued starts no process.
- CR014.1 argument and result-transport coverage remains green.

### 11.2 JsonPit

- `ReceiptFile(changeFile.FullName)` produces the same path/stem with only the
  `.receipt` extension.
- Receipt content is exactly one round-trip UTC timestamp.
- Reopening an existing receipt preserves its exact content, `Time`, and
  filesystem write timestamp.
- The first successful canonical accounting creates one receipt.
- Repeated merge, restart, and master transfer do not refresh a valid receipt.
- No change file is deleted before receipt grace elapses.
- An eligible file is deleted only after current-master and canonical-accounting
  revalidation.
- Change-file deletion failure leaves the receipt.
- Interruption between the two removals leaves a safely removable orphan receipt.
- A malformed or incomplete receipt never authorizes deletion.
- A reappearing change file without a receipt starts a new conservative grace.
- A finalizer performs no receipt, recovery-publication, flag, or other filesystem
  I/O, and its canonical path becomes reopenable after collection.

### 11.3 PitSeeder

- `maintain` accepts single-pit and WWWA targets.
- Report-only mode performs no deletion.
- `--apply` removes only validated eligible pairs and explicitly authorized aged
  process tombstones.
- Process tombstones remain untouched unless `--prune-process-flags` and an
  explicit `--older-than` value accompany `--apply`.
- Recognizable extensionless legacy artifacts remain untouched unless
  `--repair-legacy-extensions` accompanies `--apply`.
- Human and JSON summaries report the same counts and deferrals.
- `audit` remains strictly read-only and now sees dotted-stem `.event` files.
- Existing `seed`, `export`, point-in-time export, delete, and audit suites remain
  green.

### 11.4 Configured CloudDrive acceptance

The receipt lifecycle must also be exercised against at least one configured
real CloudDrive root, including materialization, restart, preservation of the
original receipt time, grace expiry, change-first removal, and receipt removal.
A skipped configured-cloud test does not count as final acceptance of the cloud
cleanup contract.

## 12. Documentation, release, and authority

- Update affected README and foldable `API.md` files.
- Update `JsonPit-FlagFiles-And-Concurrency.md` and the detailed CR003 record to
  identify CR021's narrow superseding rule.
- Publish coordinated release notes for the provider-designated version, citing
  CR003, CR014/CR014.1, and CR021 where their contracts intersect.
- Run focused tests plus the complete Release suites for OsLibCore, JsonPit, and
  PitSeeder, followed by relevant downstream and umbrella preflight validation.
- Do not tag, publish, label, or change package versions until RAI separately
  approves the release designation and manual release gate.

## 13. Acceptance criteria

CR021 is complete when:

- cleanup eligibility survives process restart and master transfer without its
  original valid receipt time being refreshed;
- no valid change file can be deleted without canonical accounting, a valid
  receipt, elapsed grace, and current exact-master authority;
- eligible change/receipt retirement is crash-safe and retryable;
- finite and long-running consumers have an explicit maintenance API;
- the typed `pits` wrapper serializes same-target calls inside one mother process;
- exact child PID identity remains intact;
- dotted application names produce correctly extended process and event files;
- old malformed and accumulated artifacts can be inventoried before any explicit
  cleanup is applied;
- required local and configured-cloud tests pass; and
- downstream AIA advice waits until the RAIkeep provider capability is complete
  and verified.

---

*Prepared by the RAIkeep provider from RAI's operational findings and the agreed
immutable `ReceiptFile` design. The change intentionally improves cleanup
liveness without converting RAIkeep into an identity-management system or
weakening JsonPit's eventually synchronized persistence guarantees.*
