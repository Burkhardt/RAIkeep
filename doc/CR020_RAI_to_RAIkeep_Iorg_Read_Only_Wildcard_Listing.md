# CR020 — `iorg` Media & Diagram Tree Custodianship (`list` and `move`)

**Requesting products:** AIA & AfricaStage (Subscriber Media & Diagram Tree Custodianship)

**Authors & Contributors:**
- RAI (Dr. Rainer Burkhardt — Founder & Chief Product Officer)
- Adele (Product Manager, AIA)
- Codex (Owner & Lead Custodian, RAIkeep)

**Requester and acceptance owner:** RAI

**Provider / Implementation Lead:** Codex (Owner, RAIkeep)

**Affected packages:** ImgSeeder (`iorg`), `OsLibCore`, `RaiImage`, `RaiDiagram`

**Proposed coordinated release:** RAIkeep v4.2.7 (all seven packages)

**Date proposed:** 2026-09-08

**Status:** Accepted, implemented, and provider-verified; publication remains behind RAI's manual gate

---

## 1. Purpose & Architecture

Establish `iorg` as the authoritative, consistency-preserving **Media and Diagram Tree Custodian CLI**. 

A subscriber's media tree legitimately hosts both **Image Assets** (source graphics and rendered derivatives) and **Diagram Files** (`.puml` Diagram specifications, `.raid` Diagram Models, and `_config.puml` Diagram Style/Header includes). 

Managing this tree requires two core capabilities:
1. **Discovery (`iorg list`)**: A first-class, strictly read-only wildcard discovery command for finding images, derivatives, and diagram files across the subscriber hierarchy.
2. **Item Relocation & Renaming (`iorg move`)**: A deterministic command that moves and/or renames all assets bound to a specific `ItemId` across bucket path conventions (e.g. `ItemIdTree3x3` $\leftrightarrow$ `ItemIdTree8x2`) without leaving orphaned derivatives or disturbing unrelated sibling items.

CR020 also removes the generic Legacy row from the root help screen. The supported `-r` option is the short form of `--root`; it is not legacy or deprecated.

---

## 2. Media and Diagram Tree Taxonomy

`iorg` recognizes the following canonical asset classes within a subscriber's tree:

| Category | File Extensions | Role & Description |
|---|---|---|
| **Image Assets** | `.svg`, `.webp`, `.png`, `.jpg`, `.jpeg`, `.avif` | Graphical assets and rendered template derivatives (`Small`, `Large`, `Huge`, `Stamp`). |
| **Diagram Files** | `.puml` | **Diagram File:** PlantUML diagram specifications. |
| | `.raid` | **Diagram Model File:** Declarative architectural models and metadata manifests. |
| | `*_config.puml` | **Diagram Style/Header File:** Item-owned resolved skinparams, theme palettes, and macros. |
| **Rich Media *(Future)*** | `.mp4`, `.webm` | Time-based audio/visual media assets. |

### Diagram Asset Tuple
For any diagram entity, `MyDiagram.puml`, `MyDiagram_config.puml`, `MyDiagram.raid`, and `MyDiagram.svg` share the exact same `ItemId` (`MyDiagram`). They form an **atomic tuple** that moves, renames, and deletes together in lockstep within the same convention-derived item home.

---

## 3. Path Convention Options (`--pathconv`)

The path layout of the subscriber tree is determined by `PathConventionType`:

| Option Value | Enum Name | Structure Description | Example Layout for `AfricanBrisket` |
|---|---|---|---|
| `1` | `CanonicalByName` | Full ItemId directory | `AfricanBrisket/AfricanBrisket_01.png` |
| `2` | `ItemIdTree3x3` | 3-char 1st tier / cumulative 6-char 2nd tier | `Afr/Africa/AfricanBrisket_01.png` |
| `3` *(Default)* | `ItemIdTree8x2` | 8-char 1st tier / cumulative 10-char 2nd tier | `AfricanB/AfricanBri/AfricanBrisket_01.png` |
| `4` | `Flat` | Unbucketed subscriber root | `AfricanBrisket_01.png` |

In CLI help menus, options are displayed with numbers ahead of the enum name, indicating the active default:
```text
--pathconv <convention>   Path convention to apply:
                            1: CanonicalByName
                            2: ItemIdTree3x3
                            3: ItemIdTree8x2 (default)
                            4: Flat
```

