# CR009 — RaiDiagram Package

**Requesting product:** AIA  
**Requesting PM:** Adele  
**Receiving product:** RAIkeep  
**Target release:** RAIkeep v4.2.0  
**Date:** 2026-08-13  
**Status:** Approved — ready for RAIkeep implementation

## 1. Request

AIA requests a new public RAIkeep package named **RaiDiagram**. The package shall extract reusable, domain-neutral diagramming capabilities from application-specific modeling workflows without moving AIA's WWWA modeling responsibilities into RAIkeep.

The canonical diagram manifest extension shall be:

```text
.raid — Rai Agentic Interactive Diagram
```

Example: `ScheduleRehearsal.raid`.

The `.raid` manifest is the authoritative diagram source. PlantUML source and rendered images are derived artifacts.

## 2. Motivation

AIA agents such as Yebo create and maintain domain models. A diagram is a selective view over such a model: it may display only part of the model and it adds presentation intent such as grouping, theme, annotations, and layout hints. It must not silently contradict the model it claims to represent.

PlantUML is an effective rendering language, but generated `.puml` text is not a sufficient model-consistency contract. It mixes semantic statements with renderer syntax and presentation directives, and it does not provide a stable, provider-neutral way to resolve source elements or explain drift to an agent.

RaiDiagram therefore needs two complementary capabilities:

1. a durable, agent-readable semantic and presentation manifest; and
2. a provider interface through which an application can expose the current model for reconciliation.

## 3. Agreed architectural boundary

The following decisions are fixed for CR009:

1. **RaiDiagram is domain-neutral and public-safe.** It shall not reference AIA, AfricaStage, WWWA, tenant-specific domain types, or private schemas.
2. **AIA owns modeling.** AIA stores and evolves WWWA facts and implements the RaiDiagram model-provider contract in `AIA.Core`.
3. **`.raid` owns view intent.** Diagram type, selected model references, semantic projection, grouping frames, themes, annotations, and layout hints belong in the `.raid` manifest rather than the domain model.
4. **One model element may appear in many diagrams.** No diagram-specific presentation data shall be added to domain entities merely to support a rendering.
5. **Rendered SVGs point back to their authority.** PlantUML SVG output shall embed the `.raid` identity and semantic hash in machine-readable SVG metadata.
6. **PlantUML is the primary v4.2 renderer.** Mermaid may be added later behind the same renderer boundary, but feature parity is not part of this request.

## 4. Package dependencies and release chain

RaiDiagram should depend on:

- **RaiUtils** for common exceptions, deterministic hashing, diagnostics, cancellation, and other dependency-light primitives;
- **OsLibCore** for `RaiPath`, files, temporary artifacts, and process/tool boundaries; and
- **RaiImage** for rendered image artifacts and supported image operations.

It shall not depend on JsonPit or AIA.

The intended dependency direction is:

```text
RaiUtils ──┐
           ├──> RaiDiagram
OsLibCore ─┤
           │
RaiImage ──┘

AIA.Core ──> RaiDiagram
   │
   └── implements IDiagramModelProvider for WWWA
```

RaiDiagram should be built and published after RaiUtils, OsLibCore, and RaiImage. Existing packages that do not consume RaiDiagram need not acquire a dependency on it.

## 5. The `.raid` manifest

### 5.1 Responsibilities

A `.raid` manifest shall contain enough structured information to:

- identify the diagram independently of its file location;
- identify the model and provider scheme it expects;
- record the model revision observed when the semantic projection was last reconciled;
- reference model elements without importing their domain types;
- represent the diagram's semantic elements and relationships;
- record only those source facts relevant to the diagram;
- distinguish semantic content from presentation intent;
- reapply optional selection rules to find newly in-scope or no-longer-in-scope elements;
- produce deterministic semantic and presentation hashes;
- compile to PlantUML without a live model provider; and
- produce a structured and agent-readable model diff when a provider is available.

### 5.2 v1 serialization decision

The v1 representation shall be versioned UTF-8 **JSON5** using the `.raid` extension. Strict JSON is a valid JSON5 subset and shall therefore also be accepted. JSON5 gives people and agents comments, trailing commas, single-quoted strings, and readable unquoted property names while retaining a structured JSON-compatible value model.

Parsing and authoring syntax shall remain separate from semantic identity. After parsing, RaiDiagram shall normalize the supported JSON5 values into a strict canonical JSON representation before computing semantic or presentation hashes. Comments, whitespace, quote style, property order, and trailing commas shall not affect those hashes.

