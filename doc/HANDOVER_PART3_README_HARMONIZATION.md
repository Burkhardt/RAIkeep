# Handover: Part 3 — Finalize RAIkeep README Harmonization & Clean Push

**Target Agent:** RAIkeep Engineer (Codex / Claude)
**Governing Standard:** Adele Behavioral Codex Rule 6 (Targeted-First Testing / Zero Tests for Markdown Changes)
**Primary Reference:** `Amafu/README.md`, `OsLib/README.md`, and `JsonPit/README.md` (Option B reference implementations)

---

## 1. Context & Scope

`OsLib` (`2b19474`) and `JsonPit` (`c7e513d`) are committed and pushed.
This final Part 3 completes the Option B harmonization across all remaining repositories:
1. **Commit already-prepared CLIs:** `PitSeeder`, `RaidSeeder`, `RaiGuard`.
2. **Harmonize & commit `ImgSeeder` (`iorg`):** Option B archive link + dual CLI install modes.
3. **Harmonize & commit Libraries:** `RaiUtils`, `RaiImage`, `RaiDiagram` (collapse dozens of legacy version headers into a single Option B archive link + NuGet installation block).
4. **Commit root updates & push:** `scripts/validate-release.py`, update submodule pointers in root RAIkeep, and push `origin/main`.

---

## 2. STRICT OPERATIONAL CONSTRAINTS

> [!IMPORTANT]
> 1. **ZERO TEST SUITE RUNS**: Do **NOT** run `dotnet test`, `pytest`, or `scripts/validate-release.py`. Pure markdown/doc edits do not affect binaries.
> 2. **COMMIT MESSAGE LENGTH**: Commit messages must be strictly $\le 20$ characters, no prefixes (e.g. `update readme`, `clean doc`, `harmonize readmes`).

---

## 3. Step-by-Step Instructions

### Step 1: Commit Already-Prepared CLIs & JsonPit

The working tree already contains Option B updates for `PitSeeder`, `RaidSeeder`, and `RaiGuard`:

```bash
# 1. PitSeeder (README.md is already staged/modified)
git -C PitSeeder add README.md
git -C PitSeeder commit -m "update readme"

# 2. RaidSeeder (README.md is already modified)
git -C RaidSeeder add README.md
git -C RaidSeeder commit -m "update readme"

# 3. RaiGuard (README.md is already modified)
git -C RaiGuard add README.md
git -C RaiGuard commit -m "update readme"

# 4. JsonPit (CURRENT_STATUS.md link update)
git -C JsonPit add CURRENT_STATUS.md
git -C JsonPit commit -m "update doc links"
```

---

### Step 2: Harmonize `ImgSeeder/README.md` (CLI `iorg`)

In `ImgSeeder/README.md`:
1. Remove all `<details>` and `<summary>` tags around `Previous Versions`.
2. Format `## Previous Versions`:
   ```markdown
   ## Previous Versions

   For release notes and changelogs of earlier releases, see the [ImgSeeder 4.x Release Notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/ImgSeeder_RELEASE_NOTES_4.x.md).
   ```
3. Add or replace `## Installation` with the standard dual-mode CLI instructions:
   ```markdown
   ## Installation

   ### .NET global tool

   ```bash
   dotnet tool install --global ImgSeeder
   ```

   To update:

   ```bash
   dotnet tool update --global ImgSeeder
   ```

   *(Requires `~/.dotnet/tools` on your PATH.)*

   ### .NET tool in `/usr/local/bin` (Recommended for macOS & Linux)

   Install directly to `/usr/local/bin` so no `$PATH` modification is needed:

   ```bash
   sudo dotnet tool install ImgSeeder --tool-path /usr/local/bin
   ```

   To update:

   ```bash
   sudo dotnet tool update ImgSeeder --tool-path /usr/local/bin
   ```

   `sudo` is needed to write to `/usr/local/bin` during installation and updates. Running `iorg` does not require it.
   ```
4. Commit:
   ```bash
   git -C ImgSeeder add README.md
   git -C ImgSeeder commit -m "update readme"
   ```

---

### Step 3: Harmonize Libraries (`RaiUtils`, `RaiImage`, `RaiDiagram`)