---

## 4. Proposed CLI Contracts

### 4.1. `iorg list` (Read-Only Wildcard Discovery)

```text
iorg list <FileNamePattern> [--subscriber <name>] (-r|--root) <dir> [global options]
```

#### Examples:
```bash
# Search for all image and diagram assets matching a prefix
iorg list 'WorkInPro*' -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa

# Search for all PlantUML diagram files
iorg list '*.puml' -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa

# Complete inventory of a subscriber tree
iorg list '*' -c OneDrive --root LiveAfricaStageImage/Nomsa
```

#### Semantics:
- Matches `FileNamePattern` against each candidate file's actual `NameWithExtension`.
- Evaluates across all legitimate assets in the subscriber tree (Images, `.puml`, `.raid`, `_config.puml`).
- Strictly read-only; zero mutation side-effects. Returns exit code `0` on 0 matches.

---

### 4.2. `iorg move` (Deterministic ItemId Relocation & Renaming)

```text
iorg move <SourceItemId> [<TargetItemId>] [--pathconv <1|2|3|4>] [--subscriber <name>] (-r|--root) <dir> [global options]
```

`iorg move` operates strictly on **`ItemId`**, NOT arbitrary wildcard string renaming.

#### Use Cases:

1. **Path Convention Migration (without renaming):**
   Migrate `AfricanBrisket` from `ItemIdTree3x3` (`Afr/Africa/`) to `ItemIdTree8x2` (`AfricanB/AfricanBri/`):
   ```bash
   iorg move AfricanBrisket --pathconv 3 -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa
   ```
   *Behavior:*
   - Finds all files bound to `ItemId = AfricanBrisket`:
     - `AfricanBrisket_01.png`
     - `AfricanBrisket_01_Small.webp`
     - `AfricanBrisket_01_Huge.avif`
     - `AfricanBrisket.puml`
     - `AfricanBrisket.raid`
     - `AfricanBrisket.svg`
   - Computes the target item home once through `ItemTreePath(rootPath, "AfricanBrisket", PathConventionType.ItemIdTree8x2)`.
   - Moves files to `AfricanB/AfricanBri/`.
   - **Crucial Invariant:** Sibling items in the source folder (e.g. `AfricanBreakfast_01.png`) are **completely untouched**.
   - Prunes empty source parent folders.

2. **ItemId Renaming (with automatic bucket relocation):**
   Rename `AfricanPicnic` $\rightarrow$ `AfricanBreakfast`:
   ```bash
   iorg move AfricanPicnic AfricanBreakfast --pathconv 3 -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa
   ```
   *Behavior:*
   - Moves and renames all source images, rendered derivatives, and diagram tuples:
     - `AfricanPicnic_01.png` $\rightarrow$ `AfricanBreakfast_01.png`
     - `AfricanPicnic_01_Small.webp` $\rightarrow$ `AfricanBreakfast_01_Small.webp`
     - `AfricanPicnic.puml` $\rightarrow$ `AfricanBreakfast.puml`
     - `AfricanPicnic.raid` $\rightarrow$ `AfricanBreakfast.raid`
   - Relocates them from `AfricanP/AfricanPic/` to `AfricanB/AfricanBre/`.

3. **Variant / Sub-Index Move:**
   Move `AfricanBreakfast_04` $\rightarrow$ `AfricanLunch_01`:
   ```bash
   iorg move AfricanBreakfast_04 AfricanLunch_01 --pathconv 3 -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa
   ```

---

### 4.3. `iorg clean` (Cache Purge & Deletion Authority)

`iorg clean` provides authoritative, consistency-preserving cleanup:
- **`iorg clean --cache`**: Purges only *rendered derivative variants* (`*.webp`, `*.avif`, `*_Small.*`, `*_Large.*`), preserving all source images, `.puml`, `.raid`, and `_config.puml` files.
- **`iorg clean <ItemId> --force`**: Deletes all files associated with `<ItemId>` (including its source image, rendered derivatives, `.puml`, and `.raid` files) when an operator explicitly removes an asset.

---

## 5. Search, Relocation and Storage Boundary