Free-form JSON5 comments are authoring aids and are not model facts. Content that must survive every programmatic rewrite shall be represented in structured fields such as `purpose`, `description`, or `annotations`. Whether structural edits preserve otherwise free-standing comments is a confirmation item in section 15.

An illustrative, non-final shape is:

```json5
{
  // The .raid identity is independent of this file's path.
  schemaVersion: '1.0',
  diagram: {
    id: 'ScheduleRehearsal',
    title: 'Schedule rehearsal',
    kind: 'UseCase',
    purpose: 'Show the roles involved in scheduling a rehearsal',
  },
  model: {
    providerScheme: 'aia-wwwa',
    modelId: 'AfricaStage',
    capturedRevision: 'wwwa-revision-184',
  },
  projection: {
    elements: [],
    relationships: [],
    selectionRules: [],
  },
  presentation: {
    theme: 'AfricaStage',
    frames: [],
    layoutHints: [],
  },
  annotations: [],
}
```

The example provider scheme is application-owned data, not a dependency or built-in RaiDiagram provider.

### 5.3 Separation inside the manifest

The schema shall distinguish at least these categories:

| Category | Meaning | Included in semantic hash |
|---|---|---:|
| Identity and model binding | Diagram identity, provider scheme, model identity | Yes |
| Semantic projection | Model references, element kinds, relevant facts, relationships | Yes |
| Selection intent | Rules used to decide what belongs in the view | Yes |
| Presentation | Theme, frames, grouping, positions, rendering hints | No |
| Annotations | Explanatory content not asserted as a model fact | No, unless explicitly marked semantic |

Changing a color, font, frame position, or routing hint must not by itself mark the represented model semantics stale.

## 6. Domain-neutral model-provider contract

RaiDiagram shall expose generic public contracts equivalent in responsibility to the following. Exact C# names and shapes may be refined during implementation, but the domain boundary shall remain unchanged.

```csharp
public interface IDiagramModelProvider
{
    string Scheme { get; }

    ValueTask<ModelRevision> GetRevisionAsync(
        DiagramModelIdentity model,
        CancellationToken cancellationToken = default);

    IAsyncEnumerable<ModelElementSnapshot> ResolveAsync(
        DiagramModelIdentity model,
        IEnumerable<ModelElementReference> references,
        CancellationToken cancellationToken = default);

    IAsyncEnumerable<ModelElementSnapshot> QueryAsync(
        DiagramModelIdentity model,
        DiagramSelectionRule selectionRule,
        CancellationToken cancellationToken = default);
}
```

The provider is read-only. RaiDiagram shall not require or expose mutation methods for an application's domain model.

`ModelElementReference` should contain a provider-neutral scheme, stable identity, optional kind, and optional revision/version hint. It must not assume JsonPit paths or WWWA identifiers.

`ModelElementSnapshot` should contain:

- the stable `ModelElementReference`;
- a generic element kind;
- a display name;
- the subset of facts relevant to the requesting diagram;
- relationship references where requested;
- a deterministic semantic hash; and
- an optional source revision.

Values used for relevant facts shall be deliberately constrained to a small, serializable value model rather than arbitrary CLR objects.

Multiple providers may be registered through dependency injection and selected by `Scheme`. A consumer without a provider can still load, edit, inspect, and render a `.raid` file from its captured projection; only live reconciliation is unavailable.

## 7. Reconciliation and stale-diagram detection

RaiDiagram shall support two distinct reconciliation modes.

### 7.1 Reference reconciliation

Resolve every explicitly referenced model element and compare the current relevant facts with the captured projection. This detects at least:

- missing source elements;
- renamed or retyped elements;
- changed relevant facts;
- changed or removed relationships; and
- references that now resolve ambiguously or cannot be accessed.

### 7.2 Projection reconciliation

Reapply the manifest's selection rules through the provider. This additionally detects:

- newly created elements that should now appear;
- elements that no longer satisfy the view criteria; and
- relationships that are now in scope but absent from the captured projection.

Not every diagram needs selection rules. A hand-curated diagram may use reference reconciliation only.

### 7.3 Diff result

`DiagramModelDiff` shall be structured data, not only prose. It should report:

- the captured and current model revisions;
- the reconciliation mode used;
- added, removed, changed, newly in-scope, and no-longer-in-scope elements;
- relationship changes;
- unresolved or inaccessible references;
- whether presentation-only changes were ignored; and
- an overall state such as `Current`, `Stale`, `ProviderUnavailable`, `ModelUnavailable`, or `Indeterminate`.

