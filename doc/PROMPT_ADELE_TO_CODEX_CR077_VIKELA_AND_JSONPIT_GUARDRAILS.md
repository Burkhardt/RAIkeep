# Dispatch Prompt: Adele (AIA PM) to Codex (RAIkeep Agent) — CR077

```text
You are Codex, Lead Systems Architect and Custodian for RAIkeep (Burkhardt/RAIkeep) and Vikela (Burkhardt/vikela).

Adele, Product Manager for AIA, has ratified Change Request CR077 on behalf of AIA Platform Governance, AfricaStage, Engenho, and Dr. Rainer Burkhardt (RAI).

Authoritative Specification:
doc/CR077_AIA_and_AfricaStage_to_RAIkeep_Vikela_and_JsonPit_Mutation_Guardrails.md
(Parent: CR040, CR069, CR070; Adopts doc/PLAN_Pitlint_and_JsonPit_Guardrails.md with official name "Vikela")

### Mission Objective:
Implement Deliverables in RAIkeep (RaiGuard.Analyzer, jsonpit) and establish the Vikela package (Burkhardt/vikela), targeting Release v4.6.0 / v0.1.0:

1. Project Identity & Architecture:
   - Establish Burkhardt/vikela as an optional Python development tool.
   - Dual invocation: standalone CLI (`vikela`) and Pylint plugin (`pylint --load-plugins=vikela`).
   - Strict decoupling: never make Vikela a dependency of jsonpit or jpit runtimes.

2. Preserve the Object-Oriented Mutation Contract:
   - Zero static facades, wrappers, or boilerplate write generators.
   - Support live indexing, SetProperty, Merge, ExtendWith, DeleteProperty, and fresh PitItem construction.
   - Guarantee exact behavioral parity between C# and Python live handle tracking, detached projections, and tombstones.

3. Sharpen C# Roslyn Analyzer (RaiGuard):
   - Enhance RAI011 and RAI012 with semantic receiver type resolution (stop relying on variable names ending in "Pit").
   - Track handle lifetimes and aliases across scopes, casts, reassignments, and collections.
   - Analyze execution order chronologically; distinguish proven violations from unresolved static dataflow.
   - Preserve valid collection removals emitting tombstones.

4. Implement Python Vikela Analyzer:
   - Pylint checker implementing the Python counterparts to RAI011/RAI012.
   - Output contract: styled terminal output per doc/cli-style.md (🛡️ badge), machine-readable --json mode, and standard exit codes (0 = clean, 1 = findings, 2 = syntax/config, 4 = internal error).
   - Zero source-file edits by default; auto-fixes opt-in and restricted to proven safe transformations.
   - The `--qondisa` Alias: Provide `--qondisa` as an official first-class alias for `--fix` ("straighten out the mutations").
   - JupyterLab support: cell magic (%%vikela) and notebook scanning (vikela notebook.ipynb).

5. Acceptance & Verification Fixtures:
   - Validate against AfricaStage historical commits (1710524, 8ef1bb3, 2a66ee4, fbf5d32).
   - Verify elimination of false positives across the 19 Sipho probes and 7 analysis boundary cases.
   - Prove cross-replica multi-process safety and C#/Python runtime parity.

6. Engenho Handover:
   - Coordinate release orchestration and packaging with Rita's Engenho runner (retire release-chain.sh for Vikela).
   - Ensure selective fleet provisioning (zero development lint tooling installed on production server nodes).
```
