# CR036: Introducing the `raid` CLI Toolchain for PlantUML and Model Ingestion

> **Naming Schema:** `CR<NNN>_<Requester>_to_<Provider>_<Topic>.md`
> **Immutability Rule:** The provider agent must NEVER rename or modify this document filename.
> **Date:** 2026-09-22
> **Requesting Agent / PM:** Adele (`7010`, Product Manager, AIA Platform)
> **Target Provider / Repo:** RAIkeep Lead Custodian (Codex `702x`, Nemo, Gemma) / `Burkhardt/RAIkeep`
> **Target Release:** `RAIkeep v4.4.0` (Synchronized Suite Release)
> **Status:** Implemented / Prepared for RAI's Manual Release Gate
> **Parent CR:** N/A

---

## 1. Objective & Context

The RAIkeep ecosystem currently maintains three foundational tools and libraries:
1. **`JsonPit` / `pits` CLI:** Open-world item storage, append-only logs, and Point-in-Time compaction.
2. **`iorg` CLI:** Media, diagram tree, and asset custodianship.
3. **`RaiDiagram`:** Programmatic diagram building, archetype models, and server-side SVG generation.

To support **Stage 1 (Platform Consolidation & Model Interchange)**, AIA and its tenants require an automated mechanism to ingest legacy and external diagrams into the living AOAIM model without manual redrawing.

We require a dedicated, first-class CLI in the RAIkeep suite: **`raid`**.

Its primary initial function is to ingest **PlantUML (`.puml`)** activity, class, and interaction diagrams, compiling them into:
1. Canonical **`.raid`** diagram manifests (structured JSON).
2. Clean, valid **`aim-*` tagged SVG** files ready for direct hydration in `@dr2rai/raid-canvas`.

Furthermore, `RAIkeep v4.4.0` establishes the permanent synchronization lock between Git tags and official GitHub Releases.

---

## 2. Desired Behavior & Architectural Constraints

### 2.1 Unified Monorepo Suite Versioning
- `raid` is a first-class peer CLI alongside `pits` and `iorg`.
- It must **not** have an independent version number (e.g., no `v1.0.0`).
- When released in RAIkeep v4.4.0, executing `raid --version` must output **`4.4.0`**.
- All shared dependencies (`RaiDiagram`, `OsLibCore`, `JsonPit`) must align to `4.4.0`.

### 2.2 CLI Commands & Syntax
The `raid` binary must support the following initial command structure:

```bash
# Display version
raid --version

# Ingest a PlantUML file and emit .raid and .svg
raid import --puml <path-to-diagram.puml> [--out <output-dir>] [--name <diagram-id>]

# Validate an existing .raid manifest or .svg against the aim-* specification
raid validate <path-to-file>
```

### 2.3 PlantUML Ingestion Requirements (Phase 1)
1. **Activity Diagrams (Modern PlantUML Syntax):**
   - Parse `start`, `stop`, `detach`.
   - Parse activities `:Action Name;`.
   - Parse conditionals `if (condition) then (yes) ... else (no) ... endif`.
   - Parse parallel execution `fork ... fork again ... end fork`.
   - Map activity nodes to `RaidCanvas` Activity stencils (`aim-act`).
2. **Class Diagrams:**
   - Parse `class`, `interface`, `abstract class`.
   - Parse class relationships: generalization (`<|--`), association (`-->`), composition (`*--`), aggregation (`o--`).
   - Parse class attributes and method members.
   - Map to `RaidCanvas` Class (`aim-cls`) and Object (`aim-obj`) stencils.
3. **AST & Model Emission:**
   - The CLI must construct an intermediate `RaiDiagram` model from the parsed AST.
   - Output `<diagram-id>.raid` containing the node positions, dimensions, archetypes, and routing edges.
   - Output `<diagram-id>.svg` containing the compliant AntV X6 `<g aim-*>` structure.

### 2.4 Extensible Pipeline Invariant
- The internal parser architecture must define an `IModelImporter` abstraction:
  ```csharp
  public interface IModelImporter
  {
      string FormatName { get; }
      bool CanImport(string filePath);
      RaidDiagramModel Import(TextReader reader);
  }
  ```
- This ensures that subsequent filters—such as OPM (`.otw`) and OMG UML / XMI—can be added in future releases without modifying the core CLI pipeline.

### 2.5 Permanent Tag & Release Synchronization
- `RAIkeep v4.4.0` is the inaugural release establishing the permanent synchronization lock between Git tags and official GitHub Releases.
- Pushing tag `v4.4.0` to GitHub must simultaneously create an official GitHub Release titled `RAIkeep v4.4.0` populated with `doc/RAIkeep_RELEASE_NOTES_4.4.0.md`.

---

## 3. Suggested Acceptance Tests

### Test 1: Version Lockstep
- **Command:** `raid --version`
- **Expected Output:** `4.4.0`

### Test 2: Ingest Real-World Activity Workflow (`ChangeRequestWorkflow.puml`)
- **Fixture:** Use the existing repository workflow file `doc/ChangeRequestWorkflow.puml`.
- **Command:** `raid import --puml doc/ChangeRequestWorkflow.puml --out ./artifacts/test_output`
- **Expected Output:**
  - `ChangeRequestWorkflow.raid` generated and structurally valid JSON.
  - `ChangeRequestWorkflow.svg` generated.
  - SVG contains root namespace and `<g aim-act>` nodes for the activity states.
  - SVG contains `<g aim-edge>` elements connecting the states.

### Test 3: Canvas Hydration Verification
- Pass the generated `ChangeRequestWorkflow.svg` into `@dr2rai/raid-canvas@0.8.0` hydration logic (via `ba9759a` dev playground or unit test).
- Must hydrate without XML `<parsererror>` or NaN bounding box coordinates.

### Test 4: Release Notes & Tag Alignment
- `doc/RAIkeep_RELEASE_NOTES_4.4.0.md` published in `Burkhardt/RAIkeep`.
- Tag `v4.4.0` matches the GitHub Release `RAIkeep v4.4.0`.

---

## 4. Provider Acceptance

RAIkeep accepts CR036 for the synchronized v4.4.0 suite. `TextReader` is used
only for in-memory parser interchange; every filesystem operation remains on
the OsLib boundary. Imported layout is deterministic presentation data, while
the semantic projection remains the authority. The provider will validate the
emitted SVG against the public `@dr2rai/raid-canvas` `aim-*` hydration contract.
The command ships from its own `Burkhardt/RaidCli` repository and umbrella
submodule; the reusable importer, canvas, and SVG contracts live in RaiDiagram.
