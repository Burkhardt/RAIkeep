# CR010 — RaiDiagram subscriber-scoped artifacts and styles

**Requesting product:** AfricaStage  
**Requesting representatives:** Eliza, RAI, and the AfricaStage product team  
**Acceptance and testing:** Eliza, RAI, and the AfricaStage product team  
**Receiving product:** RAIkeep  
**Target release:** RAIkeep v4.2.2  
**Date:** 2026-08-17  
**Status:** Accepted by Eliza and AfricaStage — ready for RAIkeep implementation

## 1. Request

AfricaStage requests that RAIkeep extend RaiImage and RaiDiagram with typed
ImageTree artifacts and deterministic, subscriber-scoped PlantUML theme and
style lookup.

The requested implementation shall keep generated PlantUML source free of
presentation directives, apply the resolved configuration through PlantUML's
`-config` option, and store the authoritative manifest, generated source,
resolved configuration, and rendered images together under one existing
ImageTree subscriber location.

This CR incorporates the implementation plan prepared by RAIkeep after the
initial RaiDiagram discussion. Eliza formally accepted the request on
2026-08-17, clearing the implementation gate.

## 2. Outcome

RaiDiagram will render every diagram as one co-located ImageTree artifact set
under the caller-selected subscriber. Reusable PlantUML themes and styles will
also use existing subscriber/ImageTree placement. An explicitly ordered list of
fallback subscriber locations may refine styles without putting theme paths,
`!include` directives, or presentation syntax into generated `.puml` files.

RaiDiagram remains domain-neutral. `Subscriber` is a storage-routing concept,
not an authenticated identity. A consumer may use names such as AIA,
AfricaStage, a subscription, or a tenant as subscriber locations, but RaiImage
and RaiDiagram assign no identity-management or authorization meaning to them.

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
subscriber-based style lookup, typed artifact set, and the migration of the
prototypes away from using `ImageTreeFile` as a generic text-file path carrier.

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

Do not add an identity abstraction. Reuse `ItemTreePath`, `PathConventionType`,
and the existing subscriber-root convention to place non-image artifacts in the
same item bucket as `ImageTreeFile`.

Add a small `ImageTreeTextFile` adapter backed by `TextFile` and `ItemTreePath`.
Its placement inputs are only subscriber root, item id, path convention,
`NameExt`, and extension. It must expose the item path, full name, sibling
creation, directory creation, existence, and normal `TextFile` read/write
behavior without inheriting from `ImageFile`.

### 4.3 RaiDiagram

RaiDiagram owns diagram-specific artifact types and style resolution:

- `RaidFile` for the authoritative manifest or render snapshot;
- `PumlSourceFile` for clean generated PlantUML;
- `PumlConfigFile` for the complete resolved render configuration;
- `PumlStyleFile` for reusable style layers;
- `PumlThemeFile` for reusable PlantUML themes; and
- `DiagramArtifactSet` for the co-located group, including rendered `ImageTreeFile`
  instances such as SVG, PNG, and WebP.

Each text type will use `ImageTreeTextFile` and the existing `ItemTreePath`.
`ImageTreeFile` remains the correct type for SVG, PNG, WebP, JPEG, and other
rendered image formats.

The dependency direction remains:

`OsLib <- RaiImage <- RaiDiagram`

There will be no RaiImage dependency on RaiDiagram and no domain dependency on
AIA or AfricaStage.

## 5. Subscriber placement boundary

CR010 introduces no identity-management subsystem. Specifically, RaiImage and
RaiDiagram shall not add principals, authenticated identities, ownership
registries, tenant lifecycle, permissions, credentials, identity-provider
integration, or authorization behavior.

The existing `Subscriber` value remains a filesystem/ImageTree routing segment.
It may represent AIA, AfricaStage, a subscription, a tenant, or any other
consumer-selected partition. Systems with identity management may map their own
concepts onto subscriber paths; systems without identity management can use the
same APIs unchanged.

`DiagramDestination.Subscriber` remains the primary rendering API. No
`DiagramArtifactOwner`, owner identity, or automatic organizational hierarchy
is introduced. Invalid subscriber path injection continues to be rejected by
the existing RaiImage path boundary.

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
subscriber root, item id, convention, and item bucket:

