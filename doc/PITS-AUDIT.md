# `pits audit` operational manual

## Purpose

`pits audit` reads JsonPit's durable persistence and recovery log. Each logical
event beneath a pit's `Events` directory—either a loose `.event` file or an
entry in an immutable `Events_*.zip` archive—records one structured occurrence
such as a role decision, change-file publication, canonical persistence,
cleanup, conflict, deferral, or failure.

Audit events answer questions such as:

- Which machine and process participated in recovery?
- Which process held or observed master authority?
- Were accepted fragments published as change files?
- Did a master canonicalize those changes?
- Was cleanup started, completed, deferred, or failed?
- Which related events belong to the same recovery attempt?

They are diagnostic evidence, not the authoritative domain data.

## What an event is—and is not

| Artifact | Purpose |
|---|---|
| `<PitName>.pit` | Authoritative canonical PitItem history at that replica |
| hashed `.json` change file | Durable fragments awaiting or surviving canonical merge |
| `.receipt` | Immutable evidence establishing cleanup-grace eligibility |
| `.event` | Structured recovery/audit logfile occurrence |
| `Events_<start>_to_<end>.zip` | Immutable compact collection of validated `.event` files |
| `Master.flag` | Current master-writer lease record |
| process `.flag` | Exact-process activity window or released tombstone |

Events do not calculate the current value of a PitItem and are not an alternative
to `pits export`. They also do not authorize deletion of change files; receipts
and current exact-master revalidation do that.

## Safety contract

`pits audit` is strictly read-only. It reads the `Events` child directory
directly and does not:

- construct or open a `Pit`;
- create or update a process flag;
- acquire or refresh `Master.flag`;
- merge changes or write the canonical pit;
- create receipts; or
- write another audit event merely because events were read.

A missing `Events` directory produces an empty result and is not created. A
temporarily incomplete, unparseable, or hash-invalid event is omitted from that
read and reconsidered on the next invocation; it is not deleted or repaired by
audit mode. Archives are read in memory without extracting files. Invalid
archives, conflicting event identities, and conflicting loose/archive content
produce audit warnings and a nonzero result while all evidence remains untouched.

## Command syntax

```text
pits audit (<PitName> | --wwwa)
  [--machine <all|local|name>]
  [--level <Trace|Debug|Information|Warning|Error|Critical>]
  [--json]
  (-r|--pitroot) <root>
  [-c|--cloud <provider>]
```

Use one Pit name or `--wwwa`, never both.

Contextual help is always available:

```bash
pits audit --help
```

## Resolving the pit root

With a configured CloudDrive, `-c` selects the provider and `-r` is relative to
that provider root:

```bash
pits audit Object -c OneDrive -r AIA
```

For a configured OneDrive root, this inspects:

```text
<configured OneDrive>/AIA/Object/Events/
```

Without `-c`, pass an explicit local or mounted pit root:

```bash
pits audit Object -r /srv/raikeep/AIA
```

The named pit is appended by the command. Do not pass the `Object` directory
twice.

## Common operations

### Inspect one pit as readable text

```bash
pits audit Object -c OneDrive -r AIA
```

Each output row contains:

```text
Machine    UTC timestamp    Level    Stage    Message    (event filename)
```

### Inspect one pit as JSON

```bash
pits audit Object -c OneDrive -r AIA --json
```

JSON mode writes one array containing the original validated event objects. It
is suited to agents, scripts, `jq`, and incident records.

### Inspect all WWWA pits

```bash
pits audit --wwwa -c OneDrive -r AIA
```

This aggregates `Person`, `Object`, `Place`, and `Activity` event directories.

### Show warning severity and above

```bash
pits audit --wwwa -c OneDrive -r AIA --level warning
```

The level filter is an inclusive minimum. `warning` therefore includes
`Warning`, `Error`, and `Critical`. Level names are case-insensitive.

### Restrict the originating machine

```bash
pits audit --wwwa -c OneDrive -r AIA --machine local
pits audit --wwwa -c OneDrive -r AIA --machine Nkosikazi
```

- `all` is the default.
- `local` resolves to the machine executing `pits`.
- Any other value is compared with the event's recorded machine name,
  case-insensitively.

Machine and severity filters can be combined.

## Compact loose event files

Archiving changes only physical storage density; it does not change the logical
history returned by `pits audit`.

Preview one pit without mutation:

```bash
pits maintain Object -c OneDrive -r AIA --archive-events --json
```

Apply after reviewing `EventFilesEligible`, `EventArchiveName`, the UTC range,
`Deferred`, and `Failures`:

```bash
pits maintain Object -c OneDrive -r AIA \
  --apply --archive-events --json
```

The WWWA form applies independently to each existing pit:

```bash
pits maintain --wwwa -c OneDrive -r AIA \
  --apply --archive-events --json
```

The filename uses the oldest and newest validated event content timestamps in
UTC, for example `Events_20260804-0118_to_20260910-1643.zip`. A compact metadata
entry records the UTC basis explicitly. The archive is created once at its final
pathname inside the already-existing `Events` directory. It is never appended
to, overwritten, deleted/recreated, or staged in `Os.TempDir`.

Loose source files stay present until the archive validates every expected
filename and exact byte payload. They are then retired one by one. A retry
recognizes identical loose/archive copies and safely completes remaining source
retirement. A different or corrupt same-name archive is retained as a collision,
and loose evidence is not removed.

