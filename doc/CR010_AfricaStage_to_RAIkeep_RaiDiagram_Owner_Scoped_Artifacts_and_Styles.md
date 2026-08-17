# CR010 — RaiDiagram owner-scoped artifacts and styles

**Requesting product:** AfricaStage  
**Requesting representatives:** Eliza, RAI, and the AfricaStage product team  
**Acceptance and testing:** Eliza, RAI, and the AfricaStage product team  
**Receiving product:** RAIkeep  
**Target release:** RAIkeep v4.2.2  
**Date:** 2026-08-17  
**Status:** Accepted

## 1. Request

AfricaStage requests that RAIkeep extend RaiImage and RaiDiagram with an
explicitly owned ImageTree artifact model and deterministic, owner-scoped
PlantUML theme and style inheritance.

The requested implementation shall keep generated PlantUML source free of
presentation directives, apply the resolved configuration through PlantUML's
`-config` option, and store the authoritative manifest, generated source,
resolved configuration, and rendered images together under one owner.

This CR incorporates the implementation plan prepared by RAIkeep after the
initial RaiDiagram discussion. Implementation remains paused until Eliza and
AfricaStage formally accept this request.

## 2. Outcome

RaiDiagram will render every diagram as one explicitly owned, co-located
ImageTree artifact set. Reusable PlantUML themes and styles will also be
owner-scoped ImageTree artifacts. A deterministic inheritance chain will allow
more specific owners to refine or override less specific owners without putting
theme paths, `!include` directives, or presentation syntax into generated
`.puml` files.

RaiDiagram remains domain-neutral. It will understand an ordered chain of
owners, but not concepts such as AIA, AfricaStage, subscription, tenant, or
WWWA. Consumers assign those meanings and supply the chain.

The runtime will not download themes from GitHub. Repository assets are
portable defaults and examples that a consumer may explicitly seed into its
local ImageTree.

## 3. Current foundation

The current v4.2.2 worktree already contains the following foundations:

- clean semantic `.puml` generation with presentation excluded;
- PlantUML `-config` injection through the real production command path;
- programmable `PumlStyleSheet` rules and diagram-kind selection;
- `PumlStyleFile`, `PumlThemeFile`, and `PumlConfigFile` prototypes;
- local theme validation with no implicit remote theme resolution;
- sibling `.raid`, `.puml`, `_config.puml`, and `.svg` output;
- semantic, config, and render hashes embedded in SVG provenance;
- an example artifact set rendered by the official PlantUML CLI; and
- regression coverage for real CLI rendering, kind-specific styling, local
  themes, and the absence of the deprecated handwritten warning.

These foundations should be retained. The remaining work is principally the
ownership abstraction, hierarchical style lookup, typed artifact set, and
the migration of the prototypes away from using `ImageTreeFile` as a generic
text-file path carrier.

## 4. Package boundary

### 4.1 OsLib

No new diagram concepts belong in OsLib. RaiDiagram and RaiImage will continue
to use `RaiPath`, `RaiRelPath`, `RaiFile`, `TextFile`, and the existing command
abstractions. No direct `System.IO` usage is planned. If implementation exposes
a missing filesystem primitive, it must be raised with RAI before adding a
`System.IO` call.

### 4.2 RaiImage

RaiImage owns the reusable ImageTree placement contract because it already owns
`ItemTreePath`, `PathConventionType`, and `ImageTreeFile`.

Add a small, immutable, non-image-specific identity/address type, provisionally
named `ImageTreeArtifactIdentity`, containing:

- ImageTree root;
- validated owner path;
- item id;
- path convention; and
- derived item bucket (`TopdirRoot` and `SubdirRoot`).

The identity computes placement only; it does not claim that the artifact is an
image. `ImageTreeFile` and diagram text files use the same identity and therefore
the same owner and directory convention.

Add a generic owner-scoped text-file base or adapter, provisionally named
`ImageTreeTextFile`, backed by `TextFile` plus `ImageTreeArtifactIdentity`.
It must expose the identity, full name, sibling creation, directory creation,
existence, and normal `TextFile` read/write behavior without inheriting from
`ImageFile`.

### 4.3 RaiDiagram

RaiDiagram owns diagram-specific artifact types and style resolution:

- `RaidFile` for the authoritative manifest or render snapshot;
- `PumlSourceFile` for clean generated PlantUML;
- `PumlConfigFile` for the complete resolved render configuration;
- `PumlStyleFile` for reusable style layers;
- `PumlThemeFile` for reusable PlantUML themes; and
- `DiagramArtifactSet` for the owned group, including rendered `ImageTreeFile`
  instances such as SVG, PNG, and WebP.

Each text type will use `ImageTreeTextFile` or compose the shared identity.
`ImageTreeFile` remains the correct type for SVG, PNG, WebP, JPEG, and other
rendered image formats.

The dependency direction remains:

`OsLib <- RaiImage <- RaiDiagram`

There will be no RaiImage dependency on RaiDiagram and no domain dependency on
AIA or AfricaStage.

## 5. Ownership model

Introduce a domain-neutral owner-path value, provisionally named
`DiagramArtifactOwner`, made from one or more validated relative segments.
Absolute paths, `..`, empty segments, and path separator injection must be
rejected.

Examples supplied by consumers may map to:

1. `RAIkeep`
2. `AIA`
3. `AfricaStage/<subscription>`
4. `AfricaStage/<subscription>/<tenant>`
5. the individual diagram artifact set

Those names and meanings are examples only. RaiDiagram receives already ordered
owners and does not infer organizational structure.

Every persisted runtime style, theme, config, manifest snapshot, source, or
rendered image must have an owner. Standalone files may still be opened for
authoring and migration, but they do not participate in owner inheritance until
attached to an owner identity.

## 6. Artifact placement and naming

The resolved PlantUML configuration is a `.puml` file with `config` in the
existing RaiFile `NameExt` field. `config` is not a compound extension. For
example:

```text
Name      = CenterUseCase
NameExt   = config
Ext       = puml
Full name = CenterUseCase_config.puml
```

All factories, render results, command arguments, examples, tests, and
documentation must use this contract. `CenterUseCase.config.puml` and an
extension value of `config.puml` are not valid representations of the resolved
configuration.

For a diagram item such as `ScheduleRehearsal`, all render artifacts share one
owner, item id, convention, and item bucket:

```text
<ImageTreeRoot>/<owner path>/<item-tree bucket>/
  ScheduleRehearsal.raid
  ScheduleRehearsal.puml
  ScheduleRehearsal_config.puml
  ScheduleRehearsal.svg
  ScheduleRehearsal.png       (optional)
  ScheduleRehearsal.webp      (optional)
```

Reusable style profiles are also ImageTree items under their owner. Their item
identity is the profile identity, while their filenames retain meaningful
PlantUML roles, for example:

```text
<owner profile bucket>/
  puml-theme-raikeep-sketch.puml
  raikeep-sketch.common.style.puml
  raikeep-sketch.usecase.style.puml
  raikeep-sketch.class.style.puml
```

The implementation must not assume that reusable profile artifacts and a
specific diagram share the same item id. They share the same placement and
ownership mechanism.

## 7. Style and theme inheritance

Replace the current preassembled catalog-only flow with an explicit resolution
context and repository boundary. Proposed public concepts:

- `DiagramStyleResolutionContext`: diagram kind, profile id, ordered owner
  chain, diagram identity, and explicit per-diagram presentation intent;
- `IDiagramStyleRepository`: locates available local theme/style artifacts for
  an owner and profile without knowing AIA/AfricaStage semantics;
- `ImageTreeDiagramStyleRepository`: RaiImage-backed local implementation;
- `DiagramStyleLayer`: owner, source identity, scope (`common` or diagram kind),
  content hash, and precedence; and
- `ResolvedDiagramStyle`: ordered contributing layers plus the final
  `PumlRenderConfiguration`.

Resolution order is least specific to most specific:

1. RAIkeep package/default layer, if explicitly supplied or seeded;
2. application layer;
3. subscription layer;
4. tenant layer;
5. diagram-kind layer within each owner;
6. explicit presentation intent in the `.raid` manifest.

Later values override earlier values at the property level. Raw PlantUML style
sources that cannot be structurally merged are appended in deterministic layer
order, so PlantUML's later declaration wins. Duplicate owner/scope entries and
ambiguous precedence must fail validation instead of relying on filesystem
enumeration order.

