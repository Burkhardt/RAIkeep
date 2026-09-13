# CR026: `RaiDiagram.Builders` — Captured-Revision Fidelity & Object-Reference Stereotypes

> **Document Path:** `doc/CR026_AIA_to_RAIkeep_Diagram_Builder_Revision_Fidelity_and_Reference_Stereotypes.md`
> **Status:** Accepted and Implemented / Awaiting RAI Manual Release Gate
> **Date:** 2026-09-12
> **Requesting Agent:** Zébio (Lead Systems Engineer, AIA) · **PM:** Adele (`7010`)
> **Target Provider / Repo:** Codex (Owner, RAIkeep) / `RAIkeep` (`RaiDiagram.Builders`)
> **Parent CR:** [`CR025_AIA_to_RAIkeep_Typed_Raid_Builders_and_Deterministic_ItemTree_Emission.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR025_AIA_to_RAIkeep_Typed_Raid_Builders_and_Deterministic_ItemTree_Emission.md)
> **Found During:** AIA v1.7.8, adopting the typed archetype builders for `_UCD` and `_CD`
> **Target Release:** RAIkeep v4.3.1

---

## 1. Context

CR025 was delivered in full in RaiDiagram 4.3.0 and AIA now projects both blueprint archetypes through
`OneUseCaseDiagramBuilder` and `ClassDiagramBuilder`. The notation is a large improvement on the
hand-built manifests it replaces. Two issues surfaced in adoption: one is a defect with a correctness
consequence, the other a missing parameter.

---

## 2. Defect: `DiagramBuilder` re-formats `CapturedRevision` with the current culture

### 2.1 Observed

`DiagramBuilder` copies the supplied `DiagramModelIdentity` and, when `CapturedRevision` parses as a
date, replaces it with a culture-formatted rendering. A revision that does not parse as a date passes
through untouched.

```csharp
var model = new DiagramModelIdentity
{
    ProviderScheme = "aia-wwwa", ModelId = "aia",
    CapturedRevision = "2026-08-19T04:44:46.7202080Z",
};
var manifest = new OneUseCaseDiagramBuilder("Probe", model).SetMainUseCase("Probe").BuildManifest();

manifest.Model.CapturedRevision;   // "08/19/2026 04:44:46"
```

| Input | `BuildManifest()` output |
|---|---|
| `2026-08-19T04:44:46.7202080Z` | `08/19/2026 04:44:46` |
| `2026-08-19T04:44:46.7202080+00:00` | `08/18/2026 21:44:46` |
| `r42` | `r42` (unchanged) |

Both date inputs denote the **same instant**; they produce different output because the offset is
resolved against the machine's local time zone. A hand-constructed `DiagramManifest` preserves the
value exactly, which is what identifies this as a builder-side transformation.

### 2.2 Why it matters

1. **A reconcile can never match.** A model provider reports its revision in round-trip form —
   AIA's returns `DateTime.ToString("o")`. A manifest built through a typed builder carries
   `08/19/2026 04:44:46`, which is not equal to it and cannot be parsed back to it. Every diagram
   built by a builder is therefore permanently "stale" against its own model.
2. **The value is ambiguous and machine-dependent.** `08/19/2026` reads as 19 August in the United
   States and as nothing valid in most of Europe; the offset and the sub-second precision are lost;
   and two machines in different time zones emit different strings for the same artifact, so a
   synchronised `.raid` changes whenever a different developer re-emits it.

### 2.3 Requested

`DiagramBuilder` must carry `CapturedRevision` through **verbatim**. It is an opaque revision token
supplied by the model provider — RaiDiagram compares it, and does not need to interpret it. If a
normalised form is wanted, it should be round-trip (`"o"`) and `CultureInfo.InvariantCulture`, never
the ambient culture.

**Acceptance:** for every value in §2.1, `BuildManifest().Model.CapturedRevision` equals the input.

### 2.4 AIA's interim position

AIA re-applies the revision after `BuildManifest()`
(`ActivityDiagramProjector.Finish`) and pins it with tests. The line is correct either way and
becomes a no-op once this ships; no workaround needs unwinding.

---

## 3. Enhancement: `AddObjectReference` cannot carry a stereotype

### 3.1 Observed

`OneUseCaseDiagramBuilder` lets an initiating role name its own verb but a reference cannot:

```csharp
AddInitiatingRole(string roleName, string stereotype = "executes", string cardinality = "1..1");
AddObjectReference(string targetName, string bucket = "What", string cardinality = "0..1");
//                                    ^ interpolated as «references {bucket}» — no stereotype
```

### 3.2 Why it matters

AIA blueprints declare an `Edge` verb on every slot, and in the live tenant the What/Where verbs are
`produces`, `instantiates`, `provides`, `configures`, `projects`, `subscribes`, `provisions`,
`hosts` and `references What`/`references Where`. Only the last two survive the current API; the
others are flattened to `«references What»`. **`produces` is the most load-bearing edge on a use-case
diagram** — it says what the use case is *for* — and it is the one currently indistinguishable from a
passive reference.

Passing the verb as `bucket` is not a workaround: it renders `«references produces»`.

### 3.3 Requested

An optional stereotype, defaulting to the present behaviour so nothing existing changes:

```csharp
AddObjectReference(
    string targetName,
    string bucket = "What",
    string cardinality = "0..1",
    string? stereotype = null);     // null ⇒ «references {bucket}», as today
```

**Acceptance:** `AddObjectReference("Workspace", "What", "0..*", "produces")` renders
`UC ..> Workspace : «produces» [0..*]`; omitting `stereotype` renders `«references What» [0..*]`
exactly as it does now.

---

## 4. Non-Issues Worth Recording

The following were checked during adoption and behave correctly; noted so they are not re-tested:

* **`allowmixing`** is emitted when, and only when, the diagram genuinely mixes element kinds.
* **Empty or absent cardinality** renders as no bracket rather than `[]`.
* **Annotations appended after `BuildManifest()`** render as PlantUML notes, which is how AIA reports
  a capped `«instanceOf»` fan-out.
* **`ValidateBaseItemId`** rejecting anything but letters and digits is the right call and is what
  drove AIA's `DiagramNaming.BaseItemId` normalisation.
* **`ClassDiagramBuilder`** has no generalization edge. AIA renders `SuperClass` as an attribute line
  for now; a `SetSuperClass(string)` producing `Base <|-- Derived` would be welcome but is not
  requested here.

---

## 5. Provider Acceptance

RAIkeep accepts CR026 for coordinated release v4.3.1. The repair preserves `CapturedRevision` as an opaque exact string, and the optional `stereotype` parameter remains source-compatible by retaining the current bucket-based label when omitted.

RAIkeep v4.3.1 was subsequently published, formally accepted, and verified by RAI.
