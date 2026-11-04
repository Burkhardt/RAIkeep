# CR077: Vikela and JsonPit Mutation Guardrails

> **Naming Schema:** `CR077_AIA_and_AfricaStage_to_RAIkeep_Vikela_and_JsonPit_Mutation_Guardrails.md`  
> **Parent CR:** `CR040_AIA_and_jsonpit_to_RAIkeep_Protected-Attributes-and-In-Memory-Delta-Compaction.md`, `CR069_AIA_to_RAIkeep_PitsCommand-Tenant-Scoping-and-Public-Contracts.md`, `CR070_AIA_to_RAIkeep_RAI007-Test-Run-Switches-and-RAI011-RAI015-Subject-Sites.md`  
> **Immutability Rule:** The provider agent must NEVER rename or modify this document filename.

**Date:** 2026-11-04  
**Requesting Agent / PM:** Adele (`7010`, PM AIA Platform) on behalf of AIA Platform, Eliza (`7000`, PM AfricaStage), Sipho (`7001`, AfricaStage Lead Dev), Rita (`7016`, Engenho Lead), and Dr. Rainer Burkhardt (`RAI`, Chief Product Officer)  
**Target Provider / Repo:** Codex (`7001`, Custodian & Systems Architect) / `Burkhardt/RAIkeep` & `Burkhardt/vikela`  
**Status:** Ratified & Dispatched to RAIkeep  
**Target Release:** RAIkeep `v4.6.0` / Vikela `v0.1.0`

---

## 1. Objective & Consumer Problem

### 1.1 The Operational Background
Across the AIA and AfricaStage production fleet, state mutations to JsonPit entities (`Person`, `Object`, `Place`, `Activity`) are the core mechanism of record. In multi-tenant, cloud-replicated environments:
1. **Full-Snapshot Read-Modify-Write Hazards (`RAI011`):** Reading an item, mutating one field on the in-memory snapshot, and writing the entire item back stomps concurrent writes from cloud replicas, erasing remote fields and causing `ProtectedAttributeException` failures.
2. **Roslyn Analyzer False Positives:** Sipho and Zébio resolved dozens of `RAI011` and `RAI012` analyzer warnings, but encountered brittle compiler heuristics where variables merely ending in `Pit` triggered false alarms, while legitimate tracked live mutations were flagged incorrectly.
3. **The Python Guardrail Vacuum:** While C# developers benefit from Roslyn analyzers, Python harnesses in `jsonpit`, `iorg`, `amafu`, and Engenho have had zero static mutation guardrails, risking silent data corruption across the Python substrate.
4. **Preserving Natural Object-Oriented APIs:** Developers must not be forced into artificial static wrapper facades or clumsy boilerplate to satisfy an overly aggressive linter. The natural, idiomatic object model must remain primary and expressive.

### 1.2 Ratified Scope
AIA, AfricaStage, and Engenho formally adopt and ratify the implementation plan developed by Dr. Burkhardt and Codex (`doc/PLAN_Pitlint_and_JsonPit_Guardrails.md`), establishing the canonical identity **`Vikela`** (*isiZulu: "to protect / shield"*):
- **Establish `Vikela`:** A dedicated Python mutation guardrail tool and Pylint checker plugin (`Burkhardt/vikela`), packaged as an optional development tool separate from the `jsonpit` runtime.
- **Sharpen C# `RAI011` and `RAI012`:** Refine the Roslyn analyzer (`RaiGuard`) to track semantic receiver types, variable lifetimes, execution order, and live handles, eliminating false positives on AfricaStage fixtures.
- **Enforce Mutation Parity:** Preserve the object-oriented mutation contract identically across C# and Python.
- **The `--qondisa` Straightening Action:** Provide an official `--qondisa` CLI alias for `--fix` (*"straighten out the mutations"*), pairing the protective shield with active rectification.
- **Zero Production Intrusion:** Keep Vikela optional, decoupled from production runtime dependencies, and orchestrate deployment via Rita's Engenho runner.

---

## 2. Project Identity & Distribution Contract

| Surface | Canonical Name |
| :--- | :--- |
| **Project Name** | **Vikela** |
| **GitHub Repository** | `Burkhardt/vikela` |
| **PyPI Distribution** | `vikela` |
| **Python Import Module** | `vikela` |
| **Standalone CLI** | `vikela` |

- **Decoupling Invariant:** Vikela is strictly optional development tooling. It must **never** be added as a required dependency of the core `jsonpit` runtime or `jpit` CLI.
- **Dual-Mode Operation:** Functions both as a standalone CLI command (`vikela <path>`) and as a native Pylint checker plugin (`pylint --load-plugins=vikela ...`).

---

## 3. Preserving the Object-Oriented Mutation Contract

The existing object model remains primary and authoritative. Consumers shall not introduce static payload generators, application-specific write wrappers, or artificial facades.

### 3.1 C# Mutation Primitives
The following idiomatic operations must be fully supported and recognized as compliant by analyzers:
- Live indexing: `pit[key]["Field"] = value` (tracked live mutation emitting sparse delta).
- Explicit methods: `SetProperty`, `Merge`, `ExtendWith`, `DeleteProperty`, `DeletePropertyPath`.
- Sparse construction: `var delta = new PitItem(id); delta.ExtendWith(patch); pit.Add(delta);`.
- Tracked deletion: `Remove` on a tracked live handle emitting an authoritative tombstone.

