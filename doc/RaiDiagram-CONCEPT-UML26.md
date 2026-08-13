# RaiDiagram UML26 Concept

**Status:** Internal RAIkeep product concept — proposed architecture  
**Date:** 2026-08-13  
**Owner:** RAIkeep  
**Proposed package:** `RaiDiagram`  
**Primary renderer:** PlantUML  
**Secondary renderer:** Mermaid (initially capability-limited)

## 1. Purpose

UML26 is the proposed semantic diagram dialect of the RAIkeep `RaiDiagram`
package. It keeps the most useful structural and behavioral vocabulary of UML,
modernizes role and object-process semantics, and separates diagram meaning from
renderer syntax.

The name **UML26** identifies a RAIkeep product dialect designed in 2026. It is
not an assertion of conformance to, or a version number assigned by, the Object
Management Group. Deliberate departures from classical UML are part of the
design and must be documented rather than hidden behind renderer-specific
notation.

The package will let people, application code, and AI agents construct diagrams
from typed elements and connectors, validate them, apply tenant presentation,
and render durable image artifacts through RaiImage.

## 2. Product and Package Decision

Diagramming is substantial enough to be a separate RAIkeep package.

The intended dependency order is:

```text
OsLibCore
RaiUtils
RaiImage
RaiDiagram
JsonPit
ImgSeeder
PitSeeder
```

`RaiDiagram` depends on `RaiImage`, `OsLibCore`, and `RaiUtils`.
`RaiImage` does not depend on `RaiDiagram`.

- RaiUtils owns dependency-light shared contracts such as domain exceptions,
  diagnostics, validation results, hashing, correlation, and async primitives.
- OsLib owns paths, files, command execution, and executable discovery.
- RaiImage owns image files, image-tree placement, and rendered image artifacts.
- RaiDiagram owns diagram semantics, validation, presentation selection, and
  renderer orchestration.

This package decision should be ratified in a separate architecture decision
record before the release chain is expanded.

## 3. Semantic First, Rendering Second

A `Diagram` is an engine-neutral semantic graph. It is not a PlantUML or Mermaid
string builder.

```text
Diagram
├── identity and DiagramKind
├── semantic elements
├── typed connectors
├── frames and partitions
├── presentation reference
└── renderer-independent validation
```

Renderers translate a validated diagram model into their own source language.
PlantUML is the primary and most complete renderer. Mermaid may support a
smaller subset, but it must report unsupported semantics instead of silently
reducing them to generic nodes and arrows.

The authoring API should be convenient and mutable. Rendering should consume an
immutable validated snapshot so no renderer can observe a half-built diagram.

## 4. Role Instead of Actor

UML26 deliberately replaces the classical use-case `Actor` semantic element
with `Role`.

An actor-shaped figure describes presentation. A role describes meaning: a
position in an interaction or process that carries responsibilities and can be
filled by different kinds of entities.

A role may be filled by, among others:

- a person;
- an autonomous or assisted agent;
- a system;
- a class or classifier;
- an object or other concrete instance.

The same role can therefore remain stable while its fillers change between
design, deployment, tenant, execution, or historical context.

Consequences:

- UML26 defines `Role`, not `Actor`, as the use-case participant element.
- UML26 defines `RoleUseCaseConnector`, not `ActorUseCaseConnector`.
- PlantUML may render a role with its `actor` notation when that is the selected
  presentation, but the stored semantic model remains a role.
- A role's display shape never limits the kinds of fillers it can accept.
- Importers may translate a classical UML actor into a UML26 role while
  preserving the original notation as presentation metadata.

## 5. Role Filling

Role filling is explicit domain information, not a label attached to an edge.

```text
Role
  ↑ is filled by
RoleFilling
  ↓ identifies
Person | Agent | System | Class | Object
```

A role filling should be able to carry:

- the role;
- the filler;
- whether the filler is a classifier or an instance;
- cardinality;
- qualifications or constraints;
- provenance;
- optional temporal or scenario scope;
- tenant or namespace scope where relevant.

The authoring API may expose `AddRoleFiller(...)`, while the immutable model
represents the result as a typed role-filling relationship. This avoids making
`RoleFiller` a misleading duplicate of the entity that fills the role.

## 6. Diagram Kinds

The initial UML26 diagram kinds are:

- `Mixed`
- `UseCase`
- `Class`
- `Object`
- `ActivityObject`
- `Activity`
- `Sequence`

### 6.1 Mixed Diagram

A mixed diagram intentionally combines structural, behavioral, role, and
object-process elements. It is a validated diagram kind, not an untyped escape
hatch.

