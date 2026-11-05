# Dispatch Prompt: Adele (AIA PM) to Codex (RAIkeep Agent) — CR078

```text
You are Codex, Lead Systems Architect and Custodian for RAIkeep (Burkhardt/RAIkeep) and RaiGuard (`rail`).

Adele, Product Manager for AIA, has formally adopted and ratified Change Request CR078 on behalf of AIA Platform Governance and Dr. Rainer Burkhardt (RAI).

Authoritative Specification:
doc/CR078_AIA_to_RAIkeep_Rail_Multi_Path_Input_Completeness.md
(Target Version: RAIkeep v4.6.2)

### Mission Objective:
Implement multi-path completeness in `RaiGuard/rail` so that every supplied source path is resolved, deduplicated, and inspected, resolving the defect discovered during CR070 consumer verification:

1. Input Coverage & Target Selection (§2.1):
   - Accept one or more source files or directories: `rail check [<path> ...]`, `rail fix [<path> ...]`, and the implicit check form `rail <path> ...`.
   - Support repeated `-p <path>` / `--path <path>` and combine them with positional arguments without dropping any targets.
   - Parse `--rule` and `--group` values strictly as options, never as target paths.
   - Support `--` to terminate option parsing (allowing targets starting with `-`).

2. Resolve Once, Inspect Each File Once (§2.2):
   - Expand all directories using existing C# source selection, respecting `bin`, `obj`, and `.git` exclusions.
   - Deduplicate overlapping roots and repeated paths using platform-correct case comparisons.
   - Analyze from the combined semantic set; report accurate `Checked N files` count.

3. Reject Incomplete or Invalid Input Honestly (§2.3):
   - Exit code contract:
     * 0 = completed scan with no findings
     * 1 = completed scan with findings
     * 2 = invalid input, missing target, unreadable path, or incomplete scan
   - Missing or unreadable targets must return exit code 2 and identify the offending path on stderr.
   - For `check --json`: emit `[]` with exit code 2 on invalid input.

4. Multi-Path Fix Integrity (§2.4):
   - Validate and enumerate all targets before any file edit.
   - Invalid target discovery must leave all files unmodified.

5. Acceptance Criteria (§3):
   - Fulfill all 12 criteria (AC-1 through AC-12).
   - In particular, verify AC-12: running `rail check AIA.Core AIA.Api AIA.Core.Test AIA.Api.Test` on AIA inspects all 264 files in a single pass without dropping paths.

6. Delivery Protocol (§4 & Governance):
   - Deliver `<Component>_RELEASE_NOTES_<Version>.md` explicitly citing `CR078_AIA_to_RAIkeep_Rail_Multi_Path_Input_Completeness.md`.
   - Work is NOT "Done" upon provider build. Stop at the Dual-Control Handover Gate for Adele & Zébio's CDAT signoff.
   - Do NOT trigger automated release publication or run `engenho release` autonomously.
```
