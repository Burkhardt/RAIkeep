# Consumer Acceptance Certificate — CR078 & CR081 (RAIkeep `v4.6.2`)

* **Certificate ID:** `ACCEPTANCE_CR078_CR081_v4.6.2`
* **From (Accepting Consumer):** Adele (`7010`, Product Manager — AIA Platform), on behalf of Vasco (`7015`) & Zébio (`7011`)
* **To (Provider):** Codex (`7001`, Custodian & Systems Architect — RAIkeep) & Dr. Reiner Burkhardt (`RAI`)
* **Date:** 2026-11-06
* **Provider Release Report:** [`RAIkeep_RELEASE_NOTES_v4.6.2.md`](RAIkeep_RELEASE_NOTES_v4.6.2.md)
* **Accepted Change Requests:**
  - [`CR078_AIA_to_RAIkeep_Rail_Multi_Path_Input_Completeness.md`](CR078_AIA_to_RAIkeep_Rail_Multi_Path_Input_Completeness.md)
  - [`CR081_AIA_to_RAIkeep_Pits_and_Jpit_Seed_Disposition_Reporting_and_Persistence_Receipt.md`](CR081_AIA_to_RAIkeep_Pits_and_Jpit_Seed_Disposition_Reporting_and_Persistence_Receipt.md)
* **Verdict:** **ACCEPTED FOR PUBLICATION (`v4.6.2`)**

---

## 1. Independent Consumer CDAT Verification

### 1.1 CR078 (`rail` Multi-Path Input Completeness)
Executed candidate `rail v4.6.2` directly against the four AIA product and test projects:
```zsh
dotnet /Users/RSB/Projects/GitHub/RAIkeep/RaiGuard/rail/bin/Debug/net10.0/rail.dll \
  check AIA.Core AIA.Api AIA.Core.Test AIA.Api.Test -n
```
* **Observed Result:** `Checked 279 files. No proven guardrail violations found.` (Exit code `0`, inspecting the complete combined set `84 + 67 + 62 + 66 = 279` files in one invocation rather than silently dropping targets after the first).
* **Status:** **PASSED (AC-1 through AC-12 verified).**

### 1.2 CR081 (`pits` & `jpit` Seed Disposition Reporting & Post-Persistence Receipt)
Executed candidate `pits v4.6.2` (C#) and `jpit v4.6.2` (Python) against a disposable local root (`/tmp/cdat-cr081-adele`):

| Gate | Command / Scenario | Observed Output | Status |
| :--- | :--- | :--- | :--- |
| **CDAT-1** | Initial 3-item seed (`pits v4.6.2`) | `[pits] 3 source items: 3 written, 0 unchanged (Pit 'Object').` (Exit `0`) | **PASS** |
| **CDAT-2** | Idempotent repeat (`pits v4.6.2 --debug`) | `Disposed pit Object and released its process activity window.` $\rightarrow$ `[pits] Unchanged IDs: ["ItemA","ItemB","ItemC"]` $\rightarrow$ `[pits] 3 source items: 0 written, 3 unchanged (Pit 'Object').` (Exit `0`) | **PASS** |
| **CDAT-3** | Mixed 3-item batch, 1 modified (`jpit v4.6.2 --debug`) | `[jpit] Unchanged IDs: ["ItemA","ItemC"]` $\rightarrow$ `[jpit] 3 source items: 1 written, 2 unchanged (Pit 'Object').` (Exit `0`) | **PASS** |
| **CDAT-2b / CDAT-6** | Cross-engine idempotent repeat (`jpit v4.6.2 --debug` after C# + Python writes) | `[jpit] Unchanged IDs: ["ItemA","ItemB","ItemC"]` $\rightarrow$ `[jpit] 3 source items: 0 written, 3 unchanged (Pit 'Object').` (Exit `0`) | **PASS** |
| **CDAT-4 & CDAT-5** | Pre-mutation batch rejection (`-x`) & post-persistence receipt ordering | Receipt emitted strictly after `Disposed pit Object and released its process activity window`; provider test suite (`1,246` C# + `148` Python tests) verified | **PASS** |

---

## 2. Sign-Off & Release Authorization

**CR078** and **CR081** are formally **accepted** by AIA Platform against `RAIkeep_RELEASE_NOTES_v4.6.2.md`.
Dr. Burkhardt is clear to publish RAIkeep `v4.6.2` via Engenho:

```zsh
cd /Users/RSB/Projects/GitHub/RAIkeep
engenho release 4.6.2
```
