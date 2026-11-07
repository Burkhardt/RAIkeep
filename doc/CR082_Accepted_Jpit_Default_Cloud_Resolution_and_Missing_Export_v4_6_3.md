# CR082 Accepted — `jpit` Default-Cloud Resolution & Missing Export Sources (`v4.6.3`)

**Date:** 2026-11-07  
**Requirer / Reviewing Agent:** Adele (`7010`, Product Manager — AIA Platform) on behalf of AfricaStage (`Sipho 7001`, `Eliza 7000`) & AIA  
**Delivering Agent:** Codex (`7001`, Custodian & Systems Architect — RAIkeep)  
**Target Release:** `RAIkeep v4.6.3` (`jsonpit-python` / `jpit v4.6.3`)  
**Status:** **ACCEPTED (Independent Consumer CDAT Passed)**  
**References:**
- [`/Users/RSB/Projects/GitHub/RAIkeep/doc/CR082_AfricaStage_to_RAIkeep_Jpit_Default_Cloud_Resolution_and_Missing_Export.md`](file:///Users/RSB/Projects/GitHub/RAIkeep/doc/CR082_AfricaStage_to_RAIkeep_Jpit_Default_Cloud_Resolution_and_Missing_Export.md)
- [`/Users/RSB/Projects/GitHub/RAIkeep/doc/JsonPit.Python_RELEASE_NOTES_4.6.3.md`](file:///Users/RSB/Projects/GitHub/RAIkeep/doc/JsonPit.Python_RELEASE_NOTES_4.6.3.md)
- [`/Users/RSB/Projects/GitHub/AIA/doc/CR082_Accepted_Jpit_Default_Cloud_Resolution_and_Missing_Export_v4_6_3.md`](file:///Users/RSB/Projects/GitHub/AIA/doc/CR082_Accepted_Jpit_Default_Cloud_Resolution_and_Missing_Export_v4_6_3.md)

---

## 1. Independent Consumer-Driven Acceptance Testing (CDAT) Summary

Independent CDAT was executed on Nkosikazi against the candidate `jpit v4.6.3` binary (`/Users/RSB/Projects/GitHub/RAIkeep/JsonPit.Python/bin/jpit`) and full Python test suite:

| Scenario | Command / Verification | Result |
| :--- | :--- | :--- |
| **1. Candidate Version** | `python3 JsonPit.Python/bin/jpit --version -n` | `jpit v4.6.3` (Exit `0`) |
| **2. Default-Cloud JSON Export (`-c` omitted)** | `python3 JsonPit.Python/bin/jpit export Object -r AfricaStage --json -n` | Resolved `OneDrive` default cloud automatically; returned all **312** live `AfricaStage/Object` entities including `Themba.NomsaBandWeb` (Exit `0`). |
| **3. Default-Cloud Directory Export (`-c` omitted)** | `python3 JsonPit.Python/bin/jpit export Object -r AfricaStage --out-dir /tmp/cdat-cr082-out -n` | Wrote `/tmp/cdat-cr082-out/Object.json` (`260 KB`) from `OneDrive` without treating `AfricaStage` as a relative local directory (Exit `0`). |
| **4. Missing Snapshot Failure & Output Preservation** | `python3 JsonPit.Python/bin/jpit export MissingPit -r AfricaStage --out-dir /tmp/cdat-cr082-out -n` | Returned **Exit `1`**, emitted **0 bytes** on `stdout`, printed canonical `.pit` path on `stderr` (`Pit error: Export source pit does not exist: .../AfricaStage/MissingPit/MissingPit.pit`), and preserved existing `/tmp/cdat-cr082-out/Object.json` SHA-256 unchanged. |
| **5. Full Python Test Suite (`test_cr082_cloud_export.py` + regression)** | `PYTHONPATH=. pytest -q` in `RAIkeep/JsonPit.Python` | **198 passed in 4.20s** (including all 50 CR082 test cases and 17 CR081 seed disposition cases). |
| **6. Explicit-Destination Write Safeguard (CR069)** | Preserved | Mutations (`seed`, `put`, `set`, `delete-*`, `rename`, `maintain --apply`) continue to require an explicit cloud or explicit local path syntax. |

---

## 2. Sign-Off & Next Step

**CR082 is formally accepted.** Codex is authorized to synchronize the suite version metadata and manifest for `v4.6.3` so Dr. Burkhardt can run `engenho release 4.6.3` and `engenho provision all`.
