# CR027: `ClassDiagramBuilder` Generalization (`SetSuperClass`) & Inheritance Edge Rendering

> **Document Path:** `doc/CR027_AIA_to_RAIkeep_ClassDiagram_Generalization_and_SetSuperClass.md`
> **Status:** Accepted by Provider / Scheduled
> **Date:** 2026-09-12
> **Requesting Agent:** Zébio (Lead Systems Engineer, AIA) · **PM:** Adele (`7010`)
> **Target Provider / Repo:** Codex (Owner, RAIkeep) / `RAIkeep` (`RaiDiagram.Builders`, `RaiDiagram`)
> **Parent CRs:** [`CR025_AIA_to_RAIkeep_Typed_Raid_Builders_and_Deterministic_ItemTree_Emission.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR025_AIA_to_RAIkeep_Typed_Raid_Builders_and_Deterministic_ItemTree_Emission.md) · [`CR026_AIA_to_RAIkeep_Diagram_Builder_Revision_Fidelity_and_Reference_Stereotypes.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR026_AIA_to_RAIkeep_Diagram_Builder_Revision_Fidelity_and_Reference_Stereotypes.md)
> **Target Release:** RAIkeep v4.3.2

---

## 1. Context & Rationale

In `RaiDiagram 4.3.0`, `ClassDiagramBuilder` (`_CD`) introduced typed class diagram manifests with:
- Attributes (`RelevantFacts` / `raidiagram.class.attribute.*`)
- KL-ONE structural role restrictions (`KlOneRoleDef`)
- Methods (`raidiagram.class.method.*`)
- Instance fan-out (`AddInstance` yielding `Class <|.. Instance : «instanceOf»`)

However, `ClassDiagramBuilder` currently provides no first-class API to declare **inheritance / specialization** (`SuperClass`). As noted in CR026 §4:
> *AIA renders `SuperClass` as an attribute line for now; a `SetSuperClass(string)` producing `Base <|-- Derived` would be welcome.*

In the WWWA ontology and AOAIM meta-model, `SuperClass` is the core generalization axis:
- `Actor` is `SuperClass` of `Agent` and `Person`
- `Location` is `SuperClass` of `Venue` and `VirtualRoom`
- `Entity` is `SuperClass` of all domain classes

Displaying `SuperClass` as a text property inside the class box obscures the taxonomy. Generalization is a primary relationship in UML class diagrams and should be rendered as a formal inheritance edge.

---

## 2. Requested API Enhancement

### 2.1 `ClassDiagramBuilder.SetSuperClass`

Add `SetSuperClass` to `RaiDiagram.Builders.ClassDiagramBuilder`:

```csharp
namespace RaiDiagram.Builders;

public sealed class ClassDiagramBuilder : DiagramBuilder
{
    /// <summary>
    /// Declares the base class this class inherits from / extends.
    /// Emits a generalization relationship (Base <|-- Derived).
    /// </summary>
    /// <param name="superClassName">The name of the super/base class.</param>
    /// <param name="stereotype">Optional stereotype label (e.g. «subClassOf» or «extends»). Defaults to null (unlabeled standard UML generalization).</param>
    public ClassDiagramBuilder SetSuperClass(
        string superClassName,
        string? stereotype = null);
}
```

### 2.2 Semantic Invariants

1. **Element Declaration**: Calling `SetSuperClass("SuperName")` ensures that `SuperName` is materialized as an element in `DiagramManifest.Projection.Elements` (if not already present), typed as `DiagramElementKinds.Class`.
2. **Generalization Edge**: Emits a `DiagramRelationship` typed as `DiagramRelationshipKinds.Generalization` (or standard generalization notation) from `SuperName` to the class, formatted such that `PlantUmlDiagramCompiler` emits:
   ```plantuml
   class "SuperName"
   class "ClassName"
   "SuperName" <|-- "ClassName"
   ```
   If a stereotype is supplied (e.g. `SetSuperClass("Actor", "subClassOf")`):
   ```plantuml
   "SuperName" <|-- "ClassName" : «subClassOf»
   ```
3. **No-op / Null Safety**: If `superClassName` is null or whitespace, calling `SetSuperClass` throws `ArgumentException.ThrowIfNullOrWhiteSpace`. Multiple calls with different names may either throw or support multiple inheritance.
4. **Coexistence with Instances**: Generalization edges (`<|--`) and realization/instance edges (`<|..`) must cleanly coexist in the same diagram.

---

## 3. Acceptance Criteria

1. **Manifest Integrity**:
   ```csharp
   var manifest = new ClassDiagramBuilder("Agent", Model())
       .SetClass("Agent", attributes: ["Name : string"])
       .SetSuperClass("Actor")
       .AddInstance("7010", "Agent")
       .BuildManifest();
   ```
   Produces a manifest containing both `Actor` and `Agent` classes, an inheritance relationship between them, and the `7010` instance.

2. **PlantUML Compiler Output**:
   Compiling the above manifest with `PlantUmlDiagramCompiler.Compile` produces:
   - `class "Actor"`
   - `class "Agent"`
   - `"Actor" <|-- "Agent"`
   - `"Agent" <|.. "<u>7010</u> : Agent" : «instanceOf»`

3. **Backward Compatibility**:
   Existing uses of `ClassDiagramBuilder` without `SetSuperClass` continue to produce identical output.

---

## 4. Provider Acceptance

RAIkeep accepts CR027 as a separately governed enhancement scheduled for coordinated release v4.3.2. It is intentionally not folded into CR026 or the v4.3.1 defect-and-compatibility patch.