### 6.2 Use Case Diagram

Use-case diagrams center on roles, use cases, systems/frames, role filling,
inclusion, extension, and role-to-use-case participation.

### 6.3 Class Diagram

Class diagrams describe classifiers, attributes, operations, inheritance,
associations, attribute-as-connector relationships, packages, interfaces, and
enumerations.

### 6.4 Object Diagram

Object diagrams describe concrete instances, values, links, role fillings, and
the classifier relationships needed to explain an observed or proposed state.

### 6.5 ActivityObject Diagram

ActivityObject diagrams are the modernized UML26 form of an
Object-Process-Diagram. They give activities/processes and affected or produced
objects equal semantic weight and preserve object-flow, state change, role, and
responsibility information.

They must not be flattened into conventional activity diagrams when that would
lose object-process meaning.

### 6.6 Activity Diagram

Activity diagrams describe activities, decisions, control flow, object flow,
parallelism, events, and responsibility partitions/swimlanes.

### 6.7 Sequence Diagram

Sequence diagrams describe roles/lifelines, messages, activation, ordering,
creation/destruction, and interaction frames.

## 7. Element Model

The initial conceptual hierarchy is:

```text
DiagramElement
├── Role
├── UseCase
├── Class
├── Interface
├── Enumeration
├── Object
├── Activity
├── ObjectNode
├── Lifeline
├── State
├── Event
├── Note
├── Frame
└── Swimlane
```

Likely shared element data includes:

- stable identity;
- display name;
- namespace;
- semantic description;
- stereotypes/tags;
- tenant-neutral semantic metadata;
- optional presentation role, but not raw renderer syntax.

## 8. Typed Connector Model

One unrestricted edge with many nullable properties is insufficient. UML26 uses
a common connector base with typed semantic connectors.

```text
DiagramConnector
├── RoleUseCaseConnector
├── RoleFillingConnector
├── IncludeConnector
├── ExtendConnector
├── AssociationConnector
├── AttributeConnector
├── GeneralizationConnector
├── RealizationConnector
├── DependencyConnector
├── ContainmentConnector
├── ControlFlowConnector
├── ObjectFlowConnector
└── MessageConnector
```

Connector contracts may carry label, role name, direction, navigability,
cardinality, guard, order, synchronous/asynchronous behavior, and other fields
appropriate to that connector type. Invalid source/target combinations should
be rejected during validation.

## 9. Frames, Namespaces, and Swimlanes

`Frame` is a recursive named and namespaced container. Frame kinds may include:

- package;
- system boundary;
- subsystem;
- box/group;
- interaction frame;
- renderer-neutral custom frame.

Frames can contain elements, connectors, and nested frames.

A swimlane is also a container, but it specifically assigns responsibility or
ownership within behavioral diagrams. Frames and swimlanes may share a
containment abstraction without being treated as semantically identical.

## 10. Presentation and Tenant Themes

Presentation is separate from the semantic model.

```text
DiagramModel                 DiagramPresentation
├── elements                ├── theme identity
├── connectors              ├── theme version/content hash
└── containment             ├── layout hints
                             ├── element style roles
                             ├── font requirements
                             └── renderer-specific extensions
```

Theme precedence should be explicit and deterministic:

1. RAIkeep UML26 default;
2. tenant theme;
3. diagram-level theme selection;
4. explicitly permitted local presentation overrides.

Tenant themes may define colors, fonts, handwritten/hand-drawn appearance,
lines, shapes, spacing, and semantic style roles. A tenant theme is identified
by a stable name plus a version or content hash so a render can be reproduced.

PlantUML local themes use its supported `puml-theme-<name>.puml` convention and
approved local theme roots. Theme paths are represented by `RaiPath`; diagram
rendering does not mutate `Os.Config`.

Remote includes and remote themes are disabled by default. An installation may
enable them only through an explicit security policy. Fonts required by a theme
must be validated before rendering so a missing font cannot silently change the
tenant's visual identity.

## 11. Renderer Boundary

The conceptual rendering contract is:

```csharp
public interface IDiagramRenderer
{
	string Name { get; }

	DiagramCapabilityReport Validate(
		DiagramModel diagram,
		DiagramRenderOptions options);

	Task<DiagramRenderResult> RenderAsync(
		DiagramModel diagram,
		DiagramDestination destination,
		DiagramRenderOptions options,
		CancellationToken cancellationToken = default);
}
```

Renderer capabilities are explicit. A renderer must never silently omit or
reinterpret an unsupported UML26 construct.

## 12. PlantUML Renderer

PlantUML is the reference UML26 renderer and should use current PlantUML
capabilities rather than limiting itself to legacy `skinparam` strings.

