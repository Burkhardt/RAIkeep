# Handover: CR060 — Image Stem Numeric Tokens, Receipt Redirection, & -i Image Filter

**Target Agent:** RAIkeep Engineer (Codex / Claude)
**Governing Standard:** Adele Behavioral Codex Rule 6 (Targeted-First Testing)
**Specification:** `doc/CR060_AfricaStage_to_RAIkeep_Image-Stem-Numeric-Tokens-and-Iorg-Ergonomics.md`
**Reference Guide:** `ImgSeeder/GettingStarted.md` (already authored in working tree)

---

## 1. Context & Objectives

AfricaStage testing on Mdlaka identified several functional and ergonomic improvements needed in `RaiImage` and `ImgSeeder` (`iorg`):
1. **Filename Stem Collision in `RaiImage`**: Intermediate numbers (e.g. `26` in `Nomsa-San-Diego-State-26-10.jpg`) were discarded from the stem (`NomsaSanDiegoState`) instead of preserved (`NomsaSanDiegoState26`), dropping event/edition context and causing preflight collisions.
2. **`iorg organize` Receipt Ergonomics**:
   - Dropping the mandatory `--import-id` requirement when `--json` is supplied (auto-generate an ID if omitted).
   - Adding `-o`, `--out`, `--receipt <file>` to write the receipt JSON directly to disk.
   - Adding `-s` as an accepted alias for `--source`.
3. **`iorg clean` & `iorg list` Image Number Filter (`-i` / `--image`)**:
   - Allowing operators to clean or list a specific image number under an ItemId (e.g. `iorg clean NomsaSanDiegoState26 -i 100 -a AfricaStage -t NOMSA --force` deletes only `_100.jpg`, `_100_Large.jpg`, etc., rather than the entire 193-photo batch).
4. **Decoupling Documentation**: Removing confusing `jpit` and downstream `pits seed Object` commands from `ImgSeeder/README.md` and pointing to `GettingStarted.md`.

---

## 2. Step-by-Step Implementation Instructions

### Step 1: Fix `RaiImage` Filename Normalization (`ImageFile.cs`)

1. In `RaiImage/ImageFile.cs`, update `SplitTrailingImageNumber(string sourceName)`:
   - Only the **very last** delimiter-separated numeric token is the sequence number (`ImageNumber`).
   - Preceding numeric tokens (e.g. `26` in `Nomsa-San-Diego-State-26-10.jpg`) must remain in `itemName` so they become part of the PascalCase `ItemId` (`NomsaSanDiegoState26`).
   - Update regex to split only the final delimiter-separated number:
     ```csharp
     var match = Regex.Match(sourceName ?? string.Empty, @"^(?<itemName>.*?)[-_](?<imageNumber>[0-9]+)$");
     ```
2. In `RaiImage/RaiImage.Tests/FilenameNormalizationTests.cs`, add test cases asserting:
   - `Nomsa-San-Diego-State-26-1.jpg` $\rightarrow$ ItemId: `NomsaSanDiegoState26`, ImageNumber: `1`, Name: `NomsaSanDiegoState26_001.jpg`
   - `Nomsa-San-Diego-State-26-10.jpg` $\rightarrow$ ItemId: `NomsaSanDiegoState26`, ImageNumber: `10`, Name: `NomsaSanDiegoState26_010.jpg`
   - `Nomsa-San-Diego-State-26-100.jpg` $\rightarrow$ ItemId: `NomsaSanDiegoState26`, ImageNumber: `100`, Name: `NomsaSanDiegoState26_100.jpg`
   - `Nomsa-San-Diego-State-26-101.jpg` $\rightarrow$ ItemId: `NomsaSanDiegoState26`, ImageNumber: `101`, Name: `NomsaSanDiegoState26_101.jpg`
3. Targeted test run:
   ```bash
   dotnet test RaiImage/RaiImage.Tests/RaiImage.Tests.csproj --filter "FullyQualifiedName~FilenameNormalization"
   ```

