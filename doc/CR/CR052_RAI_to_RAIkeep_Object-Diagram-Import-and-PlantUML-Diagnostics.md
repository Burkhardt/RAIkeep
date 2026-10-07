# CR052 — Object diagrams and PlantUML diagnostics

Delivery A targets RAIkeep 4.5.5 together with CR054. PlantUML is the active
external authoring/interchange language; `.raid` is authoritative and SVG is a
hydratable rendering. All committed examples and new fixtures use textbook models.

## Delivered contract

- Import `object "Order42 : Order" as order { Number = 42 }`, multiline bodies,
  mixed actors/classes/objects, declared endpoints, and supported relationships.
- Store ordered raw text slots in ObjectProperties; preserve large numbers,
  punctuation and quoted values without guessing CLR types. Render visible
  object compartments with underlined object headers.
- Schema 1.1 adds object slots, directed associations, deployment elements, and
  optional drawing identities/authored waypoints. Readers retain schema 1.0
  support; unchanged manifests do not acquire empty slot fields.
- `_VD` supports host/resident containment and standard deployment declarations:
  node, cloud, component, database, artifact, folder, frame. PlantUML import/export
  and DistributionDiagramBuilder share the same AST.
- Preflight parsing and artifact derivation complete before writing managed or
  flat output. Rejected input does not replace existing artifacts.

## Diagnostics

| Code | Meaning |
| --- | --- |
| PUML001 | Malformed envelope, declaration, delimiters, or control block |
| PUML002 | Unsupported construct or stereotype |
| PUML003 | Empty model or support fragment without a standalone diagram |
| PUML004 | Duplicate alias/slot or unresolved endpoint |
| PUML005 | Include/preprocessor directive requiring supported expansion |
| PUML101 | Presentation hint retained but not applied by the canvas renderer |
| RAID201 | Renderer cannot support the requested construct |

Parser errors carry source filename, line, column and code. The CLI writes them
to stderr and exits nonzero. Unsupported statements cannot become implicit classes.
Layout macros, includes, and additional UML families are not silently approximated.

## Bounded legacy XMI capability

The accepted XmiDeploymentImporter is retained for Poseidon/OTW deployment XMI.
It scans XML forward, retains the selected drawing and referenced semantics,
keeps repeated views distinct, and preserves authored node bounds and waypoints.
`raid import-xmi` / `import-otw` can list/select deployment diagrams. This capability
is frozen: no further visual tuning, dialects, general model engine, or additional
XMI diagram families are in this delivery. No SysML development is included.

## Verification

Active synthetic coverage resides in RaiDiagram.Tests and raid.Tests, including
Cr052AcceptanceTests, StructuralImportTests, XmiDeploymentImportTests, and
ImportPreflightTests. Private corpus paths remain local and their files are never
published. Prior broad legacy-content cleanup is explicitly out of scope.
