# CR060 — Intermediate Numeric Token Preservation, Iorg Flag Ergonomics, and Image Number Filter

**Origin:** AfricaStage Tenant (`MondayShow` archive) to `RAIkeep` Platform (`RaiImage`, `ImgSeeder`)
**Status:** Submitted / Accepted for RAIkeep 4.5.9 inner loop
**Primary References:** `CR054_Compact-Range-Receipts-and-PascalCase.md`, `RaiImage/ImageFile.cs`, `ImgSeeder/Program.cs`

---

## 1. Problem Statement

### 1.1 Premature Discard of Substantive Numeric Tokens in Stems
CR054 specified: *"Terminal delimiter-separated numeric tokens are discarded except the final sequence number."*
In real-world media archives (such as AfricaStage Monday Show photo sets), filenames regularly contain intermediate numbers that represent substantive item identification (e.g. event year 2026 / 26, show edition, edition code, camera body number):
```text
Nomsa-San-Diego-State-26-1.jpg
Nomsa-San-Diego-State-26-10.jpg
Nomsa-San-Diego-State-26-100.jpg
Nomsa-San-Diego-State-26-101.jpg
```
Under the current `ImageFile.SplitTrailingImageNumber` regex, the intermediate token `-26` was discarded from the stem (`NomsaSanDiegoState`) rather than preserved as part of the item identity (`NomsaSanDiegoState26`). When batch-importing archives containing multiple conventions or singleton files (e.g. `Nomsa-San-Diego-State-26.jpg`), this caused false collision preflight failures:
```text
error: Multiple source images resolve to the same destination: NomsaSan/NomsaSanDi/NomsaSanDiegoState_026.jpg
Nomsa-San-Diego-State-26-10.jpg: Import preflight failed; no copy attempted.
```

### 1.2 Mandatory `--import-id` and Missing Receipt Output Redirection
Running:
```bash
iorg organize --cloud OneDrive --app AfricaStage --subscriber NOMSA --source /path/to/archive.zip --json
```
abruptly fails with:
```text
error: --json or --exif requires --import-id for the ImageImport receipt.
```
Requiring the caller to invent and pass an arbitrary `--import-id` merely to obtain `--json` output is unnecessary friction. Furthermore, operators had no option to redirect the receipt to a file without shell `> receipt.json` redirection.

### 1.3 Missing Image Number Filter in `iorg clean`
Currently, `iorg clean <ItemId>` is an all-or-nothing operation for the specified item: it selects all images for that item (e.g. `_001` through `_193` and all size derivatives). When operators need to clean or replace only a specific image number (e.g. `100`), there is no way to filter the deletion without manual filesystem intervention.

### 1.4 Missing Short-Flag Parity (`-s`)
While legacy mode supports `-s` as an alias for `--source`, `iorg organize` omitted `-s` from its options parser, rejecting standard short-flag syntax.

### 1.5 Documentation Coupling Between `iorg` and `jpit`/`pits`
`ImgSeeder/README.md` previously included `pits seed Object ...` and `jpit seed Object ...` downstream commands in its introductory example, confusing new operators by implying that image imports require a Pit repository.

---

## 2. Requirements Specification

### 2.1 Filename Normalization: Retain Intermediate Numeric Tokens (`RaiImage`)
1. In `RaiImage.ImageFile.EasyFileName` / `SplitTrailingImageNumber`:
   - Only the **very last** delimiter-separated numeric token is treated as the sequence number (`ImageNumber`).
   - All preceding numeric tokens (e.g. `26` in `Nomsa-San-Diego-State-26-10.jpg`) MUST be retained as part of the PascalCase `ItemId` stem (`NomsaSanDiegoState26`).
