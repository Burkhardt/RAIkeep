# Release Notes: RAIkeep v4.6.2

**Date:** 2026-11-06

**Author / Delivering Agent:** Codex (`7001`), RAIkeep Custodian / Provider

**Delivered Version:** v4.6.2 candidate; all twelve child repositories synchronized

**Target Consumers:** AIA (Adele, Vasco, Zébio), AfricaStage and Engenho

**Status:** Provider implementation, tests and local release preparation complete; awaiting independent consumer CDAT. Not published or provisioned by this work.

## 1. Summary

This candidate bundles CR078 and CR081. `rail` inspects every supplied source
path rather than silently checking only the first. `pits seed` and `jpit seed` /
`put` report actual source-entry dispositions after required local persistence,
so a successful no-op is distinguishable from a write.

All twelve child repositories are prepared on local `main` commits at 4.6.2.
Eleven NuGet packages and three Python distributions have been built and checked.
No remote branch push, tag, publication, release, install or provisioning was
executed. Independent consumer acceptance remains a prerequisite to Rainer's
manual Engenho release; successful publication is a separate subsequent state.

## 2. Resolved Change Requests (CRs)

The following requests are implemented in the candidate and submitted for
consumer evaluation, not self-accepted or closed by the provider:

- [CR078_AIA_to_RAIkeep_Rail_Multi_Path_Input_Completeness.md](CR078_AIA_to_RAIkeep_Rail_Multi_Path_Input_Completeness.md)
  — Combine all explicit/positional targets, deduplicate source files, inspect
  the complete semantic set, validate inputs before fixes, and report invalid or
  incomplete checks honestly. Detailed report:
  [RaiGuard_RELEASE_NOTES_4.6.2.md](RaiGuard_RELEASE_NOTES_4.6.2.md).
- [CR081_AIA_to_RAIkeep_Pits_and_Jpit_Seed_Disposition_Reporting_and_Persistence_Receipt.md](CR081_AIA_to_RAIkeep_Pits_and_Jpit_Seed_Disposition_Reporting_and_Persistence_Receipt.md)
  — Count written/unchanged source entries, emit the receipt after required local
  persistence, preserve latest-fragment policy, and document disposal-event time.
  Supersedes the quantitative success wording in
  [CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md](CR/CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md).

## 3. Root Cause Analysis & Technical Resolution

### CR078 — complete rail inputs

The old parser returned the first positional target; an explicit path option
also overrode positional input. Later arguments could disappear while the CLI
reported a clean scan. The new shared parser accumulates all targets, consumes
filter values correctly, supports `--`, and rejects unknown or incomplete options.
Selection normalizes actual filesystem entry names, deduplicates overlapping
inputs, excludes generated directories, and validates the complete set before
any fix. Operational failures return 2 with stderr diagnostics. One semantic
compilation covers the combined source set.

The original AIA measurement on November 5 was 264 files. On November 6 the
consumer checkout contains **279 eligible files** in these same four projects:
**84 + 67 + 62 + 66**. The packaged candidate's combined and separate scans agree.
These are measured checkout counts, not constants built into the implementation.

### CR081 R1 — truthful source-entry dispositions

C# printed `itemsArray.Count` and Python incremented a counter for every input,
regardless of whether a fragment was accepted. C# now counts each `Pit.Add`
result after the existing complete payload/strict-target validation. Python does
the equivalent with `pit.add`. Existing public `AddItems` boolean APIs are not
changed, and no public write wrapper or static factory is introduced.

New tests exposed an additional Python parity defect: its append path stamped
identical input before comparison and returned true. It now compares the latest
fragment, ignoring only `Modified`, before timestamping. Typed canonical JSON
comparison distinguishes JSON booleans from numbers (`false` versus `0`). This
matches the existing C# rule; it does not introduce projected-state suppression.

Counts refer to source entries, including repeated IDs, rather than distinct
entities or physical file writes. The unchanged-ID list is emitted on stderr
under `-b` / `--debug`.

### CR081 R2 — persistence before the receipt

C# previously printed success before its `finally` cleanup, where disposal
errors were caught and reported only under debug. The seed path now emits its
final receipt only after Save and required cleanup complete, and propagates
disposal errors through the CLI's nonzero error boundary. It also checks that an
owned activity flag did not remain after attempted disposal.

Python explicitly saves before leaving the context and prints the receipt only
after context exit. `close()` now raises `OSError` when required release fails
and the activity flag is still owned by this process, rather than silently
accepting the failed deletion. Local I/O failures return exit 1 without a success
receipt. An error does not promise batch rollback; some fragments may already
have become locally durable before a later persistence failure.

The explicit `--window` opt-out retains its existing behavior: Save must succeed,
while the process window is intentionally retained until timeout. It is covered
in both CLI test suites. Default commands complete required disposal/release.