## Severity levels

JsonPit uses these levels from least to most severe:

1. `Trace`
2. `Debug`
3. `Information`
4. `Warning`
5. `Error`
6. `Critical`

The underlying .NET `None` value is never written and is rejected as a filter.

## Recovery stages

| Stage | Default level | Interpretation |
|---|---|---|
| `ConflictDetected` | `Warning` | A cloud or authority conflict signal was observed |
| `RoleDetermined` | `Information` | This process evaluated its local recovery role |
| `ChangeFilesPublished` | `Information` | Accepted fragments were made durable as change files |
| `Canonicalized` | `Information` | A master persisted an accounted canonical snapshot |
| `CleanupPending` | `Debug` | Canonical accounting succeeded and cleanup grace began |
| `Completed` | `Information` | A recovery or cleanup operation completed |
| `DeferredForRetry` | `Warning` | Work was retained because it could not yet be completed safely |
| `Failed` | `Error` | A persistence or recovery step failed |

A failure to make accepted fragments durable during explicit shutdown is raised
to `Critical`.

An event reports an occurrence, not necessarily the present state. For example,
a historical `CleanupPending` event may have a later `Completed` event. Use
`pits maintain ... --json` to inspect the current change, receipt, and flag
inventory.

## JSON event fields

| Field | Meaning |
|---|---|
| `SchemaVersion` | JsonPit recovery-event schema version |
| `EventId` | Unique event identity |
| `UtcTime`, `UtcTicks` | Event time in UTC, in readable and sortable forms |
| `Level` | Severity |
| `Stage` | Structured recovery stage |
| `Pit` | Pit identity/path recorded by the producer |
| `Machine` | Originating machine |
| `Process` | Exact local process identity |
| `Master` | Master identity known when the event was written |
| `Role` | `Master`, `Loser`, `Observer`, or `None` |
| `FragmentCount` | Number of affected in-memory fragments, when applicable |
| `FileCount` | Number of affected files, when applicable |
| `CorrelationId` | Identity joining events from one related operation/tenure |
| `Operation` | Source operation such as save, merge, disposal, or recovery |
| `Message` | Human-readable outcome |
| `Exception` | Exception detail when recorded; otherwise empty |

The complete event filename includes a content hash. Validated reading uses that
identity to avoid presenting partially materialized or inconsistent event files
as trustworthy audit evidence.

## Useful JSON reports

### Count events by stage

```bash
pits audit Object -c OneDrive -r AIA --json |
  jq 'sort_by(.Stage) | group_by(.Stage) | map({stage: .[0].Stage, count: length})'
```

### Produce a global UTC chronology

Human output is intentionally ordered by machine, then time, then event ID. For
a cross-machine time sequence:

```bash
pits audit --wwwa -c OneDrive -r AIA --json |
  jq 'sort_by(.UtcTicks) | map({UtcTime, Pit, Machine, Level, Stage, Message})'
```

### Show the newest failures

```bash
pits audit --wwwa -c OneDrive -r AIA --json |
  jq 'map(select(.Stage == "Failed")) | sort_by(.UtcTicks) | reverse | .[:20]'
```

### Follow one correlation

```bash
CORRELATION='00000000-0000-0000-0000-000000000000'
pits audit --wwwa -c OneDrive -r AIA --json |
  jq --arg id "$CORRELATION" 'map(select(.CorrelationId == $id)) | sort_by(.UtcTicks)'
```

### Count events per machine

```bash
pits audit --wwwa -c OneDrive -r AIA --json |
  jq 'sort_by(.Machine) | group_by(.Machine) | map({machine: .[0].Machine, count: length})'
```

## Situation-oriented investigations

### “Did recovery fail?”

Start with the high-severity view:

```bash
pits audit --wwwa -c OneDrive -r AIA --level warning
```

Read `Stage`, `Operation`, `Message`, and `Exception`. Then use the event's
`CorrelationId` in JSON output to retrieve the surrounding recovery sequence.

### “Why are change files still present?”

Look for `Canonicalized`, `CleanupPending`, `DeferredForRetry`, and `Failed`
events. Then inspect current state separately:

```bash
pits maintain --wwwa -c OneDrive -r AIA --json
```

Audit explains history; maintenance reports what is present now.

### “Did another machine participate?”

Aggregate WWWA JSON and count by machine, or select the suspected machine:

```bash
pits audit --wwwa -c OneDrive -r AIA --machine OtherMachine
```

### “Did a graceful shutdown protect accepted data?”

Inspect `ChangeFilesPublished`, `Completed`, `DeferredForRetry`, `Failed`, and
`Critical` events for the relevant process and correlation. A published change
file is the durability boundary when canonical persistence could not complete.

## Exit and empty-result behavior

- A valid query with no matching events succeeds and returns an empty JSON array
  or a human-readable “No matching events” message.
- Invalid levels, missing roots, or invalid combinations return an error.
- Audit success means the requested readable events were returned; it does not
  assert that no incomplete or externally removed file exists.

## Event retention and archives

RAIkeep 4.2.9 reads loose `.event` files only. `pits maintain` does not remove
them. Transparent ZIP archiving—including continued `pits audit` access—is
recorded as proposed work in
[RAIkeep_BACKLOG.md](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RAIkeep_BACKLOG.md),
but is not current behavior.
