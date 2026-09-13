# RaiDiagram 4.3.1 Release Notes

RaiDiagram 4.3.1 implements accepted
[CR026 Captured-Revision Fidelity and Object-Reference Stereotypes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR026_AIA_to_RAIkeep_Diagram_Builder_Revision_Fidelity_and_Reference_Stereotypes.md).

- `CapturedRevision` remains an opaque, verbatim string through typed builder
  snapshots, `DiagramModel.FromManifest(...)`, JSON5 serialization, and `.raid`
  parsing. ISO-looking tokens are never converted through local culture or time
  zone.
- `OneUseCaseDiagramBuilder.AddObjectReference(...)` adds the optional
  `stereotype` argument. An explicit value such as `produces` renders
  `«produces»`; `null` preserves the existing `«references {bucket}»` output.
- The complete existing agent-friendly JSON5 profile remains supported,
  including comments, unquoted names, single-quoted and continued strings,
  trailing commas, and JSON5 numeric forms.
- Duplicate properties and non-finite numbers remain rejected.
- Regression coverage exercises exact UTC/offset tokens, arbitrary revision
  tokens, default compatibility, explicit stereotypes, and real PlantUML
  1.2026.8 compilation.

Accepted CR027 `SetSuperClass` generalization is separately scheduled for
RAIkeep v4.3.2 and is not included in this patch. Publication remains behind
RAI's manual release-chain gate.