### 3.2 Python Mutation Parity
The Python `jsonpit` implementation must guarantee the exact same observable mutation semantics:
- Live item indexing and property assignment.
- Identical distinction between:
  1. **Same-owner live handles** (tracked in-memory instances).
  2. **Detached snapshots / projections** (read-only or requiring explicit sparse delta extraction).
  3. **Fresh items** (newly constructed instances).
- Rejection of cross-owner live writes and unsafe client lifecycle payloads.
- Explicit historical replay (never offered as a loophole around client guards).

---

## 4. Analyzer Precision & Rule Sharpening

The C# Roslyn analyzer (`RaiGuard.Analyzer`) and Python `Vikela` checker must implement matching analytical semantics:

1. **Semantic Receiver Resolution:** Resolve actual receiver types and method signatures rather than relying on variable name heuristics (e.g. matching identifiers ending in `Pit`).
2. **Handle Lifetime & Alias Tracking:** Track fresh items, same-owner live handles, detached projections, and unknown values across aliases, type casts, reassignments, method scopes, helpers, and collections.
3. **Execution Order Respect:** Analyze dataflow chronologically. A later assignment cannot retroactively change the classification of an earlier write.
4. **Soundness & Graceful Uncertainty:** Distinguish proven violations from unresolved static analysis. When dataflow cannot be proven, do not emit false-positive warnings merely because a value originated from an indexer or `Get` call.
5. **Preserve Valid Deletions:** Do not introduce a blanket prohibition on collection removals. A live tracked removal emitting a tombstone is fully compliant.
6. **Diagnostic Guidance:** Reconcile all diagnostic messages with CR040 guidance, providing actionable object-oriented advice and documentation links.

---

## 5. Programmer-Facing Diagnostics & CLI Experience

### 5.1 Finding Contract
Every finding emitted by `RaiGuard` or `Vikela` must provide:
- Rule ID (e.g. `RAI011`, `RAI012`, or Pylint-native symbol `vikela-full-snapshot-write`).
- Severity (`Warning` / `Error`).
- File path, Line, and Column.
- Detailed reason explaining the concurrent cloud sync hazard.
- Actionable object-oriented remediation guidance.
- Canonical documentation link.

### 5.2 Standalone CLI Experience (`vikela`)
- **Visual Styling:** Adhere strictly to `doc/cli-style.md` for terminal help, colors, and Nerdfont badge integration (🛡️ shield badge).
- **Machine Readability:** Support `--json` output emitting pure JSON on stdout with all diagnostics routed to stderr.
- **Documented Exit Codes:**
  - `0`: Success, zero lint findings.
  - `1`: Lint findings detected.
  - `2`: CLI syntax or configuration error.
  - `4`: Internal or environment failure.
- **Safety Invariant & The Straightening Alias:** Default checks must **never** edit source files. Automatic fixes (`--fix`) are strictly opt-in and restricted to proven safe transformations; linters must never infer a patch by silently dropping fields.
  - **The `--qondisa` Alias:** The CLI must support `--qondisa` as a first-class, official alias for `--fix` (*"straighten out the mutations"*), celebrating our Southern African substrate heritage.

### 5.3 Editor & Interactive Integrations
- **VS Code:** Native integration via Microsoft's Pylint extension with `vikela` configured in the active environment (`pylint.args: ["--load-plugins=vikela"]`).
- **PyCharm:** External Tool definition with file/line navigation in Milestone 1; native inspection plugin in Milestone 2.
- **JupyterLab / Notebooks:** Support IPython cell magic (`%load_ext vikela`, `%%vikela`) and standalone notebook scanning (`vikela notebook.ipynb`).

---

## 6. Acceptance Evidence & Verification Fixtures

Analysis accuracy and zero-regression must be proven against real codebase history from AfricaStage, including:
- **`1710524`:** Original before-state exhibiting 36 `RAI011` findings under analyzer `4.5.13`.
- **`8ef1bb3`:** Authoritative `RAI011` conformance commits.
- **`2a66ee4`:** Cleaned `RAI002` / `RAI003` sites.
- **`fbf5d32`:** Certified test report proving elimination of false positives (specifically verifying the 3 genuine findings vs false alarms).
- **The 19 Sipho Probes:** Coverage across the 19 distinct test probes and 7 boundary cases authored during Sprint 2644/2645.

### 6.1 Runtime Parity Suite
Validation must verify:
1. Live handle identity preservation.
2. Sparse delta generation and compaction.
3. Protected attribute immutability.
4. Tombstone persistence and propagation.
5. Dual-mode tracking (live vs snapshot).
6. Save and reload determinism.
7. Independent multi-process replication over cloud drives (proving cross-replica safety).
8. Strict C# vs Python semantic parity.

---

## 7. Engenho Handover & Fleet Provisioning

1. **Release Orchestration:** Rita's Engenho runner (`7016`) will manage package building, versioning, and fleet publication. The legacy `release-chain.sh` script is formally retired for Vikela.
2. **Selective Deployment:** Fleet provisioning must keep Python runtime tools (`jsonpit`, `jpit`) and optional development tools (`vikela`) independently selectable.
3. **Zero Production Bloat:** `vikela` must **not** be installed on production server nodes (e.g. Mzansi, Ingwe) by default. It is provisioned exclusively on developer workstations and CI runners.

---

— Ratified on 2026-11-04 by Adele (`7010`, PM AIA Platform) on behalf of AIA, AfricaStage, and Engenho.
