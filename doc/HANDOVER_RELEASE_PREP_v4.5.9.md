# Handover: RAIkeep v4.5.9 Release Preparation

**Target Agent:** RAIkeep Engineer (Codex Terra / GPT-6 Sol High)  
**Governing Standard:** Release Preparation Protocol & Manual Gate Boundary  
**Release Version:** `4.5.9`  
**Working Directory:** `/Users/RSB/Projects/GitHub/RAIkeep`

---

## 1. Objective & Scope

Prepare the coordinated **RAIkeep v4.5.9** release incorporating:
- **CR060**: `RaiImage` intermediate numeric token retention in stems (`NomsaSanDiegoState26_010.jpg`), `iorg organize` receipt file output (`-o`/`--out`) and `-s` source alias, `iorg clean` / `list` image number filter (`-i`/`--image`), and `ImgSeeder/GettingStarted.md`.
- **Option B Harmonization**: All child repositories standardized with clean single-link release history and dual-mode CLI installation commands.

> [!IMPORTANT]
> **MANUAL GATE BOUNDARY:** Your job is **Preparation and Preflight Validation only**.  
> Do **NOT** run `scripts/release-chain.sh`, do **NOT** push git tags, and do **NOT** publish packages. Dr. Rainer Burkhardt (`RAI`) alone executes `release-chain.sh 4.5.9`.

---

## 2. Step-by-Step Release Preparation Sequence

Execute each step in sequence:

### Step 1: Activate Release Virtual Environment
```bash
source ~/.venvs/raikeep-release/bin/activate
```

### Step 2: Bump Versions Across All Platform Targets
Run the bumper engine to deterministically synchronize all `.csproj` files, manifests, code constants, and release notes:
```bash
python3 scripts/bump-version.py 4.5.9
```

### Step 3: Run Isolated Release Tools Unit Tests
Verify bumping regexes and temporary directory isolations pass:
```bash
python3 scripts/test-release-tools.py
```

### Step 4: Verify Markdown Link Integrity
Ensure all tracked Markdown document links use absolute destinations:
```bash
bash scripts/check-markdown-document-links.sh
```
*(If any relative links are reported, update them to use `https://github.com/Burkhardt/RAIkeep/blob/main/...` absolute URLs).*

### Step 5: Execute Master Preflight Validation Gate
Run the complete 119-check release validator:
```bash
python3 scripts/validate-release.py 4.5.9
```
Verify that all validation checks pass 100% green:
- Git cleanliness and all submodules on `main`
- Exact version matching across all manifests and `.csproj` files
- Cross-runtime CLI parity (`pits` vs `jpit` list and help screens)
- `JsonPit.Python` tests passing

### Step 6: Commit Prepared Release Artifacts
Commit version bumps and manifest changes across all submodules and root with clean commit messages strictly $\le 20$ characters (e.g., `prepare 4.5.9`).

### Step 7: Final Handover
Report preflight pass status (checks count and outcome) and confirm readiness for Rainer to execute:
```bash
scripts/release-chain.sh 4.5.9
```
