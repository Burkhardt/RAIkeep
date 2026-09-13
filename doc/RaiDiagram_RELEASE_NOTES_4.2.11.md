# RaiDiagram 4.2.11 Release Notes

> **Superseded before publication.** This prepared package line was not released;
> its changes are carried into v4.3.0.

RaiDiagram 4.2.11 implements accepted
[CR023](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR023_AIA_to_RAIkeep_PlantUml_Relationship_Rendering.md).

- `PlantUmlDiagramCompiler.Compile(...)` renders the typed relationship kinds
  and the established concise PlantUML-facing spellings, including AIA's `Role`
  relationship.
- Relationship labels and optional cardinality survive into deterministic
  PlantUML and rendered SVG output.
- Mixed, Activity, ActivityObject, and Sequence manifests emit PlantUML's
  `allowmixing` directive so truthful Activity/Object declarations can be
  connected without flattening their types.
- `AcceptedElementKinds` and `AcceptedRelationshipKinds` publish the compiler's
  exact case-sensitive vocabulary.
- Unsupported constructs remain fail-closed and visible through `Validate(...)`;
  they are not silently removed from a supposedly complete diagram.

Regression coverage includes source compilation and a real, complete PlantUML
CLI render of an Activity Interaction relationship with its role and
cardinality.