The renderer should support:

- built-in and approved local themes;
- modern PlantUML style definitions;
- configuration files applied before each diagram;
- syntax checking before rendering;
- preprocessing variables under policy control;
- SVG as the default output;
- PNG and PDF where requested and supported;
- deterministic local include roots;
- explicit metadata inclusion/exclusion policy;
- tool and renderer version reporting;
- structured failures including missing tool, syntax, unsupported semantics,
  missing theme, and missing font.

The current RaiImage PlantUML command and rendering implementation are the
starting point for extraction into RaiDiagram. Compatibility adapters may
remain in RaiImage for one coordinated release if needed.

## 13. Mermaid Renderer

Mermaid is a secondary renderer. Its first implementation may be intentionally
small, but its limitations must be observable through capability validation.

Initial Mermaid support may cover:

- basic class diagrams;
- basic sequence diagrams;
- basic flow/activity diagrams;
- simple grouping and connections.

UML26-specific role filling, rich ActivityObject semantics, and mixed diagrams
must not be degraded without an explicit caller-selected fallback policy.

## 14. RaiImage Artifacts

All rendered diagram outputs are RaiImage artifacts. The authoritative source
and its renders can be stored together in the established image tree.

A render result should identify:

- authoritative semantic model or source artifact;
- generated PlantUML/Mermaid source;
- rendered `ImageTreeFile` artifacts;
- output format;
- renderer name and version;
- theme identity and content hash;
- diagram semantic hash;
- warnings and capability decisions;
- render time and correlation identity.

SVG is the preferred default because it is resolution-independent and suitable
for documentation and web presentation. PNG, PDF, or later formats remain
available through explicit render options. JPEG is generally unsuitable for
line diagrams but may be supported as a derived image conversion when a
consumer explicitly needs it.

## 15. Authoring API Direction

The authoring surface should feel direct to people and AI agents:

```csharp
var draft = Diagram.Create("Enrollment", DiagramKind.UseCase);

var student = draft.AddRole("Student");
var enrollmentSystem = draft.AddClass("EnrollmentSystem");
var enroll = draft.AddUseCase("Enroll in course");

draft.AddRoleFiller(student, enrollmentSystem);
draft.Connect(student, enroll, RoleUseCaseConnector.Association());

DiagramModel model = draft.ValidateAndFreeze();
DiagramRenderResult result = await renderer.RenderAsync(model, destination, options);
```

The API should provide typed `AddRole`, `AddUseCase`, `AddClass`, `AddObject`,
`AddActivity`, `AddRoleFiller`, `AddFrame`, `AddSwimlane`, and connector methods
without turning `Diagram` into an unvalidated bag of objects.

## 16. Validation Principles

Validation occurs at three levels:

1. **Semantic validation** — the UML26 graph is internally meaningful.
2. **Renderer capability validation** — the chosen renderer can faithfully
   express the model and requested presentation.
3. **Operational validation** — required tool, theme, config, fonts, paths, and
   output locations are available.

Validation results should be structured data. Exceptions are reserved for
failed operations or invalid attempts to freeze/render a model, not ordinary
capability discovery.

## 17. Open Decisions

The architecture decision record and implementation design must settle:

- the exact mutable-builder and immutable-model API;
- classifier versus instance representation for role fillers;
- whether role filling is modeled only as a relationship or also has an
  addressable element identity;
- diagram-kind-specific validation rules;
- the ActivityObject/modernized Object-Process semantic vocabulary;
- default UML26 theme and bundled font policy;
- tenant theme discovery and versioning;
- local include sandbox rules;
- whether generated SVG/PNG embeds authoritative source metadata;
- compatibility and extraction of the current RaiImage PlantUML API;
- Mermaid's initial capability boundary;
- insertion of RaiDiagram into the coordinated release chain.

## 18. Acceptance Direction

The first implementable slice should prove the architecture rather than cover
every UML26 construct:

1. create the RaiDiagram package and ADR;
2. implement draft/freeze, Role, UseCase, Frame, RoleFilling, and
   RoleUseCaseConnector;
3. implement tenant-aware PlantUML themes and SVG rendering;
4. return source and SVG as RaiImage artifacts;
5. reject unsupported or invalid semantics with structured diagnostics;
6. preserve current RaiImage PlantUML behavior through an intentional
   compatibility path;
7. add one class-diagram and one ActivityObject vertical slice next;
8. defer the Mermaid renderer until the PlantUML semantic boundary is proven.

This sequence establishes UML26's distinctive role semantics and tenant visual
identity before expanding breadth.
