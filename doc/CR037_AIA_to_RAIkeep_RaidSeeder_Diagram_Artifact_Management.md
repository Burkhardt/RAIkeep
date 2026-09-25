# CR037: `RaidSeeder` Diagram Artifact Management and Cloud-Aware CLI

> **Document Path:** `doc/CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`  
> **Naming Schema:** `CR<NNN>_<Requester>_to_<Provider>_<Topic>.md`  
> **Follow-up Sub-CR Schema:** `CR037.<M>_<Requester>_to_<Provider>_<Topic>.md`  
> **Immutability Rule:** After AIA formally submits this CR, the provider must not rename this document.  
> **Date:** 2026-09-24  
> **Drafted By:** Dr. Rainer Burkhardt (`RAI`) and RAIkeep Lead Custodian (`Codex 702x`)  
> **Requesting Agent / PM:** Adele (`7010`, Product Manager, AIA Platform)  
> **Target Provider / Repo:** RAIkeep Lead Custodian (`Codex 702x`) / `Burkhardt/RAIkeep`  
> **Target Release:** Coordinated `RAIkeep v4.4.1` Suite Release  
> **Status:** Proposed & Formally Authorized by AIA PM for Implementation  
> **Parent CR:** `CR036_AIA_to_RAIkeep_Raid_CLI.md`  

---

## 1. Objective

`CR036_AIA_to_RAIkeep_Raid_CLI.md` introduced the `raid` command as a first-class RAIkeep CLI for importing PlantUML into canonical `.raid` manifests and hydratable SVG. That first release proved the ingestion pipeline, but its command surface was deliberately narrow:

```text
raid import --puml <diagram.puml> [--out <directory>] [--name <diagram-id>]
raid validate <diagram.raid|diagram.svg>
```

A diagram tool in the RAIkeep family must do more than seed an initial file. It must manage the complete, co-located diagram artifact set in an ImageTree:

1. the authoritative `.raid` manifest;
2. the derived PlantUML `.puml` representation; and
3. the derived `.svg` representation.

This CR promotes the tool from the temporary package identity `RaidCli` to **`RaidSeeder`**, while preserving the installed shell command **`raid`**. It adds cloud-aware addressing, export and refresh operations, typed OsLib invocation, and a terminal help experience equal to `pits` and `iorg`.

The desired family symmetry is:

| Library | Tool package | Shell command |
|---|---|---|
| `JsonPit` | `PitSeeder` | `pits` |
| `RaiImage` | `ImgSeeder` | `iorg` |
| `RaiDiagram` | `RaidSeeder` | `raid` |

---

## 2. Product Semantics & Architectural Invariants

### 2.1 Artifact Authority
Within a managed diagram artifact set:
- `<stem>.raid` is the authoritative semantic and presentation manifest;
- `<stem>.puml` is a derived textual interchange representation; and
- `<stem>.svg` is a derived visual representation.

An existing `.puml` or `.svg` sibling must never be assumed current merely because it exists. `raid` must derive current output from the authoritative `.raid` manifest and use deterministic content or semantic-hash evidence to decide whether a stored derivative is current.

This establishes the operational distinction between the two tree tools:
- `iorg` locates, moves, lists, and returns an existing image or SVG;
- `raid` manages the diagram and can return or write a freshly derived SVG or PUML that reflects the current `.raid` manifest.

### 2.2 Logical Diagram Identity
The managed identity is the structured tuple:
```text
ItemId + optional Number + optional NameExt + Extension
```

`NameExt` is not part of `ItemId`. For example, a Use Case Diagram for item `SignContract` has:
```text
ItemId  = SignContract
NameExt = UCD
```
and resolves to `SignContract_UCD.raid`, `SignContract_UCD.puml`, and `SignContract_UCD.svg`. If a numbered sibling is requested, the existing RAIkeep filename convention determines the position of `Number` before `NameExt`, for example `SignContract_01_UCD.svg`.

The CLI and its typed request contracts must preserve those fields separately. They must not parse or manufacture `ItemId = SignContract_UCD` as a substitute.

### 2.3 ItemTree Placement
Managed siblings must use `DiagramArtifactSet`, `ItemTreePath`, and the selected `PathConventionType`. The default is `ItemIdTree8x2`.