```text
<ImageTreeRoot>/<subscriber>/<item-tree bucket>/
  ScheduleRehearsal.raid
  ScheduleRehearsal.puml
  ScheduleRehearsal_config.puml
  ScheduleRehearsal.svg
  ScheduleRehearsal.png       (optional)
  ScheduleRehearsal.webp      (optional)
```

Reusable style profiles are also ImageTree items under their subscriber. Their
item id is the profile id, while their filenames retain meaningful
PlantUML roles, for example:

```text
<subscriber profile bucket>/
  puml-theme-raikeep-sketch.puml
  raikeep-sketch_common.puml
  raikeep-sketch_usecase.puml
  raikeep-sketch_class.puml
```

The implementation must not assume that reusable profile artifacts and a
specific diagram share the same item id. They share the existing subscriber and
`ItemTreePath` placement mechanism.

## 7. Style and theme inheritance

Replace the current preassembled catalog-only flow with an explicit resolution
context and repository boundary. Proposed public concepts:

- `DiagramStyleResolutionContext`: diagram kind, profile id, explicitly ordered
  subscriber locations, diagram id, and per-diagram presentation intent;
- `IDiagramStyleRepository`: locates available local theme/style artifacts for
  a subscriber and profile without knowing AIA/AfricaStage semantics;
- `ImageTreeDiagramStyleRepository`: RaiImage-backed local implementation;
- `DiagramStyleLayer`: subscriber location, source path, scope (`common` or diagram kind),
  content hash, and precedence; and
- `ResolvedDiagramStyle`: ordered contributing layers plus the final
  `PumlRenderConfiguration`.

Resolution order follows only the caller-supplied list, from first fallback to
the selected subscriber location. RaiDiagram never walks parent directories or
infers an application/subscription/tenant hierarchy. A consumer may explicitly
supply locations that it regards as:

1. RAIkeep package/default layer, if explicitly supplied or seeded;
2. application layer;
3. subscription layer;
4. tenant layer;
5. diagram-kind layer within each subscriber location;
6. explicit presentation intent in the `.raid` manifest.

Later values override earlier values at the property level. Raw PlantUML style
sources that cannot be structurally merged are appended in deterministic layer
order, so PlantUML's later declaration wins. Duplicate location/scope entries and
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
hash and source path are captured before execution and rechecked afterward;
a mismatch fails the render.

The renderer continues to use the existing production chain:

`PlantUmlDiagramRenderer -> RaiImage.PlantUmlCommand -> OsLib.CliCommand -> RaiSystem`

No pruned or simulated PlantUML implementation is used for acceptance tests.

## 9. Rendering transaction

Refactor rendering into these explicit phases:

1. Validate the `.raid` model and requested subscriber destination.
2. Create one `DiagramArtifactSet` from the subscriber root and `ItemTreePath`.
3. Compile clean semantic PlantUML in memory.
4. Resolve and snapshot the explicitly supplied subscriber/style locations.
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
- keep `DiagramDestination.Subscriber` as the primary placement API;
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
expose an explicit seeding operation such as
`RaiDiagramDefaults.SeedTo(imageTreeRoot, subscriber)`.

Seeding must:

- use `RaiPath`, `TextFile`, and ImageTree artifact APIs;
- never run as an implicit static-initialization write;
- never overwrite a subscriber-local modified file unless the caller explicitly selects
  replacement behavior;
- return the paths and hashes of materialized files; and
- make no network request.

This gives AIA or AfricaStage a deliberate way to establish locally owned
defaults while keeping runtime behavior independent of GitHub availability.

## 12. Tests

### 12.1 RaiImage unit tests

- `ImageTreeTextFile` and `ImageTreeFile` derive the same bucket from subscriber
  root, item id, and every supported `PathConventionType`.
- Sibling creation preserves subscriber root, item id, convention, and bucket.
- Subscriber, `NameExt`, extension, and path injection are rejected.
- Existing `ImageTreeFile` behavior remains unchanged.

### 12.2 RaiDiagram unit tests

- Typed `.raid`, `.puml`, `_config.puml`, style, and theme files retain their
  `ItemTreePath` placement without masquerading as images.