2. Expected normalization results:
   - `Nomsa-San-Diego-State-26-1.jpg` $\rightarrow$ ItemId: `NomsaSanDiegoState26`, ImageNumber: `1` $\rightarrow$ `NomsaSanDiegoState26_001.jpg`
   - `Nomsa-San-Diego-State-26-10.jpg` $\rightarrow$ ItemId: `NomsaSanDiegoState26`, ImageNumber: `10` $\rightarrow$ `NomsaSanDiegoState26_010.jpg`
   - `Nomsa-San-Diego-State-26-100.jpg` $\rightarrow$ ItemId: `NomsaSanDiegoState26`, ImageNumber: `100` $\rightarrow$ `NomsaSanDiegoState26_100.jpg`
   - `Nomsa-San-Diego-State-26-101.jpg` $\rightarrow$ ItemId: `NomsaSanDiegoState26`, ImageNumber: `101` $\rightarrow$ `NomsaSanDiegoState26_101.jpg`
3. Single numeric token behavior:
   - A single trailing numeric token (e.g. `Nomsa-San-Diego-State-26.jpg`) continues to treat `26` as `ImageNumber`, yielding ItemId `NomsaSanDiegoState` and filename `NomsaSanDiegoState_026.jpg`.
4. Update unit test suite in `RaiImage.Tests/FilenameNormalizationTests.cs` to assert these exact transformations.

### 2.2 CLI Ergonomics & Flag Improvements (`ImgSeeder` / `iorg`)

#### A. `organize` Ergonomics
1. **Remove Mandatory `--import-id` Requirement**:
   - If `--json` or `--exif` is supplied without `--import-id`, auto-generate an ID (e.g. `Import_<UtcTimestamp>`) rather than failing.
   - If `--import-id` is explicitly passed, use it.
2. **Receipt File Output Parameter (`-o` / `--out` / `--receipt`)**:
   - Add `-o`, `--out`, `--receipt <filepath>` to `iorg organize`.
   - When present, the receipt JSON is written directly to the target file.
3. **Short-Flag Parity for Source**:
   - Accept `-s` as an alias for `--source`.

#### B. `clean` Image Number Filter (`-i` / `--image`)
1. Add optional `-i`, `--image <number>` filter to `iorg clean`:
   - Without `-i` / `--image`: `iorg clean <ItemId> ...` selects all images and derivatives under that ItemId.
   - With `-i` / `--image <number>`: `iorg clean <ItemId> -i <number> ...` filters the target list to only the specified sequence number and its derivatives:
     ```bash
     iorg clean NomsaSanDiegoState26 -i 100 -a AfricaStage -t NOMSA --force
     ```
     Deletes only `NomsaSanDiegoState26_100.jpg`, `NomsaSanDiegoState26_100_Large.jpg`, etc.
2. Safety: Retain dry-run default behavior unless `--force` is passed.

#### C. `list` Image Number Filter
1. Support `-i` / `--image <number>` on `iorg list <ItemId>` to filter listings by image number.

### 2.3 Documentation Decoupling (`ImgSeeder`)
1. **`ImgSeeder/README.md`**:
   - Remove references to `jpit` and downstream `pits seed Object` commands from the core usage example.
   - Link prominently to `GettingStarted.md`.
2. **`ImgSeeder/GettingStarted.md`**:
   - Standalone guide covering: OneDrive setup, `Amafu` & `ImgSeeder` installation, `amafu init --create-links`, `iorg -c OneDrive -a AfricaStage -h` preflight, bulk import with `-o`/`--out`, and cleanup with `-i`/`--image`.

---

## 3. Acceptance Criteria

1. **`RaiImage.Tests`**:
   - `FilenameNormalizationTests` verifies multi-numeric token preservation in stems (`Nomsa-San-Diego-State-26-10.jpg` $\rightarrow$ `NomsaSanDiegoState26` + `10`).
   - All tests pass under `dotnet test RaiImage/RaiImage.Tests/RaiImage.Tests.csproj`.
2. **`ImgSeeder.Tests`**:
   - `ImportCliTests` verifies:
     - `iorg organize --json` succeeds without `--import-id`.
     - `iorg organize -o receipt.json` writes receipt to file.
     - `iorg organize -s archive.zip` accepts short flag.
   - `CleanCliTests` verifies `iorg clean <ItemId> -i <number>` selects only matching images.
   - All tests pass under `dotnet test ImgSeeder/ImgSeeder.Tests/ImgSeeder.Tests.csproj`.