### CR081 R3 / R4 — preserved policy and audit meaning

C# `AppendFragment` is unchanged. Sparse patches are compared against the latest
fragment, not the current projection. A patch whose values already exist in the
projection can still append when the latest fragment differs. Tombstones,
timestamps, live identity and both tracking modes remain covered by tests.

C# `Dispose` / `ChangeFilesPublished` events record current UTC when recovery
change-file publication is reported after validation. They do not timestamp the
original mutation or confirm remote cloud replication, and are not a complete
ledger of canonical Save operations. Adele confirmed that the clustered
22:26:29–30Z events in the original report came from four commands in one
`&&`-chained shell invocation.

### Implementation locations

- `PitSeeder/pits/Program.cs`: per-entry accounting, receipt ordering and strict
  seed cleanup error propagation. The internal test boundary substitutes I/O
  operations without adding production CLI/environment test switches.
- `JsonPit.Python/jsonpit/cli.py`: seed/put receipts, debug IDs, explicit Save and
  I/O exit status.
- `JsonPit.Python/jsonpit/store.py`: C# latest-fragment comparison parity and
  failed owned-window release propagation.
- `RaiGuard/rail/`: complete parser, source selection and check/fix boundary.
- C#, Python and runtime tests plus component documentation.

## 4. Public Contract & API / Package Changes

### Seed receipt

```text
[pits] 3 source items: 3 written, 0 unchanged (Pit 'Object').
[pits] 3 source items: 0 written, 3 unchanged (Pit 'Object').
[pits] 3 source items: 1 written, 2 unchanged (Pit 'Object').
```

Python uses the same wording with `[jpit]`. The old
`Successfully committed <N> entity(ies)` sentence is superseded intentionally.
Scripts matching that sentence must migrate. A successful no-op still exits 0;
persistence/disposal failures exit nonzero and emit no final success receipt.
“Written” means newly accepted source fragments whose required local persistence
completed, not remote replication, distinct IDs, or a count of filesystem writes.
Zero-entry default seeds report zero dispositions; strict empty patches remain
rejected before mutation.

Debug example:

```text
[pits] Unchanged IDs: ["Alice","Bob","Carol"]
```

### rail inputs and exits

```text
rail check [<path> ...] [--rule <id>] [--group <name>] [--json]
rail fix [<path> ...] [--rule <id>] [--group <name>] [--dry-run]
```

Positional paths and repeated `-p` / `--path` options combine. `--` terminates
option parsing. No targets still means the current directory. Check exits are
0 completed/clean, 1 completed/findings, 2 invalid input/incomplete inspection.
On an invalid JSON check, stdout is `[]`, stderr explains the failure, and the
exit is 2. The diagnostic-array schema is unchanged. Fixes validate all targets
before writing; later execution failures can leave already-applied fixes.

### Synchronized packages

The candidate includes **11 NuGet packages**: Amafu, OsLibCore, RaiUtils, RaiImage,
RaiDiagram, RaidSeeder, JsonPit, ImgSeeder, PitSeeder, RaiGuard, RaiGuard.Analyzer;
and **3 Python distributions**: jsonpit, jpit, vikela. All versions and coordinated
dependencies are 4.6.2. Standalone jpit is regenerated at 4.6.2.

Vikela remains optional development tooling, with no new runtime dependency from
jsonpit/jpit and no automatic installation on production nodes.

The release manifest points to fresh 4.6.2 Python artifacts, retains companion
jpit / RaiGuard.Analyzer visibility checks and uses the established workflow
names. No release-chain orchestration logic was changed. The consistency check
now recognizes required versioned provider reports while still rejecting flat
major-version histories outside `doc/releases/`.

## 5. Validation & Acceptance Evidence

| Provider check | Result |
|---|---|
| `dotnet test RAIkeep.slnx` | **1,246 passed; 0 failed; 0 skipped**, across 11 test projects, including existing remote-sync scenarios |
| Python runtime / CLI tests | **148 passed**, including 17 new CR081 cases and explicit local cross-engine tests |
| Vikela tests | **71 passed** in an existing development environment |
| Targeted JsonPit reference/history/recovery tests | **36 passed**, including both-mode CR081 policy cases |
| Release consistency suite | **141 checks passed** |
| Release-tool regression tests | **10 passed** |
| Formatter source parity | Passed |
| Package builds / metadata | **11 NuGet + 3 Python distributions**, 17 package archives; all 4.6.2; Twine checks passed |
| Extracted-package smoke tests | Five .NET CLI versions, jpit, Vikela, standalone jpit, shared-pit seed receipts and packaged rail coverage passed |

The full .NET build retains existing xUnit analyzer warnings in older test files;
the test pass count is not a claim of a new zero-warning framework build baseline.
No warning bypass or new test skip was introduced to obtain these results.

