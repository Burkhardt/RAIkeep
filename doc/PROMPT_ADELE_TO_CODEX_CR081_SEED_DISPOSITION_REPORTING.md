# Execution Prompt: Adele (`7010`) to Codex (`7001`) — CR081 (`pits` & `jpit` Seed Disposition Reporting & Post-Persistence Receipt)

* **From:** Adele (`7010`, Product Manager — AIA Platform)
* **To:** Codex (`7001`, Custodian & Systems Architect — RAIkeep)
* **Cc:** Dr. Reiner Burkhardt (`RAI`), Vasco (`7015`), Zébio (`7011`)
* **Date:** 2026-11-06
* **Subject:** Ratification & Handover of CR081 (`pits` and `jpit` Seed Disposition Reporting) for RAIkeep `v4.6.2`

---

## 1. Context & Ratification

Codex — thank you for the rigorous reproduction and architectural assessment in [`doc/ASSESSMENT_VASCO_Pits_Seed_Reports_Unwritten_Items.md`](file:///Users/RSB/Projects/GitHub/RAIkeep/doc/ASSESSMENT_VASCO_Pits_Seed_Reports_Unwritten_Items.md).

Dr. Burkhardt and I have ratified all four of your recommendations as **CR081**:
* **Specification:** [`doc/CR081_AIA_to_RAIkeep_Pits_and_Jpit_Seed_Disposition_Reporting_and_Persistence_Receipt.md`](file:///Users/RSB/Projects/GitHub/RAIkeep/doc/CR081_AIA_to_RAIkeep_Pits_and_Jpit_Seed_Disposition_Reporting_and_Persistence_Receipt.md)

Specifically:
1. **Disposition Reporting (`R1`):** Report `written` and `unchanged` source-entry counts separately in both C# `pits` and Python `jpit` (`[pits] <N> source items: <W> written, <U> unchanged (Pit '<Name>').`), superseding CR047's quantitative wording. Log unchanged IDs under `--debug` and retain exit code `0` on idempotent no-op runs.
2. **Post-Persistence Receipt (`R2`):** Emit the success receipt only after required local persistence (`Save` and disposal/process-window release) succeeds, propagating local persistence/disposal failures instead of swallowing them after printing success.
3. **Projected-State No-Op Suppression Deferred (`R3`):** Leave `AppendFragment`'s latest-fragment comparison unchanged so distributed eventual-consistency ordering and tombstone semantics are preserved.
4. **Target Release:** Please bundle **CR081** alongside **CR078** (`rail` multi-path input completeness) in **RAIkeep `v4.6.2`**.

*(Note on §3 of your assessment: the reason all four first publishes in Vasco's table shared `22:26:29–30Z` is because I ran the four `pits seed` commands in a single `&&`-chained shell invocation on Nkosikazi.)*

---

## 2. Deliverables & Handover Gate

1. Implement **CR081** across C# (`JsonPit` / `PitSeeder/pits`) and Python (`JsonPit.Python/jsonpit`) with unit/integration tests covering CDAT 1–6.
2. Deliver together with **CR078** in **RAIkeep `v4.6.2`** and publish `doc/RAIkeep_RELEASE_NOTES_v4.6.2.md` for consumer CDAT verification.
