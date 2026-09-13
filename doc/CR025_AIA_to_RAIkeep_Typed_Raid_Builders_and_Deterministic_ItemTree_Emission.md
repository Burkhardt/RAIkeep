# CR025 — RaiDiagram Typed Builders and Deterministic ItemTree Emission

**Requesting product:** AIA

**Requesters:** Adele (PM, AIA) and RAI

**Provider:** RAIkeep

**Provider owner:** Codex (Owner and Lead Custodian, RAIkeep)

**Accepted by:** RAI and Adele (PM, AIA)

**Target release:** Coordinated RAIkeep v4.3.0

**Status:** Accepted and implemented; awaiting RAI's manual release-chain gate

## 1. Objective

RaiDiagram supplies pure managed-C# semantic builders and deterministic
`DiagramManifest`-to-PlantUML compilation. AIA owns browser-side WASM/TeaVM
rendering. The established `IDiagramRenderer` and `PlantUmlDiagramRenderer`
remain optional 4.x compatibility APIs for servers with PlantUML installed.

## 2. Accepted typed builders

The public `RaiDiagram.Builders` namespace provides:

- `OneUseCaseDiagramBuilder` (`UCD`) with role-first initiating and defined
  roles, object references, dependencies, frames, and narrative notes;
- `RoleFillerDiagramBuilder` (`RFD` or `OD`) with instance attributes and Who,
  What, and Where fillers;
- `ClassDiagramBuilder` (`CD`) and public `KlOneRoleDef` structural roles;
- `ActivityDiagramBuilder` (`AD`) with swimlanes, steps, transitions,
  decisions, initial steps, and terminal steps;
- `SequenceDiagramBuilder` (`SD`) with participants, synchronous/asynchronous
  messages, returns, self-messages, dividers, and notes.

Each builder produces a validated `DiagramManifest`; consumers do not construct
untyped dictionary trees or concatenate PlantUML themselves.

## 3. Corrected ItemTree identity contract

The provider acceptance incorporates RAI's correction to the requester wording:

- `ItemId` is the base domain identity, for example `SignContract`.
- `NameExt` is the archetype without a leading underscore, for example `UCD`.
- `ItemNumber` is optional and precedes `NameExt` when present.
- A filename is composed by the existing RaiImage convention as
  `ItemId[_NN][_NameExt].ext`.
- `ItemTreePath` cumulative buckets are calculated **only from the base
  `ItemId`**, never from `ItemNumber`, `NameExt`, or the composed filename.

Therefore the siblings for base ItemId `SignContract`, no item number, and
NameExt `UCD` are:

```text
<imagesRoot>/AfricaStage/SignCont/SignContra/SignContract_UCD.raid
<imagesRoot>/AfricaStage/SignCont/SignContra/SignContract_UCD.puml
<imagesRoot>/AfricaStage/SignCont/SignContra/SignContract_UCD.svg
```

With item number 2 they become `SignContract_02_UCD.*` in the same bucket.
`ItemTreeTextFile.ItemNumber` is symmetric with
`ImageTreeFile.ImageNumber`. No arbitrary `/Activity/` or `/UseCase/`
directory is introduced.

## 4. Compiler and renderer boundary

1. `PlantUmlDiagramCompiler` is pure managed C# and performs no external
   process invocation.
2. It emits native PlantUML for the five builder families and injects
   `allowmixing` immediately after `@startuml` when the declaration families
   actually require it.
3. Relationships preserve direction, label, stereotype, and cardinality under
   the accepted CR023 rules.
4. Unknown element or relationship kinds remain explicit validation failures.
5. Optional server-side rendering rejects PlantUML error/warning SVG documents
   through `PlantUmlSvgDiagnostics`.
6. The publishing test environment pins the real PlantUML CLI at 1.2026.8;
   AIA remains responsible for TeaVM/browser execution tests.

## 5. Storage and cloud safety

`DiagramArtifactSet`, `RaidFile`, `PumlSourceFile`, and `PumlConfigFile` carry
base `ItemId`, optional `ItemNumber`, and `NameExt` independently. The `.raid`,
`.puml`, `_config.puml`, and `.svg` artifacts remain co-located siblings in one
subscriber ItemTree bucket. Writes continue through RaiFile/RaiImage boundaries
and must obey CR022: no TempDir-to-cloud moves and no directory replacement.

## 6. Verification and release boundary

- Unit tests cover every typed builder, exact identity composition, numbered
  artifacts, cumulative 8x2 bucketing from base ItemId, and sibling placement.
- A real unpruned PlantUML 1.2026.8 CLI validates all builder-generated PUML
  and rejects diagnostic SVGs.
- Existing CR023 relationship and CR024 lifecycle regressions remain active.

CR025 is part of coordinated RAIkeep v4.3.0. Tagging, GitHub labeling,
workflow dispatch, and NuGet publication remain exclusively behind RAI's
manual `scripts/release-chain.sh 4.3.0` gate.