Implementation rules for `RaiImage` and `ImgSeeder`:
- `ItemTreePath` is the object-oriented tree home of one subscriber-local `ItemId` and every physical file belonging to it.
- `ItemTreePath.SelectFiles()` returns `IReadOnlyList<RaiFile>` for the exact `ItemId`, across image and diagram extensions, while excluding bucket-sharing sibling ItemIds.
- Aggregate relocation follows the destination-oriented `RaiFile.mv(...)` idiom: `destinationItemPath.mv(sourceItemPath)`.
- Typed `ImageTreeFile`, `ItemTreeTextFile`, `RaidFile`, `PumlSourceFile`, `PumlConfigFile`, `PumlStyleFile`, and `PumlThemeFile` constructors accept `ItemTreePath`; no `FromImageTree`/`FromItemTree` factory is required.
- The destination `ItemTreePath` supplies both target ItemId and path convention, supporting relocation, rename-plus-relocation, and Flat/tree migration with the same operation.
- Use only `RaiPath` / `RaiFile` filesystem boundaries.
- Preserve CR016's canonical-equivalent Unicode NFC/NFD lookup behavior.
- In `iorg move`, preflight the complete move set, create destination directories through `RaiFile.mv(...)`, roll back completed file moves on a later failure where possible, and prune vacated bucket directories.
- Never use raw `System.IO` primitives or unstructured string path concatenation.

---

## 6. Output and Exit Behavior

1. **Standard Output (`iorg list`):** Emits one `NameWithExtension` per matched physical file, followed by a concise count summary.
2. **Standard Output (`iorg move`):** Emits each moved/renamed file pair (`source -> destination`), followed by the count of relocated files.
3. **Machine-Readable Flags (`--json` / `--quiet`):** Emits clean JSON array or newline-delimited output for scripting without trailing human summary lines.
4. **Exit Codes:**
   - Zero matches on `list` exits `0`.
   - Successful `move` exits `0`.
   - Invalid syntax, missing source `ItemId`, or filesystem permission errors exit nonzero.

---

## 7. Typed `OsLibCore` Boundary

`OsLibCore` exposes typed requests and wrappers:

```csharp
public sealed record IorgListRequest(string FileNamePattern, RaiPath Root)
{
    public IorgCommandOptions Options { get; init; }
}

public sealed record IorgMoveRequest(
    string SourceItemId,
    string? TargetItemId,
    RaiPath Root,
    PathConventionType PathConvention = PathConventionType.ItemIdTree8x2)
{
    public IorgCommandOptions Options { get; init; }
}
```

`IorgCommand` provides:

```csharp
RaiSystemResult List(IorgListRequest request);
Task<RaiSystemResult> ListAsync(IorgListRequest request, CancellationToken ct = default);

RaiSystemResult Move(IorgMoveRequest request);
Task<RaiSystemResult> MoveAsync(IorgMoveRequest request, CancellationToken ct = default);
```

---

## 8. Required Verification

### 8.1 ImgSeeder Behavior
- `list` returns exact filenames, wildcards (`WorkInPro*`, `*.puml`, `*.raid`), and full tree (`*`).
- `move` relocates all files of `AfricanBrisket` across path conventions (3x3 $\leftrightarrow$ 8x2) while leaving `AfricanBreakfast` untouched.
- `move` renames stem `AfricanPicnic` $\rightarrow$ `AfricanBreakfast` across source images, derivatives, and `.raid`/`.puml` pairs.
- Empty parent directories are cleanly pruned after moving.
- `clean --cache` purges only derivatives, while `clean <ItemId>` removes the complete item tuple.

### 8.2 OsLibCore Wrapper
- Argument arrays asserted for mandatory and optional flags (`--pathconv 1`, `--subscriber`).
- Sync and async capture-command tests prove identical tokens reach the child process.

### 8.3 Release Gates
- Full `OsLibCore`, `ImgSeeder`, `RaiImage`, and `RaiDiagram` test suites green.
- Coordinated seven-package Release build and test gate.

---

## 9. Release and Authority

Coordinated release designation: **RAIkeep v4.2.7** across all seven packages. Implementation begins upon acceptance by Codex. Release and publication to NuGet remain behind RAI's manual release gate.