The package shall also provide a deterministic, concise agent-text projection of the diff. This text is an aid to Yebo or another agent; stable references and structured comparison remain the integrity mechanism.

## 8. Diagram semantics

RaiDiagram is domain-neutral, but it is not limited to pixels. It should expose a renderer-independent diagram graph with stable element and connector identities.

The design shall be **role-first**. A Use Case diagram element is a `Role`, not an `Actor`. A role may be filled by a person/agent, system, class, service, or other model element. The corresponding relationship is a `RoleUseCaseConnector`. PlantUML may render a role using actor notation, but the RaiDiagram semantic type remains `Role`.

The package design should accommodate these diagram kinds:

- Mixed Diagram
- Use Case Diagram
- Class Diagram
- Object Diagram
- Activity-Object Diagram
- Activity Diagram
- Sequence Diagram

And these semantic concepts:

- roles and role fillings;
- use cases;
- classes, objects, activities, states, and interactions;
- typed edges/connectors, including role–use-case and class–class connectors;
- frames such as packages, namespaces, boxes, or other named containers;
- swimlanes; and
- nested diagram elements.

For v4.2.0, the implementation may deliver these through an extensible core plus a documented initial set rather than claim complete UML coverage. Unsupported constructs must round-trip or fail explicitly; they must not be silently discarded.

## 9. Presentation, themes, and rendering

PlantUML is the primary v4.2.0 compiler and renderer. RaiDiagram shall:

- compile the semantic graph and presentation intent into deterministic `.puml` text;
- support modern PlantUML theme, styling, font, handwritten, and hand-drawn options without embedding them in the domain model;
- allow an application or tenant to select its own theme set through explicit RaiDiagram configuration;
- use OsLib/RaiPath abstractions for local files and temporary artifacts;
- use RaiUtils `ToolNotFoundException` when the configured PlantUML tool cannot be found;
- return or persist supported render products through RaiImage abstractions; and
- treat `.puml`, `.svg`, `.png`, and other render products as reproducible derivatives of `.raid`.

Remote includes, remote themes, and implicit network access shall be disabled by default. Local includes and themes shall be constrained to configured roots. No rendering operation may mutate `Os.Config`.

## 10. SVG provenance metadata

Every SVG produced through the PlantUML renderer shall point back to its authoritative manifest without exposing a machine-specific absolute file path.

At minimum, the rendered SVG root or a dedicated `<metadata>` element shall contain:

```text
data-raid-id
data-raid-semantic-hash
data-raid-schema-version
```

An optional provider-neutral manifest URI and captured model revision may also be embedded when the caller allows it. Absolute local paths, credentials, private model facts, tenant secrets, and unredacted provider diagnostics shall not be embedded.

The semantic hash shall be computed from a documented canonical representation of the manifest's semantic categories. Presentation-only edits shall not change it. RaiDiagram shall insert or verify this metadata after PlantUML rendering so correctness does not depend on PlantUML preserving an incidental comment.

## 11. Exceptions and diagnostics

RaiDiagram-specific public exceptions shall inherit from `RaiException`. Expected failures should have typed diagnostics, including at least:

- invalid or unsupported `.raid` schema;
- unresolved diagram model provider;
- model or element reconciliation failure;
- unsupported diagram construct;
- rendering failure; and
- malformed or mismatched SVG provenance metadata.

Missing external executables shall use `ToolNotFoundException`. Missing paths shall use OsLib's `RaiPathNotFoundException` where the failure is specifically a path failure.

## 12. Public-safety requirements

RaiDiagram is intended for public NuGet distribution. Therefore:

- the package and its tests shall contain no AIA, AfricaStage, customer, or tenant secrets;
- examples may use fictional data or generic provider schemes;
- snapshots shall include only facts relevant to the diagram, not wholesale model serialization;
- provider errors exposed to files or SVG metadata shall be sanitized;
- default rendering shall perform no network access; and
- the dependency graph shall be auditable and shall not acquire an application-model dependency.

## 13. Verification

The RaiDiagram test project shall cover at least:

