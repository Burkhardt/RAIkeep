# CR023 — PlantUML Relationship Rendering in RaiDiagram

**Requesting product:** AIA

**Requesting agent:** Zébio (AIA Dev Agent)

**Provider:** RAIkeep

**Provider owner:** Codex (Owner and Lead Custodian, RAIkeep)

**Accepted by:** RAI and Adele (PM, AIA)

**Target release:** Coordinated RAIkeep v4.2.11

**Status:** Accepted and implemented; awaiting RAI's manual release-chain gate

## 1. Problem

AIA Activity Interaction diagrams carry their model relationships in the
authoritative `.raid` manifest. AIA's provider expresses the Activity-to-filler
edge with the concise relationship kind `Role`, its WWWA role as the label, and
an optional cardinality. RaiDiagram 4.2.10 rejected that relationship kind, so
AIA could only compile a deliberately incomplete elements-only fallback and
withheld the misleading edgeless SVG.

The typed `...Connector` relationship vocabulary already had PlantUML mappings,
but neither concise compatibility kinds nor direct relationship rendering were
covered by a real Activity Interaction regression test.

## 2. Accepted capability

1. `PlantUmlDiagramCompiler.Compile(...)` renders typed relationships and the
   established concise PlantUML-facing spellings, including AIA's `Role` edge.
2. A relationship preserves its optional label and cardinality in the generated
   PlantUML. Cardinality is emitted as visible relationship-label metadata so it
   remains valid in mixed PlantUML diagrams.
3. Mixed, Activity, ActivityObject, and Sequence manifests opt into PlantUML's
   `allowmixing` directive. Element declarations retain their truthful RaiDiagram
   kinds while Activity/Object combinations remain renderable by the real CLI.
4. `PlantUmlDiagramCompiler.AcceptedElementKinds` and
   `AcceptedRelationshipKinds` publish the compiler's exact case-sensitive
   vocabulary. Existing `DiagramElementKinds` and `DiagramRelationshipKinds`
   constants remain source- and manifest-compatible.
5. Unknown constructs remain explicit failures. The provider considered CR023's
   optional partial-render suggestion and retains fail-closed behavior because a
   silently incomplete diagram can misstate the model; callers can use
   `Validate(...)` to obtain `DiagramCapabilityReport` before compilation.

## 3. Verification

- A source-level regression proves an Activity-to-participant `Role` edge emits
  its direction, role label, and cardinality.
- Public-vocabulary coverage proves typed and concise relationship kinds are
  discoverable without exception probing.
- A real, unpruned PlantUML CLI renders the Activity/Object relationship to SVG,
  and the SVG contains both endpoints, the role label, and cardinality.
- Existing checked-in `.raid` / `.puml` / SVG provenance tests remain unchanged.

## 4. Release boundary

CR023 is part of the coordinated seven-package RAIkeep v4.2.11 line. Tagging,
GitHub labeling, workflow dispatch, and NuGet publication remain exclusively
behind RAI's manual `scripts/release-chain.sh 4.2.11` gate.
