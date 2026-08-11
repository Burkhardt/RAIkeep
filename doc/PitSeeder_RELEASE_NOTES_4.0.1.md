# Release Notes: PitSeeder v4.0.1

**Date:** 2026-08-10
**Author / Delivering Agent:** RAIkeep Dev Agent
**Delivered Version:** v4.0.1
**Target Consumers:** AfricaStage, AIA
**Status:** Prepared — publication approval pending

## 1. Summary

PitSeeder v4.0.1 adds command-first `seed`, `export`, and `audit` interfaces to
`pits`. Established flat seed/export invocations continue to work during the
`4.x` transition, while the recent audit flag family moves directly to the new
command surface.

## 2. Resolved Change Requests (CRs)

- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — implements contextual subcommands and isolated operation options for `pits`.

## 3. Root Cause Analysis & Technical Resolution

The flat parser inferred its operation from combinations of `-s`, `-e`,
`--json`, `--wwwa`, and `--events`. That made unrelated options appear together
and allowed invalid combinations to reach late execution-intent checks.

The v4.0.1 entry point now selects the command parser only when the first token
is `seed`, `export`, or `audit`. All other input follows the established parser.
Both paths normalize into the existing execution handlers; no second seeding,
exporting, or auditing implementation was introduced.

Command validation now rejects unknown, missing, mutually exclusive, and
out-of-scope options before filesystem or JsonPit work begins. Contextual help is
available through `pits <command> --help`.

## 4. Public Contract & API / Package Changes

Preferred syntax:

```text
pits seed (<PitName> | --wwwa) --source <file-or-directory>
pits export (<PitName> | --wwwa) (--out-dir <dir> | --json)
pits audit (<PitName> | --wwwa) [--machine <filter>] [--level <severity>] [--json]
```

- `--json` remains available for machine-readable audit output.
- `-c`/`--cloud` accepts only providers present in `Os.Config.DefaultCloudOrder`
  with a non-empty `Os.Config.Cloud` path. A provider path alone no longer makes
  that provider selectable, and matching remains case-insensitive.
- Top-level help presents those providers in configured order, marks the first
  as the configured default, and uses the filled number glyph for the selected
  provider. The resolved root appears once on `-r`/`--pitroot`; the redundant
  second PitRoot status line was removed.
- `audit --wwwa` aggregates the four WWWA event directories and preserves
  deterministic machine/time/event ordering.
- `--events`, `--event-machine`, and `--event-level` are intentionally not part
  of legacy compatibility. They fail with guidance to `audit`, `--machine`, and
  `--level`.
- Existing flat seed/export syntax remains supported throughout `4.x`.
- The legacy parser is scheduled for removal in `5.x.x`; see
  [`CLI-PARSER-TRANSITION-4.x-TO-5.x.md`](CLI-PARSER-TRANSITION-4.x-TO-5.x.md).
- Startup banner rules no longer use repeated equals characters.

## 5. Validation & Acceptance Evidence

- `PitSeeder.Tests`: **20 passed, 0 failed, 0 skipped**.
- Executable-process coverage proves command seed/export routing, legacy export
  equivalence, target/output mutual exclusion, contextual help, command-only
  audit migration, WWWA audit aggregation, JSON filtering, and zero audit
  filesystem side effects.
- Process-level version coverage proves `pits --version` emits `pits v4.0.1`.
- Debug builds complete with zero warnings and zero errors.

## 6. Upgrade & Consumption Instructions

1. Update the coordinated RAIkeep tool line to v4.0.1 after publication approval.
2. Prefer the command syntax above for new scripts.
3. Existing seed/export scripts may migrate during `4.x`.
4. Replace audit flags immediately:
   `--events` → `audit`, `--event-machine` → `--machine`, and
   `--event-level` → `--level`.
5. Independently validate operational scripts and record the requester-led
   CR006 Accepted/Rejected evaluation.