Each library currently contains dozens of historical version headers (`## 4.5.7`, `## 4.5.6`, down to `## 4.2.3`).
Adopt Option B matching `OsLib/README.md`: keep only `## 4.5.8`, add `## Previous Versions`, and add `## Installation` (NuGet).

#### A. `RaiUtils/README.md`
Replace the entire top version block with:
```markdown
# RaiUtils

## 4.5.8

Coordinated 4.5.8 release; public behavior is aligned with the synchronized platform.

Latest release notes: [RaiUtils 4.5.8 release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiUtils_RELEASE_NOTES_4.x.md#458).

## Previous Versions

For release notes and changelogs of earlier releases, see the [RaiUtils 4.x Release Notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiUtils_RELEASE_NOTES_4.x.md).

## Installation

### .NET CLI

```bash
dotnet add package RaiUtils --version 4.5.8
```

### PackageReference

```xml
<PackageReference Include="RaiUtils" Version="4.5.8" />
```
```
(Remove all older version sections `## 4.5.7` through `## 4.2.3`).
Commit:
```bash
git -C RaiUtils add README.md
git -C RaiUtils commit -m "update readme"
```

#### B. `RaiImage/README.md`
Replace the top version block with:
```markdown
# RaiImage

## 4.5.8

Coordinated 4.5.8 release; public behavior is aligned with the synchronized platform.

Latest release notes: [RaiImage 4.5.8 release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiImage_RELEASE_NOTES_4.x.md#458).

## Previous Versions

For release notes and changelogs of earlier releases, see the [RaiImage 4.x Release Notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiImage_RELEASE_NOTES_4.x.md).

## Installation

### .NET CLI

```bash
dotnet add package RaiImage --version 4.5.8
```

### PackageReference

```xml
<PackageReference Include="RaiImage" Version="4.5.8" />
```
```
(Remove all older version sections `## 4.5.7` through `## 4.2.3`).
Also stage `BugB_Verification_StillOpen_3.8.14_Handoff.md` if modified:
```bash
git -C RaiImage add README.md BugB_Verification_StillOpen_3.8.14_Handoff.md
git -C RaiImage commit -m "update readme"
```

#### C. `RaiDiagram/README.md`
Replace the top version block with:
```markdown
# RaiDiagram

## 4.5.8

Coordinated 4.5.8 release; public behavior is aligned with the synchronized platform.

Latest release notes: [RaiDiagram 4.5.8 release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiDiagram_RELEASE_NOTES_4.x.md#458).

## Previous Versions

For release notes and changelogs of earlier releases, see the [RaiDiagram 4.x Release Notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiDiagram_RELEASE_NOTES_4.x.md).

## Installation

### .NET CLI

```bash
dotnet add package RaiDiagram --version 4.5.8
```

### PackageReference

```xml
<PackageReference Include="RaiDiagram" Version="4.5.8" />
```
```
(Remove all older version sections `## 4.5.7` through `## 4.2.3`).
Commit:
```bash
git -C RaiDiagram add README.md
git -C RaiDiagram commit -m "update readme"
```

---

### Step 4: Commit Root RAIkeep Validator, Submodules, & Push

1. Commit validator build isolation fix:
   ```bash
   git add scripts/validate-release.py
   git commit -m "improve validator"
   ```

2. Stage all submodule pointers in root RAIkeep:
   ```bash
   git add PitSeeder RaidSeeder RaiGuard ImgSeeder RaiUtils RaiImage RaiDiagram JsonPit OsLib
   git commit -m "harmonize readmes"
   ```

3. Push all submodules and root repository to `origin/main`:
   ```bash
   for d in PitSeeder RaidSeeder RaiGuard ImgSeeder RaiUtils RaiImage RaiDiagram JsonPit OsLib; do
     git -C $d push origin main
   done
   git push origin main
   ```

---

## 4. Verification

Confirm clean status across all repos:
```bash
git status
for d in PitSeeder RaidSeeder RaiGuard ImgSeeder RaiUtils RaiImage RaiDiagram JsonPit OsLib; do
  git -C $d status -s
done
```
All trees must be clean and up-to-date with `origin/main`.
**Reminder:** Do not run test suites or release validator.
