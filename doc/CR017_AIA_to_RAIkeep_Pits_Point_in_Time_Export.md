# CR017 — `pits` Point-in-Time Export

**Requesting product:** AIA
**Requesters:** Adele (PM, AIA) and RAI
**Receiving product:** RAIkeep (`PitSeeder`, `OsLibCore`, and the existing
`JsonPit` historical projection boundary)
**Acceptance owner:** RAI
**Target release:** Coordinated RAIkeep v4.2.5
**Date originally drafted by RAIkeep:** 2026-08-27
**Date submitted by AIA:** 2026-08-31
**Date reviewed by RAIkeep:** 2026-08-31
**Status:** Formally accepted by AIA and RAIkeep; implemented and verified for
RAI's manual v4.2.5 release gate
**AIA request:** [CR017 at the reviewed AIA commit](https://github.com/Burkhardt/AIA/blob/923cbddbefd0c69730a99746bedd16f150397050/doc/CR017_AIA_to_RAIkeep_Pits_Point_in_Time_Export.md)
**AIA Step 3 acceptance:** [CR017 acceptance at the immutable AIA commit](https://github.com/Burkhardt/AIA/blob/1394850b5fd8fc77e74a9e9fa28903d333c87aa7/doc/CR017_Accepted_Pits_Point_in_Time_Export.md)

## 0. Provider review and clarifications

RAIkeep accepts CR017 as a backward-compatible coordinated patch targeted at
v4.2.5. The AIA request is substantively aligned with the earlier RAIkeep
discussion draft. The following provider clarifications remove remaining
ambiguity and form part of the accepted implementation contract:

1. `--at` applies to both `--json` and `--out-dir`, for both a single pit and
   `--wwwa`.
2. AIA's phrase “references pointing to items not existing at `at` are
   omitted/unbound” means that the absent target item is omitted from the
   projected lookup and the source reference remains safely unresolved in the
   established WWWA representation. Export does not throw and does not silently
   delete or rewrite the source reference property.
3. `_export.exported` is captured once in UTC for the export document. It is
   provenance, not a synchronization boundary or proof of history completeness.
4. JsonPit's existing `GetAt(...)`, `ExportJson(..., at: ...)`, and
   `ProjectState(...)` semantics remain authoritative. PitSeeder must not
   implement a competing history algorithm.
5. `PitsExportRequest.At` and the CLI parser use offset-explicit
   `DateTimeOffset` values. Offset-free timestamps fail fast rather than being
   interpreted through the local machine timezone.
6. Default exports without `--at` retain their existing output shape. The
   `_export`/`data` envelope exists only when `--at` is present.
7. Implementation and coordinated 4.2.5 preparation were explicitly authorized.
   Tagging, publication, and release-chain execution remain behind RAI's later
   manual gate.

## 1. Purpose

Expose JsonPit's existing point-in-time projection capability through the
`pits export` command.

The requested capability is not a new persistence model. JsonPit already keeps
the timestamped PitItem history and already supports historical item and pit
projection. The missing boundary is a typed CLI option that lets a process,
agent, or operator request that projection through `pits`.

Proposed examples:

```bash
pits export Person --json --at 2026-08-27T12:00:00Z
pits export Person --out-dir ./exports --at 2026-08-27T12:00:00Z
pits export --wwwa --json --at 2026-08-27T12:00:00Z
pits export --wwwa --out-dir ./exports --at 2026-08-27T12:00:00Z
```

`--at` applies only to `export`. It is not an `audit`, `seed`, or deletion
option.

## 2. Existing capability and identified gap

JsonPit already provides the necessary historical projection primitives:

- `Pit.GetAt(string key, DateTimeOffset timestamp, bool withDeleted = false)`
  projects one PitItem at a requested timestamp.
- `Pit.ExportJson(..., DateTimeOffset? at = null, ...)` projects a complete pit
  at a requested timestamp.
- `PitItems.ProjectState(DateTimeOffset? at = null, ...)` applies timestamped
  history, deletion walls, and property tombstones.

Current `pits export ... --json` and `pits export ... --out-dir ...` do not
accept a timestamp. They always export the current projection. Current WWWA
export likewise resolves references from current projections.

`pits audit ... --json` is not an alternative: it exports durable events, not a
reconstructed PitItem state.

## 3. The two relevant times

Point-in-time export has two different and equally important times.

### 3.1 Projection time (`at`)

The caller-supplied timestamp is the historical cutoff. For every known
PitItem, the export projects all applicable history whose PitItem timestamp is
less than or equal to this value.

### 3.2 Export time (`exported`)

The export time records when `pits` generated the export from the history then
available to that invocation.

The export time is descriptive metadata. It is not a synchronization barrier,
a claim that all remote fragments had arrived, or a transaction timestamp.

## 4. Required temporal semantics

At the time the command is invoked, `pits` loads the histories available
through JsonPit's normal read boundary. It then projects each history using the
requested `--at` cutoff.

For each PitItem:

1. Consider all history available to this export invocation.
2. Ignore fragments timestamped after `--at`.
3. Project the applicable fragments timestamped at or before `--at` using
   JsonPit's established ordering, tombstone, deletion-wall, and resurrection
   rules.
4. Omit an item when it had no projected value at `--at`.
5. Omit an item when its projected state was deleted at `--at`.
6. Include the projected value exactly as its history produces it. Do not
   repair, reinterpret, or reconcile it against a later state.

This is a retrospective projection from the history known when the export is
executed. It is not a reconstruction of what one particular machine happened
to see at that historical wall-clock instant.

JsonPit's documented persistence model remains **asynchronous persistence with
eventual durability**. A remote or delayed fragment may arrive after the
historical time it describes. If that fragment is available when a later
export runs and its PitItem timestamp is at or before `--at`, it participates in
that later projection. Therefore, two exports using the same `--at` value may
legitimately differ when additional historical fragments have become available
between the two invocations.

The command must not wait for remote synchronization, declare the histories
complete, or imply repeatability that JsonPit's persistence model does not
promise.

## 5. WWWA projection and reference resolution

For `pits export --wwwa --at ...`, the same cutoff applies independently to all
four WWWA pits: Person, Object, Place, and Activity.

The command must:

1. Project each PitItem in each pit at the requested cutoff from the history
   available to the export invocation.
2. Omit items that did not exist or were deleted at that cutoff.
3. Build the existing one-level WWWA reference lookups from those projected
   results.
4. Resolve each reference according to its projected value without changing,
   repairing, or inferring the reference.
5. Preserve the established unresolved-reference representation when a target
   has no projected value at the cutoff.

This ordering prevents a current referenced value from leaking into a
historical export. It does **not** establish transactional or referential
consistency across the four pits. If the projected histories contain an
incomplete or temporarily inconsistent set of references, the export faithfully
reports that state.

In particular, the feature does not attempt to determine what all machines had
observed at the requested time. It considers every currently available PitItem
history and applies the requested timestamp to each history.

## 6. JSON shape and the point-in-time export envelope

The two timestamps are provenance of the exported content. A filename is only
one delivery mechanism: standard output has no filename, callers may select or
later rename a file, and a pipe may persist the content under an unrelated
name. The filename therefore cannot be the authoritative location of temporal
export metadata.

JSON comments are also unsuitable. Emitting JSONC would make `--json` cease to
be strict JSON and could break `jq`, standard JSON parsers, APIs, canonical
hashing, and consumers that discard comments.

### 6.1 Existing exports without `--at`

When `--at` is absent, the output remains exactly compatible with the existing
contract:

- a single-pit export is the established JSON array;
- a WWWA export is the established object containing the four pit arrays;
- established output filenames and caller-selected destinations remain
  unchanged;
- no metadata envelope is added.

### 6.2 Point-in-time exports with `--at`

When `--at` is present, both standard-output and file exports use one strict,
self-describing JSON envelope. Metadata is attached to the export document, not
to individual PitItems.

Single-pit example:

```json
{
  "_export": {
    "at": "2026-08-27T12:00:00.0000000Z",
    "exported": "2026-08-27T18:45:12.1234567Z"
  },
  "data": [
    {
      "Id": "Adele",
      "Modified": "2026-08-27T11:42:00Z"
    }
  ]
}
```

WWWA example:

```json
{
  "_export": {
    "at": "2026-08-27T12:00:00.0000000Z",
    "exported": "2026-08-27T18:45:12.1234567Z"
  },
  "data": {
    "Person": [],
    "Object": [],
    "Place": [],
    "Activity": []
  }
}
```

Envelope contract:

- `_export.at` is the requested cutoff converted to UTC.
- `_export.exported` is captured once in UTC when the export document is
  generated.
- `data` contains the same payload shape that the corresponding ordinary
  current-state export uses.
- Both timestamps use invariant round-trip UTC representation.
- The envelope itself is ordinary strict JSON, not JSONC.
- `--json` writes the complete envelope to standard output without diagnostic
  text contaminating the JSON stream.
- File export writes that same envelope and honors the established or
  caller-selected filename. Renaming the file does not destroy its provenance.

Consumers that need only the historical payload can select `.data`, for
example with `jq '.data'`.

## 7. CLI parsing contract

- Syntax: `--at <timestamp>`.
- Parse as `DateTimeOffset`, not as an unspecified local `DateTime`.
- Require an explicit `Z` or numeric UTC offset and fail fast on ambiguous
  offset-free values.
- Normalize the value to UTC for projection, filenames, help examples, and
  envelope metadata, help examples, and diagnostics.
- Accept `--at` for both single-pit and `--wwwa` exports and for both `--json`
  and `--out-dir` output modes.
- Preserve all existing export behavior when `--at` is absent.
- Document that a future cutoff projects all currently available history whose
  timestamps are no later than that cutoff; it does not wait until the future
  time arrives.

## 8. Typed `OsLibCore` command boundary

CR014 established `PitsCommand` as the typed external-call boundary and CR015
extended it for deletion commands. CR017 must preserve that architecture.

`PitsExportRequest` should expose an optional `DateTimeOffset? At` value. Its
argument builder must:

- omit `--at` when `At` is null;
- otherwise append exactly one `--at` token and one invariant, offset-explicit
  timestamp value;
- produce the same arguments for synchronous and asynchronous execution;
- avoid caller-built raw command strings.

The public API and command examples must be reflected in the `OsLibCore` and
`PitSeeder` README/API/release documentation belonging to the eventual release.

## 9. Compatibility requirements

- Existing `pits export` commands without `--at` are unchanged.
- Existing current-state JSON root shapes are unchanged when `--at` is absent.
- Historical export with `--at` uses the strict `_export`/`data` envelope.
- The value inside `data` retains the corresponding established single-pit or
  WWWA payload shape.
- Existing `Pit.GetAt(...)` and `Pit.ExportJson(..., at: ...)` behavior remains
  authoritative; the CLI must not invent a second projection algorithm.
- Existing one-level WWWA resolution and unresolved-wrapper behavior remain in
  force.
- No package version or target release is assigned by this discussion draft.
- Tagging and publication remain behind RAI's manual release gate after formal
  customer acceptance and implementation verification.

## 10. Explicit non-goals

CR017 does not introduce:

- a synchronization barrier or remote-provider wait;
- a promise that all historical fragments have arrived;
- an immutable snapshot of what a particular replica observed in the past;
- transaction-time or bitemporal storage;
- transactional consistency across pits;
- referential repair or historical data correction;
- an identity-management feature;
- history rewriting, compaction, or canonical-file mutation;
- a change to JsonPit's asynchronous-persistence/eventual-durability contract.

## 11. Acceptance coverage

The eventual implementation should verify at least:

1. A single item with values before, exactly at, and after the cutoff.
2. An item with no history at or before the cutoff is omitted.
3. Deletion at or before the cutoff omits the item.
4. A later resurrection is absent before its timestamp and present afterward.
5. Property and nested-property tombstones project correctly.
6. Equal-timestamp histories preserve JsonPit's deterministic ordering.
7. A delayed/backdated fragment can change a later invocation using the same
   cutoff, proving that the export uses history available at invocation time.
8. Single-pit `--json` and `--out-dir` produce equivalent payloads.
9. WWWA applies the same cutoff independently to all four pits.
10. WWWA does not resolve a historical reference from a target that exists only
    after the cutoff.
11. WWWA preserves an unresolved reference when its target has no projected
    value.
12. Current-state output without `--at` remains compatible.
13. Point-in-time file and standard-output exports contain the same strict JSON
    envelope with `at` and `exported` metadata.
14. The envelope's `data` value retains the established single-pit or WWWA
    payload shape.
15. Filenames remain independent from the authoritative timestamp metadata;
    renaming a saved export does not remove its provenance.
16. Standard output contains parseable JSON only when `--json` and `--nologo`
    are used.
17. Offset-bearing timestamps are converted to the same UTC instant.
18. Missing, malformed, or offset-free `--at` values fail with actionable help.
19. `PitsCommand.BuildExportArguments(...)` passes the optional timestamp as
    separate exact tokens for single-pit and WWWA requests.

Tests should exercise the real JsonPit projection code and the real `pits`
parser. They should test RAIkeep's wrapper and invocation behavior rather than
retesting an external binary's internal implementation.

## 12. Formal customer acceptance and implementation gate

AIA formally accepted all six review points in its Step 3 record: the two-time
distinction, retrospective projection over history available at invocation,
the absence of a cross-pit transaction guarantee, the conditional envelope,
in-document provenance independent of filenames, and preservation of unresolved
source references when a target has no projected value.

RAI then gave the explicit implementation go-ahead for coordinated v4.2.5.
RAIkeep implemented the parser, single-pit and WWWA projection paths, strict
envelope, typed OsLib request boundary, and regression coverage. The manual
release gate remains unchanged: this acceptance does not itself authorize a
push, tag, workflow dispatch, or NuGet publication.