### CR081 acceptance mapping

| Gate | Provider evidence |
|---|---|
| CDAT-1 | Three new entries produce three accepted/persisted fragments, exit 0, and `3 written, 0 unchanged` in both engines. |
| CDAT-2 | Exact repeat preserves fragment count, exits 0, reports `0 written, 3 unchanged`, and lists IDs under debug. |
| CDAT-3 | One changed entry among three appends one fragment and reports `1 written, 2 unchanged`. |
| CDAT-4 | Existing strict-patch regressions plus new Python coverage prove entire-batch rejection before mutation; invalid later lifecycle payloads are also tested. |
| CDAT-5 | The real C# CLI error boundary is exercised with simulated Save/disposal failures. Python tests inject Save, close and owned-window release failures. All return nonzero without the receipt; ordering tests prove receipt follows successful Save/cleanup. |
| CDAT-6 | Explicit C#-first and Python-first scenarios operate on the same disposable pit, alternate writers, preserve combined canonical/change-file history and match disposition/error results. |

Additional coverage checks repeated source IDs, retained-window compatibility,
JSON type distinctions, sparse patches that match projection but differ from
the latest fragment, tombstones, original live identity and both tracking modes.

### CR078 acceptance mapping

All AC-1–AC-12 provider evidence is recorded in
[RaiGuard_RELEASE_NOTES_4.6.2.md](RaiGuard_RELEASE_NOTES_4.6.2.md). Final packaged
coverage on the current consumer checkout is **279 = 84 + 67 + 62 + 66**. The
existing stderr advisory about incomplete project-reference resolution remains;
complete file coverage does not replace compiler-analyzer validation.

### Artifacts and provenance

- Candidate feed: `/private/tmp/raikeep-4.6.2-candidates/nuget/`.
- Python wheels/sdists: `/private/tmp/raikeep-4.6.2-candidates/python/`.
- Standalone source artifact: `JsonPit.Python/bin/jpit`.
- Review-only extracted tools: `/private/tmp/cr081-package-smoke/`.
- [Machine-readable evidence and source commits](verification/CR081_4.6.2_Evidence.json).

Package repository commit metadata matches the prepared local child commits.
All thirteen remotes (umbrella plus twelve children) were checked read-only:
no existing v4.6.2 tag was found at preparation time. No tag was created or moved.

Packaging used existing tools and cached backend files in temporary storage.
No pip/tool install or fleet installation ran. Local candidates from an initial
pack pass were moved out of the shared NuGet cache into private review storage,
so later public-feed validation cannot mistake them for published packages.

## 6. Upgrade & Consumption Instructions

### Consumer CDAT before publication

Adele / Vasco / Zébio should independently evaluate CR081 CDAT-1–CDAT-6 and CR078
AC-1–AC-12 against this candidate, then issue acceptance or rejection with an
improvement request. Cite this exact provider filename,
**RAIkeep_RELEASE_NOTES_v4.6.2.md**, and the exact applicable CR filenames.

Use local candidates without changing installed fleet tools:

```zsh
dotnet /Users/RSB/Projects/GitHub/RAIkeep/PitSeeder/pits/bin/Debug/net10.0/pits.dll -v
dotnet /Users/RSB/Projects/GitHub/RAIkeep/RaiGuard/rail/bin/Debug/net10.0/rail.dll -v

cd /Users/RSB/Projects/GitHub/AIA
dotnet /Users/RSB/Projects/GitHub/RAIkeep/RaiGuard/rail/bin/Debug/net10.0/rail.dll \
  check AIA.Core AIA.Api AIA.Core.Test AIA.Api.Test -n
```

For Python, use the source checkout or extracted wheel with Python 3.12+:

```zsh
PYTHONPATH=/Users/RSB/Projects/GitHub/RAIkeep/JsonPit.Python \
  python3 -m jsonpit.cli -v
```

Run seed/failure tests only on disposable local roots. Use `--debug` to inspect
unchanged IDs and check the process exit status. Read history through the engine
so change-file fragments count alongside canonical history.

### Rainer's manual release after consumer acceptance

```zsh
cd /Users/RSB/Projects/GitHub/RAIkeep
engenho release 4.6.2
```

The manifest and exact prepared gitlinks are committed locally for that future
operation. This command is documented, **not executed** by the provider. After
publication completes, use the separately established manual Engenho provisioning
command; no legacy install script is required or run here.

Rita's integration notes are in
[HANDOVER_TO_RITA_Engenho_4.6.2_CR078_CR081.md](HANDOVER_TO_RITA_Engenho_4.6.2_CR078_CR081.md).
The provider stops at this handover gate; test success is not consumer signoff,
and preparation is not publication.
