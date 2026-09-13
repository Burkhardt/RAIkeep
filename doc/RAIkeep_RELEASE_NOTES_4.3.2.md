# RAIkeep 4.3.2 Release Notes

RAIkeep 4.3.2 is the coordinated seven-package delivery of accepted
[CR027 Class-Diagram Generalization and `SetSuperClass`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR027_AIA_to_RAIkeep_ClassDiagram_Generalization_and_SetSuperClass.md).

## RaiDiagram class generalization

- `ClassDiagramBuilder.SetSuperClass(...)` adds a typed superclass to a class
  diagram and a typed generalization relationship to the derived class.
- `PlantUmlDiagramCompiler` renders that semantic direction as UML `<|--`.
- An optional stereotype labels the generalization; omission produces the
  standard unlabeled UML relationship.
- Generalization and existing instance-of edges can be rendered together.
- The singular builder API rejects a second superclass definition explicitly.
- Existing class builders without a superclass preserve their prior output.

OsLibCore, RaiUtils, RaiImage, JsonPit, ImgSeeder, and PitSeeder have no
behavioral changes in this patch; they participate so all seven package and
fallback dependency versions remain aligned on 4.3.2.

Tagging, GitHub labeling, workflow dispatch, and NuGet publication remain behind
RAI's manual `scripts/release-chain.sh 4.3.2` gate.
