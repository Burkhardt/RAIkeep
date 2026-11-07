# CR081 — `pits` and `jpit` Seed Disposition Reporting (`written` vs. `unchanged`) & Post-Persistence Receipt

* **CR ID:** CR081
* **From (Requirer):** Adele (`7010`, Product Manager — AIA Platform) & Vasco (`7015`, Lead Ontologist — AIA)
* **To (Provider):** Codex (`7001`, Custodian & Systems Architect — RAIkeep)
* **Cc:** Dr. Reiner Burkhardt (`RAI`), Zébio (`7011`, Lead Backend Engineer — AIA)
* **Date:** 2026-11-06
* **Target Release:** RAIkeep `v4.6.2` (bundled alongside [`CR078`](CR078_AIA_to_RAIkeep_Rail_Multi_Path_Input_Completeness.md))
* **Supersedes (in part):** CR047 quantitative seed receipt wording (`Successfully committed <N> entity(ies)`)
* **References:**
  - [`doc/PROMPT_VASCO_TO_RAIKEEP_Pits_Seed_Reports_Unwritten_Items.md`](PROMPT_VASCO_TO_RAIKEEP_Pits_Seed_Reports_Unwritten_Items.md)
  - `/Users/RSB/Projects/GitHub/RAIkeep/doc/ASSESSMENT_VASCO_Pits_Seed_Reports_Unwritten_Items.md`

---

## 1. Problem Statement

When seeding a pit via `pits seed <PitName> --source <file>` (C#) or `jpit seed` (Python), the CLI prints:

```text
[pits] Successfully committed <N> entity(ies) to Pit '<Name>'.
```

where `<N>` is `itemsArray.Count` — the number of entries in the input file — rather than the number of entries actually written as new history fragments. When a seed batch is repeated (no-op) or only modifies a subset of entries (mixed batch), both `pits` and `jpit` still report all `<N>` source entries as committed. Furthermore, in `PitSeeder/pits/Program.cs`, the success message is emitted before `ReleaseProcessWindow` in the `finally` block completes disposal and recovery-file publication.

---

## 2. Ratified Scope & Architectural Rulings

Following Codex's assessment (`ASSESSMENT_VASCO_Pits_Seed_Reports_Unwritten_Items.md`), we ratify all four provider recommendations:

### R1. Separate `written` and `unchanged` Source-Entry Counts (C# `pits` & Python `jpit`)
1. Track the per-entry disposition across every source entry in the input batch (`written` when `Add(item)` appends a new fragment to history; `unchanged` when `Add(item)` returns `false` because the entry matches the latest fragment).
2. Counts refer to **source entries** in the input payload (the least ambiguous measure when a batch contains multiple entries).
3. Supersede CR047's quantitative receipt line in both `pits` and `jpit` with:
   ```text
   [pits] <N> source items: <W> written, <U> unchanged (Pit '<Name>').
   ```
   *(and the equivalent `[jpit] <N> source items: <W> written, <U> unchanged (Pit '<Name>').` in Python `jpit`)*.
4. Under `--debug` (`-b`), log the list of unchanged item IDs.
5. Preserve exit code `0` for a valid seed operation even when `0 written, <N> unchanged` (an idempotent re-seed is a successful no-op, not an error).
6. Preserve complete pre-mutation batch validation (including `-x` / `--id-exists` / `--patch` target checks) before any item is mutated.

### R2. Emit Success Receipt Only After Required Local Persistence Completes
1. "Written" means newly accepted source fragments whose required local persistence (`Save` and process-window / disposal publication) completed without error.
2. Emit the final success receipt **after** `Save()` and local disposal/recovery publication succeed, and propagate required local persistence/disposal failures as non-zero exit errors rather than swallowing them after printing a success line.

### R3. Keep Projected-State No-Op Suppression Out of Scope (Preserve Distributed Ordering)
1. **Explicit Ruling on Vasco §4:** Do **not** change `AppendFragment`'s equality check (`EqualsIgnoringModified(top, item)` against the latest fragment) to compare against projected state.
2. As Codex's assessment established (§5), suppressing a sparse write solely because its values match the current local projection can alter distributed eventual-consistency winners when a concurrent replica update is in flight, and interacts non-trivially with property tombstones and replay. Latest-fragment deduplication remains the sole engine rule.

### R4. Audit Timestamp Semantics Documented (`Dispose`)
1. Confirm as documented behavior that `Dispose` / `ChangeFilesPublished` audit events record `DateTimeOffset.UtcNow` at disposal recovery-publication time, not the original mutation timestamp or remote cloud replication time. (The clustered `22:26:29–30Z` timestamps in Vasco's report occurred because the four `pits seed` commands were executed in a single chained shell invocation.)

---

## 3. Consumer-Driven Acceptance Tests (CDAT)

1. **CDAT-1 (Initial Seed):** Seeding 3 new items into a disposable pit adds 3 history fragments, exits `0`, and prints `3 source items: 3 written, 0 unchanged`.
2. **CDAT-2 (Idempotent Repeat / No-Op):** Re-running the exact same 3-item seed adds 0 history fragments, exits `0`, and prints `3 source items: 0 written, 3 unchanged` (and lists the 3 unchanged IDs when `--debug` is passed).
3. **CDAT-3 (Mixed Batch):** Re-running the 3-item seed with 1 item modified and 2 unchanged adds 1 history fragment, exits `0`, and prints `3 source items: 1 written, 2 unchanged`.
4. **CDAT-4 (Strict `-x` / `--patch` Rejection Before Mutation):** Running `pits seed -x` with 1 valid modified item and 1 non-existent item ID rejects the entire batch before mutating the pit (0 fragments added, non-zero exit code).
5. **CDAT-5 (Post-Persistence Receipt Ordering):** The success line is printed only after local persistence and disposal succeed; a simulated persistence/disposal failure exits non-zero and does not print the success receipt.
6. **CDAT-6 (C# `pits` & Python `jpit` Parity):** Both `pits` and `jpit` pass CDAT 1–5 with matching disposition counts and exit codes.