For example:
```text
<image-root>/AfricaStage/SignCont/SignContra/
  SignContract_UCD.raid
  SignContract_UCD.puml
  SignContract_UCD.svg
```

No arbitrary `/Activity/`, `/UseCase/`, or other type directory may be inserted between the subscriber and the deterministic ItemTree buckets.

### 2.4 Round-Trip Fidelity Invariant (Adele Refinement)
PUML emitted by `raid export --format puml` must possess syntactic and semantic round-trip fidelity:
1. Re-importing derived `.puml` back through `raid import --puml` must reproduce an equivalent semantic AST in the resulting `.raid` model.
2. Comments, notes, or non-semantic layout hints that cannot be mapped into the AOAIM archetype model must be gracefully ignored rather than causing import failures.

### 2.5 Static Seeder vs. Dynamic Execution Boundary (Adele Refinement)
`RaidSeeder` is a structural and visual artifact custodian, not an AOAIM reasoning engine:
1. When generating `hydratable` SVG, `RaidSeeder` emits structural nodes (`aim-act`, `aim-uc`, `aim-cls`, etc.), ports, routing, and declared infix expressions (`aim-expression="..."`).
2. `RaidSeeder` **must never evaluate or stamp dynamic runtime state attributes** (such as `aim-satisfied="true|false"`). Dynamic condition evaluation and state badge rendering belong strictly to the runtime platform (`AIA.Core` / `AomAgendaService` / `AomLinqEvaluator`). Static stored derivatives in the ImageTree must remain domain- and runtime-neutral.

---

## 3. Package and Repository Migration

### 3.1 New Package Identity
The 4.4.0 `RaidCli` package cannot be renamed in place on NuGet. This CR therefore requires a successor package:
- GitHub repository: `Burkhardt/RaidSeeder`;
- NuGet package ID: `RaidSeeder`;
- Product / Title: `RaidSeeder`;
- Installed tool command: `raid`;
- Coordinated version: `4.4.1`.

The expected installation and invocation are:
```bash
dotnet tool install --global RaidSeeder --version 4.4.1
raid --version
```

The shell command is intentionally `raid`, not `raidseeder`. The message emitted by `dotnet tool install` is owned by the .NET/NuGet client and is not a custom RAIkeep help surface.

### 3.2 Repository Migration
After this CR is formally submitted and provider work is authorized, the provider will:
1. Rename `Burkhardt/RaidCli` to `Burkhardt/RaidSeeder`;
2. Rename the umbrella submodule path and `.gitmodules` entry;
3. Update solution, workflow, documentation, and release-chain references;
4. Preserve Git history and the immutable `v4.4.0` tag;
5. Create or update the NuGet Trusted Publishing policy for repository `RaidSeeder`, workflow `publish-nuget.yaml`, and package `RaidSeeder`; and
6. Publish `RaidSeeder` only through RAI's coordinated manual release chain.

### 3.3 `RaidCli` Migration Notice
After `RaidSeeder 4.4.1` is successfully published and verified, `RaidCli` versions should be marked deprecated on NuGet with `RaidSeeder` as the replacement package. The immutable `RaidCli 4.4.0` package and tag must not be rewritten or reused.

Because both packages expose the `raid` command, migration guidance must state:
```bash
dotnet tool uninstall --global RaidCli
dotnet tool install --global RaidSeeder --version 4.4.1
```

---

## 4. Required Command Surface

`raid` must support four first-class verbs:
```text
import    ingest an external representation into a canonical .raid manifest
export    derive and export current .raid, .puml, and/or .svg artifacts
refresh   refresh missing or stale co-located derivatives in the ImageTree
validate  validate a .raid manifest, .puml source, or .svg representation
```

The existing `CR036` command remains backward compatible:
```bash
raid import --puml <diagram.puml> [--out <directory>] [--name <item-id>]
```

### 4.1 Import
`import` continues to use the extensible `IModelImporter` pipeline. When ImageTree addressing is supplied, it writes the canonical artifact set through `DiagramArtifactSet` rather than constructing paths procedurally.

Representative syntax:
```bash
raid import --puml Workflow.puml \
  -c OneDrive --app AIA -t nomsa \
  --name Workflow --name-ext AD
```