1. JSON5 `.raid` parsing, deterministic structural save, and canonical semantic hashing, including comments, trailing commas, single quotes, and unquoted keys;
2. rejection of unsupported schema versions without losing the original file;
3. semantic-hash stability across presentation-only edits;
4. semantic-hash change after a semantic element or relationship change;
5. fake-provider reference reconciliation for current, changed, and missing elements;
6. fake-provider projection reconciliation for newly and no-longer-in-scope elements;
7. provider-unavailable offline loading and rendering;
8. agent-text diff generation that omits purely presentational detail;
9. role-first Use Case compilation, including `RoleUseCaseConnector`;
10. frames, swimlanes, typed connectors, and theme compilation for the supported v4.2 subset;
11. safe local theme resolution and default refusal of remote includes;
12. `ToolNotFoundException` for a missing PlantUML executable;
13. SVG metadata containing the correct `.raid` identity, schema version, and semantic hash;
14. refusal to embed absolute paths or private model facts in SVG metadata;
15. RaiImage-based handling of rendered SVG and raster output; and
16. an assembly/dependency check proving RaiDiagram has no AIA, WWWA, or JsonPit dependency.

PlantUML integration tests should be separable from pure compiler tests so the semantic/compiler suite remains deterministic when the external renderer is unavailable.

## 14. Acceptance criteria for RAIkeep v4.2.0

CR009 is complete when:

- a public `RaiDiagram` package exists with the agreed dependency boundary;
- `.raid` is recognized as its canonical diagram-manifest extension;
- the JSON5 v1 manifest schema, supported JSON5 value domain, and canonical semantic-hash algorithm are documented;
- generic `IDiagramModelProvider`, `ModelElementSnapshot`, and `DiagramModelDiff` contracts are public and tested;
- an application can register a provider by scheme without RaiDiagram referencing application types;
- a `.raid` manifest can be reconciled by reference and, when rules are present, by projection;
- a `.raid` manifest can compile to PlantUML and render through the configured tool boundary;
- rendered SVG contains verified manifest identity and semantic-hash metadata;
- the supported v4.2 semantic constructs and known limitations are documented;
- package and release documentation cite this CR by filename; and
- all focused and relevant RAIkeep Release test suites pass.

Implementation and testing of the WWWA provider in `AIA.Core` belongs to AIA and is not a prerequisite for demonstrating the public RAIkeep contract; RaiDiagram shall provide a fake/sample provider for contract verification.

## 15. Approved first-slice implementation decisions

The implementation uses these decisions without changing the architectural boundary in section 3:

1. A dedicated conformant JSON5 parser handles `.raid` input. The result is normalized into the existing Newtonsoft/JToken and OsLib `CanonicalJson` pipeline.
2. Programmatic structural saves emit strict indented JSON, which is a valid JSON5 subset. Free-standing comments are authoring aids; durable prose uses structured fields.
3. `ModelElementSnapshot` relevant facts are limited to null, Boolean, finite decimal number, and string. `.raid` v1 rejects `NaN` and infinity.
4. Model references use provider scheme plus stable provider-owned identity; revision and kind are optional hints. Manifest URI is separately provider-neutral.
5. The first compiler slice supports the declared element and connector vocabulary through an extensible string-kind graph, with role-first Use Case behavior tested most deeply. Unknown constructs fail capability validation and are never silently dropped.
6. RaiImage's existing PlantUML execution remains a compatibility adapter for one release. RaiDiagram owns semantic compilation and post-render SVG provenance.
7. Public SVG metadata always includes `.raid` identity, semantic hash, and schema version. Manifest URI and captured model revision are optional and absolute local paths are forbidden.
8. Mermaid is deferred from v4.2.0 until the PlantUML semantic and capability boundary is proven.

## 16. Out of scope

CR009 does not request:

- moving AIA's domain model or Yebo modeling logic into RAIkeep;
- a generic persistence engine for WWWA;
- a RaiDiagram dependency on JsonPit;
- automatic mutation of a model to match a diagram;
- round-trip recovery of model semantics from SVG, PNG, or `.puml` output;
- complete UML-standard conformance;
- Mermaid feature parity with PlantUML; or
- package publication, tagging, or version changes before the design and implementation are separately accepted for release.

## 17. Requester summary

RaiDiagram should make diagramming reusable without becoming the modeling product. AIA remains responsible for knowing what its WWWA model means. RaiDiagram is responsible for a durable view manifest, generic source references, model-diff contracts, expressive diagram semantics, PlantUML compilation, theme-aware rendering, and verifiable provenance in the resulting SVG.

## 18. Subsequent implementation decision

Subscriber-scoped artifact placement, typed ImageTree text artifacts, local
PlantUML style lookup, and `_config.puml` materialization for the v4.2.2 work
are specified by
`CR010_AfricaStage_to_RAIkeep_RaiDiagram_Subscriber_Scoped_Artifacts_and_Styles.md`
and `ADR002_RaiDiagram_Subscriber_Scoped_Artifacts_and_Style_Lookup.md`. This
follow-on decision does not change CR009's domain-neutral package boundary.