Missing optional inherited layers are skipped. A profile, style, or theme named
explicitly by the diagram or caller is required and must fail fast with the
appropriate RAI exception when absent.

## 8. PlantUML configuration materialization

The compiler continues to produce presentation-free `.puml`.

The resolver produces one deterministic `_config.puml` using
`NameExt = "config"` and `Ext = "puml"`, and the renderer passes it to PlantUML
with `-config`. The resolved config records the ordered source layer identities
and hashes in comments for auditability.

Local source files must be read through RAI file classes before execution. The
resolved config should be self-contained wherever PlantUML syntax permits so a
render does not silently change when a reusable source file is edited during
execution. If a PlantUML theme must remain path-referenced, its exact content
hash and path identity are captured before execution and rechecked afterward;
a mismatch fails the render.

The renderer continues to use the existing production chain:

`PlantUmlDiagramRenderer -> RaiImage.PlantUmlCommand -> OsLib.CliCommand -> RaiSystem`

No pruned or simulated PlantUML implementation is used for acceptance tests.

## 9. Rendering transaction

Refactor rendering into these explicit phases:

1. Validate the `.raid` model and requested owner destination.
2. Create one `DiagramArtifactSet` identity.
3. Compile clean semantic PlantUML in memory.
4. Resolve and snapshot the complete owner/style chain.
5. Persist `.raid`, `.puml`, and `_config.puml` siblings.
6. Invoke the real PlantUML CLI with `-config`.
7. Verify that the expected SVG exists and contains no PlantUML error/warning
   banner.
8. Embed `.raid` identity, semantic hash, config hash, render hash, and style
   layer provenance into the SVG.
9. Re-read and verify the SVG metadata before returning the artifact set.

The public async operation should return only after every required artifact is
present and mutually consistent. Partial failures must not be reported as a
successful artifact set. Cleanup behavior must use RAI file/path APIs and be
covered by tests before any deletion is introduced.

## 10. Compatibility and migration

Keep currently released v4.2.0 entry points source-compatible:

- retain `DiagramDestination.Subscriber` as a one-segment compatibility path;
- add the owner-path API alongside it and reject conflicting simultaneous
  values;
- retain existing `ImageTreeFile.RenderPlantUml` overloads;
- retain existing result properties while adding typed artifact access; and
- document the compatibility members as adapters, not the preferred new model.

Because `PumlStyleFile`, `PumlThemeFile`, and `PumlConfigFile` are current
v4.2.2 worktree additions, replace their provisional `ImageTreeAsset` shortcut
before release rather than preserving it as public debt.

No package version is changed while implementing or testing this plan.

## 11. Default assets and seeding

Keep the checked-in RAIkeep sketch theme and examples in Git for source control,
documentation, and package tests. If defaults are shipped in the NuGet package,
expose an explicit seeding operation such as `RaiDiagramDefaults.SeedTo(owner)`.

Seeding must:

- use `RaiPath`, `TextFile`, and ImageTree artifact APIs;
- never run as an implicit static-initialization write;
- never overwrite an owner-modified file unless the caller explicitly selects
  replacement behavior;
- return the identities and hashes of materialized files; and
- make no network request.

This gives AIA or AfricaStage a deliberate way to establish locally owned
defaults while keeping runtime behavior independent of GitHub availability.

## 12. Tests

### 12.1 RaiImage unit tests

- `ImageTreeArtifactIdentity` derives the same bucket as `ImageTreeFile` for
  every supported `PathConventionType`.
- Nested owner paths are preserved.
- Text and image artifacts created from the same identity share `SubdirRoot`.
- Sibling creation preserves owner, item id, convention, and bucket.
- Absolute owner paths, traversal, separators in segments, and extension/path
  injection are rejected.
- Existing `ImageTreeFile` behavior remains unchanged.

### 12.2 RaiDiagram unit tests

- Typed `.raid`, `.puml`, `_config.puml`, style, and theme files retain their
  artifact identity without masquerading as images.
- Config artifacts use `NameExt = "config"`, `Ext = "puml"`, and the resulting
  `_config.puml` filename throughout the RaiFile/RaiImage/RaiDiagram APIs.
