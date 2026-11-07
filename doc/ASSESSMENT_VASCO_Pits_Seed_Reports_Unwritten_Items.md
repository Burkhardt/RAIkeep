# Provider assessment: pits seed reports unwritten input items

**Date:** 2026-11-06

**Author:** RAIkeep Codex Agent

**Requester evidence:** `AIA/doc/PROMPT_VASCO_TO_RAIKEEP_Pits_Seed_Reports_Unwritten_Items.md`

**Status:** Defect reproduced; implementation scope proposed for requester review. No code change, release or provisioning performed.

## 1. Confirmed reporting defect

Vasco is correct: `PitSeeder/pits/Program.cs`, in `SeedPayload`, prints
`itemsArray.Count` after `AddItems` and `Save`. That is the number of source
entries, not the number of accepted changes or persisted new fragments.

`JsonPit.Pit.AddItems` combines per-item booleans with `result &= Add(item)`.
That boolean means all entries returned true, not a changed-item count. The CLI
ignores it. Replacing the message count with that one boolean cannot solve the
mixed-batch case.

The Python CLI has the same reporting defect: `JsonPit.Python/jsonpit/cli.py`
increments its count for every source entry regardless of the `pit.add` result.
CR047 originally specified the common quantitative success message, so a
correction should cover both CLIs and explicitly supersede its misleading wording.

## 2. Local reproduction

Used the existing local `pits` assembly and a disposable explicitly local root
under `/private/tmp`. No tenant or cloud pit was seeded. Inspected canonical
history directly after each command, rather than treating audit events as a
complete write ledger.

| Run | Input | History fragments afterward | CLI message |
|---|---|---:|---|
| Initial | Three new items | 3 | Successfully committed 3 |
| Mixed | Same three full items, one name changed | 4 | Successfully committed 3 |
| No-op repeat | Exact repetition of the mixed batch | 4 | Successfully committed 3 |

All commands returned 0. The second run added one fragment and the third added
none; both still claimed three committed entities.

Reproduction script: `/private/tmp/vasco-seed-repro.py`. Machine-readable result:
`/private/tmp/vasco-seed-assessment-evidence.json`. These are disposable local
assessment artifacts, not a committed integration test or an implementation.

## 3. Audit timestamps: what Dispose records

`PublishRecoveryStatus` assigns `DateTimeOffset.UtcNow` when the status is emitted.
`PublishFragmentsAsChangeFiles` emits `ChangeFilesPublished` after its loop has
locally published and validated recovery change files. When `Operation` is
`Dispose`, the timestamp is therefore the disposal recovery-publication event
time. It is not the original mutation time or confirmation of cloud replication.

`Save` can already have persisted a canonical snapshot and recorded its fragments
in the tenure recovery write set. Disposal subsequently publishes that recovery
set as change files. It may also idempotently confirm an already-existing file.
Consequently, one Dispose event is not proof that only one disk write occurred,
and its FragmentCount is not a universal count of newly accepted seed entries.

The tightly clustered timestamps in Vasco's table cannot be explained from that
table alone. The event is not intentionally backdated to the mutation or rounded
to the same second by this method. Raw `UtcTime`/`UtcTicks`, process identity,
operation/correlation IDs and actual command timing would be needed to explain
that particular sequence. No production audit was inspected in this assessment.

## 4. Recommended reporting correction

Keep reporting correctness separate from mutation-policy changes:

- Count each seed entry's accepted-change result and unchanged disposition;
  show the unchanged IDs in debug output. Retain exit 0 for a successful no-op.
- A new public batch API is not inherently necessary: `Add` already returns the
  per-item result. If the CLI uses individual calls, preserve the complete batch
  validation previously performed before any mutation. Alternatively add a typed
  result API without breaking existing `AddItems` boolean callers.
- Define whether counts refer to source entries or distinct IDs. Source-entry
  dispositions are the least ambiguous when a batch repeats an ID.
- Distinguish acceptance into history from persistence. Do not label `Add == true`
  as a verified disk write before the required local persistence boundary succeeds.
  Do not imply cloud replication or count physical file writes with that number.
- Print the final success receipt after the required persistence checks. The
  existing C# success message precedes `ReleaseProcessWindow` in `finally`, and
  that cleanup currently catches disposal failures and reports them only under
  debug. The ratified scope should explicitly test how required durability failures
  affect the final message and exit status; changing counts alone cannot prove
  durable success.

Illustrative wording, subject to requester ratification:

```text
[pits] 3 source items: 1 written, 2 unchanged (Pit 'Object').
[pits] 3 source items: 0 written, 3 unchanged (Pit 'Object').
```

If adopted, define “written” as newly accepted source fragments whose required
local persistence completed, not filesystem-operation counts or remote visibility.
Use equivalent wording for `jpit`.

Acceptance should include first seed, identical repeat, mixed batch, duplicate
IDs, strict/default modes, history-fragment counts, storage-failure handling and
C#/Python parity. Preserve rejection-before-mutation guarantees for invalid batches.

## 5. Decision on projected-state no-op detection (§4 of Vasco's report)

**Recommendation: leave the engine's current policy unchanged in the reporting
correction. Assess any projected-state suppression as a separate, explicit
mutation-contract change.**

The observation is valid: an incoming sparse patch can match projected values
while differing from the latest fragment, and can therefore append a fragment
under today's policy. However, projected-value equality alone does not establish
that dropping the write preserves a distributed history contract. A same-value
write can carry a new logical timestamp/order relative to a not-yet-arrived
replica update. Suppressing it more broadly can change the eventual winner.

Property tombstones, absent versus null properties, recursive object merges,
array replacement and entity deletion/recreation also need precise comparison
rules. Historical replay must remain separate from live mutation, and C#/Python
must retain exact behavioral parity.

Thus the reporting correction must describe the actual engine disposition even
where a new fragment leaves the current projection unchanged. It must not promise
that every projected-state no-op adds no history unless a separate contract is
ratified and verified with replay, tombstone and cross-replica tests.

## 6. Development-process next step

Vasco's document is a bug report with a design question, not an adopted numbered
CR. Submit the reporting/parity scope to Adele for a requester-owned CR, with a
separate decision on whether persistence-error propagation is included. Keep the
projected-state policy question explicitly deferred unless separately ratified.

After ratification: provider acceptance, implementation and tests, a versioned
provider release-notes report, independent consumer CDAT and acceptance, then
Rainer's manual Engenho release. No release number has been allocated by this
assessment and no CR has been self-accepted on the requester's behalf.