- Config artifacts use `NameExt = "config"`, `Ext = "puml"`, and the resulting
  `_config.puml` filename throughout the RaiFile/RaiImage/RaiDiagram APIs.
- Common and diagram-kind layers resolve in deterministic order.
- Explicit fallback subscriber locations demonstrate deterministic precedence
  without hardcoding application, subscription, or tenant concepts.
- A subscriber-local override affects only resolutions that explicitly include
  that subscriber location.
- One model entity may be projected into multiple diagrams with independent
  presentation artifacts.
- Missing optional layers are skipped; missing explicitly selected layers fail
  fast.
- Resolution output and hashes are stable across repeated runs and independent
  of filesystem enumeration order.
- The generated `.puml` contains no theme, include, style, or handwritten
  directive.
- Config/source/layer changes alter the appropriate config and render hashes.
- Seed operations preserve subscriber-local edits unless replacement is explicit.

### 12.3 Real PlantUML acceptance tests

- Use the pinned, official, unmodified PlantUML CLI/JAR.
- Render the checked-in `.raid` example through the production command chain.
- Prove `-config` applies the selected subscriber and diagram-kind theme/style.
- Prove the deprecated handwritten warning is absent.
- Prove Chalkduster with Comic Sans MS fallback is present in SVG output.
- Prove `.raid`, `.puml`, `_config.puml`, and `.svg` share one subscriber item bucket.
- Prove SVG metadata refers to the authoritative manifest and exact resolved
  style/config hashes.

### 12.4 Regression and package verification

Run, in this order:

1. focused RaiImage ImageTree artifact tests;
2. focused RaiDiagram subscriber-style and placement tests;
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

Add an ADR, provisionally `ADR002_RaiDiagram_Subscriber_Scoped_Artifacts_and_Style_Lookup.md`,
because this is a RAIkeep architectural decision implementing CR009 rather than
a new AIA-originated change request.

Update:

- RaiImage `README.md` and `API.md` for ItemTree-based text artifacts;
- RaiDiagram `README.md` and `API.md` for artifact sets, subscriber locations, local
  repositories, config injection, and seeding;
- the checked-in `ScheduleRehearsal` example;
- CR009 with a short implementation-reference link, without rewriting its
  approved requirements; and
- the future v4.2.2 release notes only when the coordinated release is prepared.

## 14. Implementation sequence

1. Record ADR002 and freeze the public names and compatibility rules.
2. Implement and test generic RaiImage text placement using `ItemTreePath`.
3. Migrate RaiDiagram typed files to subscriber/ItemTree placement.
4. Introduce `DiagramArtifactSet` while retaining subscriber destination APIs.
5. Implement the local style repository and deterministic explicit fallbacks.
6. Make resolved config materialization auditable and race-resistant.
7. Refactor the renderer to the artifact-set transaction.
8. Add explicit default seeding.
9. Update the example, API documentation, and READMEs.
10. Run focused, real-CLI, full release-suite, build, pack, and diff checks.

## 15. Completion criteria

The work is ready for RAI's v4.2.2 release-chain decision when:

- every persisted diagram-related file has an explicit subscriber placement;
- image and text artifacts use one shared ImageTree placement contract while
  retaining truthful file types;
- subscriber fallback and diagram-kind lookup are deterministic and locally resolved;
- generated `.puml` remains presentation-free;
- the exact resolved configuration is stored beside each render;
- SVG provenance identifies the `.raid`, semantic state, style layers, config,
  and render;
- the official PlantUML CLI acceptance test passes without warning banners;
- RaiImage and RaiDiagram release suites and packs pass; and
- no package was versioned, tagged, pushed, published, or released by Codex.

## 16. Acceptance gate

Eliza formally accepted CR010 on behalf of AfricaStage on 2026-08-17. RAIkeep
may implement the approved request and will invite Eliza, RAI, and the
AfricaStage team to perform the acceptance testing described in section 12.

| Representative | Role | State |
|---|---|---|
| Eliza | AfricaStage acceptance | Accepted 2026-08-17 |
| RAI | Requester and acceptance tester | Requested |
| RAIkeep | Receiving implementation team | Implementation authorized |
