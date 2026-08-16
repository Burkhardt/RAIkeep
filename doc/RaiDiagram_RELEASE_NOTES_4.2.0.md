# RaiDiagram 4.2.0 Release Notes

**Status:** Prepared source and verification candidate; not published
**Change request:** `CR009_AIA_to_RAIkeep_RaiDiagram_Package.md`

RaiDiagram introduces domain-neutral, agent-readable diagrams to RAIkeep.

## Highlights

- `.raid` is the canonical Rai Agentic Interactive Diagram extension.
- Version 1 manifests use JSON5 and normalize to strict canonical JSON for
  deterministic semantic hashing.
- Public `IDiagramModelProvider`, `ModelElementSnapshot`, provider registry, and
  `DiagramModelDiff` contracts let applications expose a read-only model through
  dependency injection without leaking domain types.
- Reference and projection reconciliation detect changed, missing, ambiguous,
  newly in-scope, and no-longer-in-scope model elements.
- The initial UML26 graph is role-first and supports roles, use cases, classes,
  objects, activities, frames, swimlanes, and typed connectors.
- PlantUML compilation supports built-in or explicitly approved local themes,
  fonts, and handwritten rendering without remote includes.
- Rendering uses RaiImage artifacts and embeds verified `.raid` identity, schema,
  and semantic hash metadata in SVG.
- RaiDiagram has no AIA, WWWA, or JsonPit dependency. AIA owns the provider
  implementation in `AIA.Core`.

Mermaid and full UML conformance are not claimed by this initial slice.

The public RaiDiagram repository and its tag-triggered NuGet workflow now exist
at <https://github.com/Burkhardt/RaiDiagram>. No version tag or NuGet package has
been published by this implementation candidate.

Release verification: 20 RaiDiagram Release tests passed.