- Common and diagram-kind layers resolve in deterministic order.
- Application, subscription, tenant, and diagram overrides demonstrate the
  generic owner precedence without hardcoding those domain names in production
  code.
- A tenant override affects only that tenant's resolution.
- One model entity may be projected into multiple diagrams with independent
  presentation artifacts.
- Missing optional layers are skipped; missing explicitly selected layers fail
  fast.
- Resolution output and hashes are stable across repeated runs and independent
  of filesystem enumeration order.
- The generated `.puml` contains no theme, include, style, or handwritten
  directive.
- Config/source/layer changes alter the appropriate config and render hashes.
- Seed operations preserve owner edits unless replacement is explicit.

### 12.3 Real PlantUML acceptance tests

- Use the pinned, official, unmodified PlantUML CLI/JAR.
- Render the checked-in `.raid` example through the production command chain.
- Prove `-config` applies the selected owner and diagram-kind theme/style.
- Prove the deprecated handwritten warning is absent.
- Prove Chalkduster with Comic Sans MS fallback is present in SVG output.
- Prove `.raid`, `.puml`, `_config.puml`, and `.svg` share one owned item bucket.
- Prove SVG metadata refers to the authoritative manifest and exact resolved
  style/config hashes.

### 12.4 Regression and package verification

Run, in this order:

1. focused RaiImage ImageTree artifact tests;
2. focused RaiDiagram style/ownership tests;
3. real PlantUML acceptance tests;
4. complete RaiImage release test suite;
5. complete RaiDiagram release test suite;
6. release builds and `dotnet pack` for RaiImage and RaiDiagram into temporary
   output directories; and
7. `git diff --check` in both repositories and the umbrella.

No tag, push, NuGet publication, release-chain execution, or package-version
change is part of implementation verification. RAI starts the coordinated
v4.2.2 release chain separately after reviewing the completed work.

## 13. Documentation and decision record

Add an ADR, provisionally `ADR002_RaiDiagram_Owner_Scoped_Artifacts_and_Style_Inheritance.md`,
because this is a RAIkeep architectural decision implementing CR009 rather than
a new AIA-originated change request.

Update:

- RaiImage `README.md` and `API.md` for the generic ImageTree artifact identity;
- RaiDiagram `README.md` and `API.md` for artifact sets, owner chains, local
  repositories, config injection, and seeding;
- the checked-in `ScheduleRehearsal` example;
- CR009 with a short implementation-reference link, without rewriting its
  approved requirements; and
- the future v4.2.2 release notes only when the coordinated release is prepared.

## 14. Implementation sequence

1. Record ADR002 and freeze the public names and compatibility rules.
2. Implement and test the generic RaiImage artifact identity/text placement.
3. Migrate RaiDiagram typed files to the generic identity.
4. Introduce `DiagramArtifactSet` and owner-aware destination/result APIs.
5. Implement the local style repository and deterministic owner inheritance.
6. Make resolved config materialization auditable and race-resistant.
7. Refactor the renderer to the artifact-set transaction.
8. Add explicit default seeding.
9. Update the example, API documentation, and READMEs.
10. Run focused, real-CLI, full release-suite, build, pack, and diff checks.

## 15. Completion criteria

The work is ready for RAI's v4.2.2 release-chain decision when:

- every persisted diagram-related file has an explicit owner identity;
- image and text artifacts use one shared ImageTree placement contract while
  retaining truthful file types;
- owner and diagram-kind inheritance is deterministic and locally resolved;
- generated `.puml` remains presentation-free;
- the exact resolved configuration is stored beside each render;
- SVG provenance identifies the `.raid`, semantic state, style layers, config,
  and render;
- the official PlantUML CLI acceptance test passes without warning banners;
- RaiImage and RaiDiagram release suites and packs pass; and
- no package was versioned, tagged, pushed, published, or released by Codex.

## 16. Acceptance gate

Implementation shall not begin until Eliza formally accepts CR010 on behalf of
AfricaStage. RAIkeep will then implement the approved request and invite Eliza,
RAI, and the AfricaStage team to perform the acceptance testing described in
section 12.

| Representative | Role | State |
|---|---|---|
| Eliza | AfricaStage acceptance | Accepted |
| RAI | Requester and acceptance tester | Requested |
| RAIkeep | Receiving implementation team | Waiting for acceptance |