---

### Step 2: Update `ImgSeeder` Organize Command (`Program.cs`)

1. **Remove mandatory `--import-id` check**:
   - In `RunOrganizeCommand`, remove `if (json && importId is null) throw ...`.
   - If `importId` is null/empty when `--json` is active, synthesize: `importId = $"Import_{DateTimeOffset.UtcNow:yyyyMMdd_HHmmss}";`.
2. **Add `-o` / `--out` / `--receipt <file>`**:
   - Add `"-o"`, `"--out"`, `"--receipt"` to `valueOptions` in `RunOrganizeCommand`.
   - If specified, write the serialized receipt JSON directly to that file path (creating directories if needed).
3. **Add `-s` alias for `--source`**:
   - Add `"-s"` to `valueOptions` and resolve via `ParamValue(args, "--source", "-s")`.
4. **Update `organize` help text**:
   - Document `(-s|--source)`, `[-o|--out <file>]`, and optional `[--import-id <id>]`.

---

### Step 3: Add `-i` / `--image` Filter to `clean` and `list` (`Program.cs`)

1. In `RunCleanCommand`:
   - Add `"-i"`, `"--image"` to `valueOptions`.
   - Retrieve optional filter: `var imageNumber = OptionalPositiveLimit(args, "-i", "--image");`.
   - Pass `imageNumber` into `ImageOrganizer.CleanItem(...)`.
2. In `ImageOrganizer.CleanItem(...)`:
   - Accept optional `int? imageNumber = null` parameter.
   - If `imageNumber` is provided, filter `files` to only include files matching that image number (e.g. where `new ImageFile(file.FullName).ImageNumber == imageNumber`).
3. In `RunListCommand`:
   - Add `"-i"`, `"--image"` to `valueOptions`.
   - If specified, filter listed files by `ImageNumber`.
4. Update `clean` and `list` help text:
   - `iorg clean <ItemId> [-i|--image <nr>] ((-r|--root) <dir>|(-a|--app) <dir>) [--force] [options]`
   - `iorg list <FileNamePattern> [-i|--image <nr>] ...`
5. In `ImgSeeder/ImgSeeder.Tests/`:
   - Add unit test verifying `clean <ItemId> -i 100` deletes only image 100 files.
   - Add unit test verifying `organize -o receipt.json` writes receipt to file.
   - Add unit test verifying `organize -s archive.zip` parses correctly.
6. Targeted test run:
   ```bash
   dotnet test ImgSeeder/ImgSeeder.Tests/ImgSeeder.Tests.csproj
   ```

---

### Step 4: Documentation Decoupling & GettingStarted.md

1. In `ImgSeeder/README.md`:
   - Remove lines 59–68 (`pits seed Object ...` and `jpit seed Object ...`).
   - Replace with pure ImageTree verification using `jq` and `iorg list`.
   - Add link: `For an end-to-end walkthrough, see [GettingStarted.md](GettingStarted.md).`
2. `ImgSeeder/GettingStarted.md` is already authored in the working tree. Stage it.

---

### Step 5: Commit & Push

Follow strict message length $\le 20$ chars:
```bash
# RaiImage
git -C RaiImage add -A
git -C RaiImage commit -m "fix stem numbers"

# ImgSeeder
git -C ImgSeeder add -A
git -C ImgSeeder commit -m "iorg ergonomics"

# RAIkeep Root
git add doc/CR060_AfricaStage_to_RAIkeep_Image-Stem-Numeric-Tokens-and-Iorg-Ergonomics.md ImgSeeder RaiImage
git commit -m "cr059 iorg stem fix"

# Push
git -C RaiImage push origin main
git -C ImgSeeder push origin main
git push origin main
```

---

## 3. Strict Testing Directive

Per Rule 6: **Do NOT run `validate-release.py` or whole-solution tests.** Run only the targeted test commands in Step 1 and Step 3.
