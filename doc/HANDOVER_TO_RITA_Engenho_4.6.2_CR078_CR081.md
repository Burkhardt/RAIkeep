# Engenho handover: RAIkeep 4.6.2 candidates, CR078 and CR081

**Date:** 2026-11-06

**For:** Rita, Engenheira / Engenho Custodian

**Status:** Provider preparation complete; consumer CDAT and Rainer's manual release remain required. This document does not authorize execution.

The formal provider report is
[RAIkeep_RELEASE_NOTES_v4.6.2.md](RAIkeep_RELEASE_NOTES_v4.6.2.md), addressing
`CR078_AIA_to_RAIkeep_Rail_Multi_Path_Input_Completeness.md` and
`CR081_AIA_to_RAIkeep_Pits_and_Jpit_Seed_Disposition_Reporting_and_Persistence_Receipt.md`.

## Release inputs

- `scripts/release-manifest.json` prepares all twelve child repositories at 4.6.2.
- Python publication entries reference fresh artifacts under
  `/private/tmp/raikeep-4.6.2-candidates/python/`; jsonpit and jpit are paired.
- Preserve the configured workflow names, dependency graph, companion-package
  visibility checks and umbrella-last publication. No shell-chain changes are
  needed or requested.
- Local commits and exact child SHA pointers are prepared. There have been no
  pushes, tags, publications, release executions or fleet installs in this work.
- Gate release on independent requester acceptance. Rainer runs
  `engenho release 4.6.2` manually afterward; provisioning is a separate manual
  operation after publication.

## CR081 seed runner implications

The old `Successfully committed <N> entity(ies)` success text is superseded:

```text
[pits] 3 source items: 1 written, 2 unchanged (Pit 'Object').
[jpit] 3 source items: 0 written, 3 unchanged (Pit 'Object').
```

If an Engenho runner parses the old sentence, update it to this source-entry
contract. A no-op is exit 0; `written + unchanged == source items`. Do not infer a
failure from zero writes or claim every input changed. Repeated IDs are counted
per source entry, not per distinct entity.

The receipt follows required local Save/cleanup. Persistence failures are
nonzero and have no final receipt. Trust both the exit status and receipt;
progress lines or a matching projected value do not prove persistence. Do not
invent JSON fields: CR081 changes the textual receipt only.

Debug unchanged IDs are on stderr. “Written” confirms required local persistence,
not remote cloud replication. C# disposal audit time is recovery-publication time,
not original mutation or remote visibility time. Projected-state no-op suppression
has not been introduced.

## CR078 rail runner implications

`rail check` can now accept all project paths in one invocation. Repeated `-p` /
`--path` combines with positional targets. Overlaps are deduplicated.

Check exits: 0 clean, 1 findings, 2 invalid input/incomplete inspection. With
`--json`, an input failure emits `[]` plus stderr and exit 2. Do not interpret
an empty diagnostic array alone as a successful scan. `fix` validates all targets
before edits; later failures can leave already-applied fixes.

Keep installed version verification in the provisioning task so a stale binary
cannot silently stand in for the candidate under acceptance. Vikela remains
optional development tooling; production nodes should not receive it by default.

No changes were made to Engenho's source or deployed service by this handover.
