# ADR001 — RaiDiagram Package Boundary

**Status:** Accepted  
**Date:** 2026-08-13  
**Decision owners:** RAIkeep and AIA  
**Related request:** `CR009_AIA_to_RAIkeep_RaiDiagram_Package.md`

## Context

AIA agents create and maintain WWWA domain models and use PlantUML diagrams to
communicate selected views of those models. Diagram construction, theming,
rendering, provenance, and consistency checking are reusable capabilities, but
the meaning and storage of WWWA remain AIA responsibilities.

Putting diagram presentation in the domain model would clutter domain facts and
prevent one element from participating in multiple views. Treating `.puml` as
the authoritative representation would mix renderer syntax with model references
and make deterministic reconciliation unnecessarily fragile.

## Decision

RAIkeep will provide a separate public package named `RaiDiagram`.

1. `.raid` (Rai Agentic Interactive Diagram) is the authoritative manifest
   extension. Version 1 is UTF-8 JSON5.
2. A `.raid` manifest contains a captured semantic projection, generic model
   references, optional selection rules, annotations, and presentation intent.
3. Semantic identity is the SHA-256 of strict canonical JSON derived from the
   semantic categories. Comments, formatting, presentation frames, themes,
   layout hints, and captured revision are excluded.
4. `IDiagramModelProvider` is read-only and domain-neutral. `AIA.Core` implements
   the WWWA provider; RaiDiagram does not depend on AIA or JsonPit.
5. RaiDiagram supports reference reconciliation and optional projection
   reconciliation, returning structured `DiagramModelDiff` data plus a
   deterministic agent-text view.
6. Diagram semantics are role-first: `Role` and `RoleUseCaseConnector` replace
   Actor as the stored use-case concept. Renderers may still choose actor-shaped
   notation.
7. PlantUML is the primary renderer. Mermaid is deferred until the semantic and
   capability boundaries have proven stable.
8. PlantUML SVG output receives verified `data-raid-id`,
   `data-raid-semantic-hash`, and `data-raid-schema-version` metadata after
   rendering.
9. RaiDiagram depends on RaiUtils, OsLibCore, and RaiImage. It does not introduce
   reverse dependencies into those packages.
10. The existing RaiImage PlantUML API remains the compatibility/tool boundary
    for the first RaiDiagram release. Extraction can occur in a coordinated
    later release without breaking current RaiImage consumers.

## JSON5 decision

RaiDiagram uses a conformant JSON5 parser at its input boundary, then converts
the parsed value graph into RAIkeep's existing Newtonsoft/JToken and
`CanonicalJson` pipeline. Strict JSON is a valid input subset and is the default
structural save format.

Free-standing comments are authoring aids and are not guaranteed to retain their
lexical position after a structural rewrite. Durable prose belongs in structured
`purpose`, `description`, or `annotations` fields. Non-finite JSON5 numbers are
rejected in schema v1 because strict canonical JSON cannot represent them.

## Consequences

- AIA can expose WWWA through dependency injection without publishing WWWA
  contracts or persistence details.
- A diagram remains renderable offline from its captured projection.
- An agent can receive a small semantic diff rather than renderer-heavy `.puml`.
- Presentation-only edits do not create false model-staleness signals.
- Rendered SVG can be traced to the authoritative `.raid` identity and content.
- A new package/repository slot is needed in the coordinated release chain after
  RaiImage. The source is staged in the umbrella workspace until that external
  repository and publication workflow are explicitly provisioned.
- A true JSON5 parser becomes a direct implementation dependency; Newtonsoft
  remains the canonical value/hash representation already used by RAIkeep.

## Rejected alternatives

- **Place diagramming in AIA:** rejected because generic diagram semantics,
  rendering, and provenance are reusable public-safe capabilities.
- **Place diagramming in RaiImage:** rejected because semantic graphs and model
  reconciliation are broader than image handling.
- **Make `.puml` authoritative:** rejected because it mixes semantics and
  presentation and lacks provider-neutral model references.
- **Make RaiDiagram a modeling engine:** rejected because WWWA meaning and model
  evolution belong to AIA.
- **Use Actor as the semantic participant:** rejected in favor of the more
  general Role/RoleFilling model.