`--out <directory>` remains available for an explicit flat/external output directory. It is mutually exclusive with ImageTree destinations selected by `--root` or `--app`.

### 4.2 Export
`export` reads the authoritative `.raid` manifest and derives the requested current representation in memory before writing it to `--out` or the selected output stream. It must not blindly copy a possibly stale sibling `.puml` or `.svg` file.

Representative syntax:
```bash
raid export SignContract \
  -c OneDrive --app AIA -t AfricaStage \
  --name-ext UCD --format all --out ./export

raid export SignContract \
  -c OneDrive --app AIA -t AfricaStage \
  --name-ext UCD --format svg --svg-profile plain --out ./export
```

Required format selector:
```text
--format raid|puml|svg|all
```

Required SVG profiles:
```text
--svg-profile hydratable|plain
```
- `hydratable`: retains the public `aim-*` structure, ports, and declared expressions required by AIA Workbench and `@dr2rai/raid-canvas`;
- `plain`: preserves visible vector aesthetics but omits RAI/AIA `aim-*` hydration metadata for ordinary external viewers.

Exporting must not silently mutate the stored ImageTree artifact set. Updating stored siblings is the responsibility of `refresh`.

### 4.3 Refresh
`refresh` loads the authoritative `.raid` manifest, derives the expected PUML and SVG, compares them with the co-located siblings, and writes only missing or stale derivatives.

Representative syntax:
```bash
raid refresh SignContract \
  -c OneDrive --app AIA -t AfricaStage \
  --name-ext UCD
```

Required invariants:
1. A changed `.raid` manifest changes the next derived SVG and PUML.
2. A stale sibling is replaced by current derived content.
3. A sibling proven current is not rewritten; its modification timestamp and cloud-provider identity remain untouched.
4. A missing derivative is created directly at its final sibling address.
5. The authoritative `.raid` manifest is never rewritten merely because a derivative is refreshed.

### 4.4 Validate
The path-based validation remains supported:
```bash
raid validate <diagram.raid|diagram.puml|diagram.svg>
```
Validation must distinguish structural validity, semantic/provenance validity, and whether an SVG satisfies the `hydratable` or `plain` profile. Validation is strictly read-only.

---

## 5. Common Addressing Options

The cloud and ImageTree options must align with the mature `iorg` vocabulary:
```text
-c, --cloud <provider>       configured cloud provider
-r, --root <directory>       exact ImageTree root
-a, --app <directory>        application root; Image is resolved beneath it
-t, --tenant <name>          subscriber/tenant directory in the ImageTree
    --subscriber <name>      compatibility alias for --tenant
-p, --pathconv <1|2|3|4>     ItemTree path convention; ItemIdTree8x2 by default
    --name-ext <value>        optional NameExt, kept separate from ItemId
    --number <value>          optional artifact number, kept separate from ItemId
    --out <directory>         explicit flat/external output directory
```

`--root` and `--app` are alternative ways to resolve the ImageTree root:
- `--root AIA/Image` identifies the exact image root relative to `--cloud`;
- `--app AIA` resolves the application root and appends `Image`.

Thus these forms address the same tenant tree when the configured cloud root is the same:
```bash
raid refresh SignContract -c OneDrive --root AIA/Image -t AfricaStage --name-ext UCD
raid refresh SignContract -c OneDrive --app AIA        -t AfricaStage --name-ext UCD
```

Supplying contradictory destination options must fail fast with a concise usage error.

---

## 6. Help and Terminal Experience

`raid` must use the same polished presentation conventions as `pits` and `iorg`:
1. The RAI banner and aligned command/option columns;
2. The RAIkeep JetBrains Nerd Font glyph vocabulary, including provider-specific cloud glyphs;
3. `-h|--help`, `-v|--version`, `-n|--nologo`, and `-d|--debug`;
4. Command-level help for `import`, `export`, `refresh`, and `validate`;
5. Examples for flat output and cloud/tenant ItemTree use;
6. A clear explanation that the NuGet package is `RaidSeeder` while the command is `raid`; and
7. README guidance for terminal font installation (including Blink stylesheet guidance).

`raid --version` must output `raid v4.4.1` in coordinated v4.4.1 builds.

---

## 7. Public OsLib Boundary

