# RaiDiagram 4.3.0 Release Notes

RaiDiagram 4.3.0 delivers accepted
[CR023 relationship rendering](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR023_AIA_to_RAIkeep_PlantUml_Relationship_Rendering.md) and
[CR025 typed builders and deterministic ItemTree emission](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR025_AIA_to_RAIkeep_Typed_Raid_Builders_and_Deterministic_ItemTree_Emission.md).

- `RaiDiagram.Builders` adds typed UCD, RFD/OD, CD, AD, and SD builders plus
  `KlOneRoleDef`.
- The managed compiler emits native use-case, object, class, activity, and
  sequence PlantUML and conditionally injects `allowmixing`.
- `ItemId`, optional `ItemNumber`, and archetype `NameExt` remain separate;
  `.raid`, `.puml`, `_config.puml`, and `.svg` siblings share one ItemTree bucket.
- `PlantUmlSvgDiagnostics` rejects diagnostic SVG output.
- `IDiagramRenderer` remains an optional 4.x server compatibility API.
- CI syntax coverage uses the real PlantUML 1.2026.8 CLI; AIA owns TeaVM tests.

The unpublished 4.2.11 preparation is superseded. Publication remains behind
RAI's manual `scripts/release-chain.sh 4.3.0` gate.
