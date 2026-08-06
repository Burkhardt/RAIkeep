# Release Notes: PitSeeder (pits CLI) v3.13.2

**Date:** 2026-08-05  
**Author / Delivering Agent:** RAIkeep Dev Agent  
**Delivered Version:** v3.13.2  
**Target Consumers:** AIA, AfricaStage, RAIkeep operators  
**Status:** Implemented — coordinated 3.13.2 line; NuGet publication pending release authorization

---

## 1. Summary

`pits` 3.13.2 aligns the CLI with the coordinated JsonPit concurrency contract: it adds
the strictly read-only `--events` audit mode for JsonPit recovery events and routes
finite CLI shutdown through JsonPit's full durability boundary.

## 2. Resolved Change Requests (CRs)

- [`CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md`](CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md) — PitSeeder share of the coordinated v3.13.2 work (`pits --events` audit mode; CR003 disposal boundary for finite CLI runs).

## 3. Root Cause Analysis & Technical Resolution

- Recovery diagnostics were previously invisible to operators. `pits --events` now
  reads a pit's durable audit events through JsonPit's `PitAudit` (backed by OsLib's
  `EventDirectory`) **without** opening a `Pit`, creating a process flag, touching
  `Master.flag`, merging change files, or writing an audit event. Audit routing runs
  before any `Pit` construction.
- Finite CLI runs previously only tombstoned their activity window. They now dispose
  each opened `Pit` through the CR003 durability boundary (change-file export first,
  optional canonical save while still exact master, then window/watcher/registry
  release). `--retain-window` still opts out and keeps the activity window until its
  normal timeout.

## 4. Public Contract & API / Package Changes

- New: `pits -r <root> <PitName> --events`
  - `--event-machine all|local|<machine>` (default `all`)
  - `--event-level <level>` — case-insensitive inclusive minimum
    (`Trace|Debug|Information|Warning|Error|Critical`, default `Trace`)
  - with `--json`: emits the filtered events as a JSON array; otherwise human-readable
    lines ordered deterministically by machine, UTC time, and event identity.
  - Audit mode requires one positional pit name; `--wwwa --events` is rejected
    (outside CR003). Invalid levels and missing values produce clear CLI errors with
    zero side effects.
- Package/tool version 3.13.2; consumes `JsonPit 3.13.2` and `OsLibCore 3.13.2`.

## 5. Validation & Acceptance Evidence

- `pits.Tests`: 13 passed, 0 failed, 0 skipped — including the new
  `EventsAuditModeTests` (all/local/named-machine filters, inclusive severity,
  case-insensitivity, deterministic ordering, JSON parseability, and before/after
  filesystem snapshots proving zero side effects) and the updated
  `LocalCliTicketWindowTests`, which exercise real separate CLI processes and prove
  exact-PID master inheritance after the previous CLI process released its window.
- Deployed and verified on the configured remote node Mzansi (`pits v3.13.2`,
  self-contained linux-x64), including seeding against the OneDrive-backed root.

## 6. Upgrade & Consumption Instructions

- Install/update the `pits` tool to 3.13.2 on **every** machine sharing a pit
  (pre-3.13.2 binaries can fail when merging 3.13.2 hashed change files).
- Inspect recovery activity with, for example:
  `pits -n -r <root> Person --events --event-level warning`
  or `pits -n -r <root> Person --events --json | jq`.
