# RaiDiagram 4.3.2 Release Notes

RaiDiagram 4.3.2 implements accepted
[CR027 Class-Diagram Generalization and `SetSuperClass`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR027_AIA_to_RAIkeep_ClassDiagram_Generalization_and_SetSuperClass.md).

- `ClassDiagramBuilder.SetSuperClass(superClassName, stereotype)` materializes
  the superclass as a typed `Class` element and emits a typed
  `GeneralizationConnector` to the derived class.
- The compiler renders the accepted superclass-to-derived-class convention as
  UML `<|--`, with no label by default.
- An optional stereotype such as `subClassOf` renders as `«subClassOf»` on the
  generalization edge.
- Generalization and the existing `<|.. : «instanceOf»` relationship coexist in
  the same generated class diagram.
- Null or whitespace superclass names, calling before `SetClass(...)`, and a
  second superclass definition fail explicitly.
- Builders that do not call `SetSuperClass(...)` retain their existing output.
- Regression coverage validates manifest direction, optional labeling, failure
  cases, and rendering through the real PlantUML 1.2026.8 CLI.

Publication remains behind RAI's manual release-chain gate.