OsLibCore must expose a typed `RaidCommand` wrapper parallel to `PitsCommand` and `IorgCommand`. It must support typed requests for import, export, refresh, and validate, including structured identity and cloud-address fields.

The wrapper must:
- Use `CliCommand` / `RaiSystem` rather than an individually baked process call;
- Preserve argument boundaries without shell concatenation;
- Expose exit code, stdout, and stderr through the established typed result;
- Serialize concurrent calls according to the existing OsLib command policy; and
- Receive argument-forwarding tests using a controlled fake executable.

### 7.1 Configuration Resolution (`RAICONFIG`) & Anti-Circumvention Invariant
`OsLibCore 4.4.1` resolves the default configuration location as:
```csharp
public static readonly string DefaultConfigFileLocation =
    Environment.GetEnvironmentVariable("RAICONFIG") ?? "~/.config/RAIkeep.json5";
```
This applies uniformly across all three suite tools: `pits`, `iorg`, and `raid`.

**Strict Anti-Circumvention Invariant:**
No test in `Burkhardt/RAIkeep` or consuming suites is permitted to use `RAICONFIG` to smuggle synthetic, mock, or rogue configuration files into test runs. Machine configuration and the canonical `RAIkeep.json5` schema remain authoritative. Unit and integration tests requiring isolated storage roots must continue to use explicit constructor parameters or established options objects, never hijacking `RAICONFIG` to evade operator configuration.

Every new public type and member must appear in the relevant foldable `API.md`.

---

## 8. Filesystem and Cloud-Safety Invariants

`CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md` remains absolute:
1. Never create or stage a managed artifact or directory in `Os.TempDir` and move it into a CloudDrive tree.
2. Never replace, rename, move, or swap an ItemTree directory as a unit.
3. Create a missing artifact directly at its final path through the `RaiPath`/`RaiFile` boundary.
4. Refresh an existing derivative in place using only the established cloud-safe file primitive.
5. A no-op refresh performs no write and no directory churn.
6. Do not use ad-hoc `System.IO` calls at the product boundary.

---

## 9. Required Verification

1. **Command and Help:** `raid --version` outputs `raid v4.4.1`; help layout tested as text against drift.
2. **Authority and Freshness:** Stale derivatives are refreshed; up-to-date derivatives cause no disk write; `.raid` remains unmodified.
3. **SVG Profiles:** `hydratable` passes `@dr2rai/raid-canvas` hydration; `plain` renders cleanly in standard SVG viewers without `aim-*`.
4. **PUML Determinism & Round-Trip:** Derived PUML is deterministic and round-trips back into `.raid`.
5. **ItemTree and Cloud-Safety:** `.raid`, `.puml`, and `.svg` share one stem in `ItemIdTree8x2`; no TempDir-to-cloud moves.
6. **Package Migration:** `dotnet tool install --global RaidSeeder --version 4.4.1` installs command `raid`.

---

## 10. Documentation and Release Records

The coordinated release must update:
- Root and package README files;
- `API.md` for OsLibCore, RaiDiagram, and RaidSeeder;
- Release notes for all eight packages referencing `CR037_AIA_to_RAIkeep_RaidSeeder_Diagram_Artifact_Management.md`:
  `OsLib -> RaiUtils -> RaiImage -> RaiDiagram -> RaidSeeder -> JsonPit -> ImgSeeder -> PitSeeder -> RAIkeep umbrella release`
- All eight packages remain version-aligned at **`4.4.1`**.

---

## 11. Governance and Delivery Authorization

This Change Request is formally submitted by Adele (`7010`, PM AIA) and authorizes implementation by the RAIkeep Lead Custodian (`Codex 702x`):

1. **Implementation & Tests:** RAIkeep owns implementation and internal unit tests across `RaidSeeder`, `RaiDiagram`, and `OsLibCore`.
2. **Release Preparation:** RAIkeep commits all package changes and prepares `scripts/release-chain.sh 4.4.1`, then stops.
3. **Manual Release Chain:** Dr. Rainer Burkhardt (`RAI`) alone executes `scripts/release-chain.sh 4.4.1`.
4. **Requester Evaluation:** Adele and Zébio will independently evaluate the release in AIA and record `CR037_Accepted_RaidSeeder_Diagram_Artifact_Management.md`.
