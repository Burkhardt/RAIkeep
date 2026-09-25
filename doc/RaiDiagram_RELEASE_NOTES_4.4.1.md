# RaiDiagram 4.4.1 Release Notes

RaiDiagram 4.4.1 implements the reusable artifact capabilities requested by
accepted
[`CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md).
The coordinated release also carries accepted
[`CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR037.1_AIA_to_RAIkeep_CLI_Global_Flag_and_Verb_Dispatch_Resilience.md).

- `DiagramArtifactManager` treats `.raid` as authoritative, derives current
  PUML/SVG in memory, exports without mutating managed siblings, and refreshes
  only missing or stale derivatives.
- Proven-current refresh is a true no-op; the authoritative manifest is never
  rewritten by refresh.
- Compiler-emitted PUML contains integrity-bound semantic metadata and
  round-trips through `PlantUmlModelImporter` to an equivalent semantic AST.
  Edited or external PUML continues through the ordinary syntax parser.
- `AimSvgProfile.Hydratable` emits typed structure, endpoints, docking ports,
  routing, and declared `aim-expression` values. It never emits dynamic
  `aim-satisfied` state. `Plain` emits visible SVG without `aim-*` metadata.
- All managed writes use the final `RaiFile` pathname; no TempDir-to-cloud move
  or directory swap is introduced.
