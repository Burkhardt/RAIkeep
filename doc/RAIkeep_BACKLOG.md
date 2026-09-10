# RAIkeep product backlog

This document records approved ideas that still require a dedicated design or
change-request decision before implementation. Backlog entries are not release
commitments and do not authorize package publication.

## JsonPit recovery-event archive compaction

**Status:** Proposed after the CR021/CR022 maintenance review; not implemented.

### Goal

Prevent a pit's `Events` directory from accumulating an unbounded number of
loose `.event` files while preserving the durable recovery audit trail and the
mandatory cloud-storage in-place invariant.

For each pit, collect a stable snapshot of eligible loose files from:

```text
<Pit>/Events/*.event
```

and write one immutable ZIP archive in that same `Events` directory. Entry names
inside the archive retain the complete original `.event` filenames.

The archive filename uses the plural `Events` plus the oldest and newest event
UTC times in human-readable `yyyyMMdd-HHmm` form:

```text
Events_20260804-0118_to_20260910-1643.zip
```

The range is derived from the validated event contents, not filesystem modified
times. The archive records UTC explicitly in its metadata even though the compact
filename omits punctuation and a timezone suffix.

### Proposed CLI boundary

The first implementation should be explicitly requested rather than silently
added to every applying maintenance run:

```bash
pits maintain Object -c OneDrive -r AIA --apply --archive-events --json
pits maintain --wwwa -c OneDrive -r AIA --apply --archive-events --json
```

This recommendation keeps deletion of loose audit evidence visible and
reviewable while the behavior is new. Whether event archiving should later
become automatic during ordinary applying maintenance remains a separate
product decision based on operational experience.

A report-only preview must identify the exact archive name, selected event
count, date range, and any deferred files without writing or deleting anything.
The final option shape and any minimum-age/grace policy must be frozen before
implementation.

### Audit continuity

`pits audit` must transparently read and combine:

- remaining loose `.event` files; and
- validated `Events_<start>_to_<end>.zip` archives.

Human and `--json` output, `--machine`, `--level`, deterministic ordering, and
minimum-severity behavior remain unchanged. During an interrupted or retried
archive operation, duplicate loose/archive copies are deduplicated by validated
event identity; conflicting content is reported rather than hidden.

Archiving therefore changes physical storage density, not the logical audit
history visible to users and agents.

### OsLib and cloud-safety requirements

- JsonPit and PitSeeder use an OsLib collection-capable ZIP abstraction. They do
  not invoke `System.IO.Compression`, `zip`, `7z`, or a separately constructed
  process directly.
- The archive is created directly at its final path inside the existing `Events`
  directory. No file or directory is staged in `Os.TempDir` and moved into a
  CloudDrive.
- An existing archive pathname is never deleted and recreated or overwritten.
  A same-name retry validates and reuses identical content; different content is
  deferred as a collision.
- The selected loose events remain untouched until the archive has materialized
  and validation proves that every expected filename and byte payload is present.
- If loose source events are retired, they are removed individually and only
  after successful archive validation. Failure retains the remaining sources and
  the immutable archive for a safe retry.
- Events arriving after the initial stable snapshot are not absorbed into the
  running operation and remain loose for a later archive.
- Existing ZIP archives are never recursively archived and are never appended to
  or replaced; each successful batch produces an immutable archive.

### Verification expectations

- Single-pit and `--wwwa` archive creation with deterministic range naming.
- Mixed loose and archived audit reads with unchanged filtering and ordering.
- Interrupted archive creation, partial source retirement, idempotent retry, and
  filename-collision behavior.
- Corrupt event and corrupt archive handling that fails safe and preserves source
  evidence.
- Concurrent new-event publication while a stable older snapshot is archived.
- Tests proving zero TempDir-to-cloud moves, zero directory replacement, and zero
  delete/recreate of an established archive pathname.
- OsLib tests for the collection ZIP abstraction and JsonPit/PitSeeder tests for
  the domain policy and CLI argument/reporting boundary.

