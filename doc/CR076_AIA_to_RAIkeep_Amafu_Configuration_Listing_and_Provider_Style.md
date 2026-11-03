# CR076: Amafu Configuration Listing and Provider Presentation

> **Naming Schema:** `CR076_AIA_to_RAIkeep_Amafu_Configuration_Listing_and_Provider_Style.md`  
> **Parent CR:** `CR044_AIA_and_jsonpit_to_RAIkeep_Auto-Detect-Cloud-Drives-and-Init-Config.md`, `CR051_RAI_to_RAIkeep_Multiple-Cloud-Accounts-and-Named-Shortcuts.md`, `CR057_AIA_and_jsonpit_to_RAIkeep_Amafu-Shortcut-First-Explicit-Cloud-and-Umbrella-Consolidation.md`, `CR058_AIA_to_RAIkeep_Conditional-WWWA-Help-Screen-Parity-in-pits-and-jpit.md`  
> **Immutability Rule:** The provider agent must NEVER rename or modify this document filename.

**Date:** 2026-11-02  
**Requesting Agent / PM:** Adele (`7010`, PM AIA Platform) on behalf of AIA Platform, Engenho, and Dr. Rainer Burkhardt (RAI)  
**Target Provider / Repo:** Codex (`7001`, Custodian & Systems Architect) / `Burkhardt/RAIkeep`  
**Status:** Ratified & Dispatched to RAIkeep  
**Target Release:** RAIkeep `v4.5.17`

---

## 1. Objective & Context

### The Operator & Consumer Problem
Host configuration in `~/.config/RAIkeep.json5` defines crucial execution parameters across the fleet: `TempDir`, `LocalBackupDir`, `DefaultCloudOrder`, `Cloud` directory paths, and `Observers` SSH targets.
Currently:
1. Inspecting these settings requires operators and scripting harnesses to open, parse, or query the raw JSON5 file using external tools.
2. Shell scripts in AIA and Engenho need clean, undecorated scalar access to configured paths (e.g. `$(amafu list cloud OneDrive)`) without ANSI codes, banners, or trailing labels.
3. Interactive terminal users need human-readable, beautifully styled collection tables matching the established `jpit` / `CliHelpStyle` visual standard, with authentic cloud provider glyphs and exact tabular alignment.
4. Top-level `amafu list all` was a premature and unstructured dump that risked leaking unrelated configuration fields.

### Ratified Scope
AIA formally adopts and ratifies CR076 with the following key design ratifications:
- **Strictly Read-Only:** No network calls, no directory creation, no writes, no probes, no SSH connections.
- **Clean Scalar Output:** When querying a single item, stdout receives *only* the raw expanded value and a single terminating newline. Exit code 0. Zero banner, zero decoration, zero ANSI.
- **Human-Readable Collection Tables:** For collection lookups (`order all`, `cloud all`, `observer all`), formatted with provider glyphs, color palettes, and the explicit tabbed alignment requested by RAI.
- **Specific Help:** Full contextual help for each sub-selector (`amafu list <selector> -h`).

---

## 2. Public Command Contract & Syntax

```text
amafu list temp
amafu list backup
amafu list order <provider|all>
amafu list cloud <provider|all>
amafu list observer <name|all>
```

| Selector | Configuration Key | Output Format | Exit Code |
| :--- | :--- | :--- | :---: |
| `temp` | `TempDir` | Expanded absolute filesystem path + `\n` | `0` |
| `backup` | `LocalBackupDir` | Expanded absolute filesystem path + `\n` | `0` |
| `order <provider>` | `DefaultCloudOrder` | 1-based integer position (`1`, `2`, etc.), or `0` if not in order array | `0` |
| `order all` | `DefaultCloudOrder` | All badged provider names on one line in configured order | `0` |
| `cloud <provider>` | `Cloud[provider]` | Expanded absolute directory path + `\n` | `0` |
| `cloud all` | `Cloud` | Tab-aligned table with provider glyphs, names, and quoted paths | `0` |
| `observer <name>` | `Observers[name]` | Configured SSH target string (e.g. `rsb@Mzansi`) + `\n` | `0` |
| `observer all` | `Observers` | Space-aligned table of observer names and SSH targets | `0` |

### Prohibited / Replaced Syntax:
- **`amafu list all` is strictly rejected (Exit Code 2).** `all` is only valid as the sub-argument to `order`, `cloud`, or `observer`.
- Bare `amafu list` without arguments displays usage guidance and available selectors (Exit Code 2).

---

## 3. Formatting & Alignment Rules

### 3.1 Scalar Queries (Script Mode)
- **Output:** Exactly `{value}\n`.
- **Zero ANSI:** No escape codes, no bold, no colors, no headers, no quotes, no badges.
- **Path Expansion:** `~` expanded to user home; absolute path with trailing directory separator according to host OS conventions.
- **Absent Order Sentinel:** `amafu list order <provider>` prints `0\n` with exit code `0` when the provider is not listed in `DefaultCloudOrder` (even if configured in `Cloud`).

### 3.2 Collection Output (Interactive Human Mode)
1. **`amafu list order all`**:
   - Leading 2 spaces, badged provider names separated by a single space:
     `  󰰕 OneDrive 󰯴 Dropbox 󰯽 GoogleDrive 󰰃 ICloudDrive`
2. **`amafu list cloud all` (Explicit Tab Exception)**:
   - **RAI review amendment, 2026-11-02:** replaces the original one-line table.
   - Each entry follows `{badge} {provider}\n\t"{path}"\n`.
   - The glyph/name starts at the left margin with no leading whitespace or colon.
   - The double-quoted path follows on its own line with exactly one leading tab.
     ```text
     󰰕 OneDrive
     \t"/Users/RSB/Library/CloudStorage/OneDrive/OneDriveData/"
     󰯴 Dropbox
     \t"/Users/RSB/Library/CloudStorage/Dropbox/DropboxData/"
     󰯽 GoogleDrive
     \t"/Users/Shared/ServerData/GDriveData/"
     󰰃 ICloudDrive
     \t"/Users/RSB/Library/Mobile Documents/com~apple~CloudDocs/ICloudDriveData/"
     ```
3. **`amafu list observer all`**:
   - Space-padded alignment:
     ```text
       Mzansi:  rsb@Mzansi
       Ingwe:   rsb@ingwe
       Mdlaka:  umshadisi@Mdlaka
     ```

### 3.3 Provider Badges & Styling Parity
- **Glyphs:** Must match `jpit` / `CliHelpStyle`:
  - 󰰕 OneDrive (`U+F0C15`)
  - 󰯴 Dropbox (`U+F0BF4`)
  - 󰯽 GoogleDrive (`U+F0BFD`)
  - 󰰃 ICloudDrive (`U+F0C03`)
- **Palette:** Repeating ANSI palette: `96`, `92`, `94`, `91`, `35`, `95`, `36`, `34`.
- **Environment Respect:** Automatically strip ANSI escapes if stdout is redirected or `NO_COLOR` / `TERM=dumb` is set. Collection layout and unicode glyphs remain intact.

---

## 4. Contextual Help & Exit Codes

### Contextual Help
- Every selector supports specific help: `amafu list temp -h`, `amafu list order -h`, `amafu list cloud -h`, `amafu list observer -h`.
- Help flags must never fail if `~/.config/RAIkeep.json5` is missing.
- `amafu list order -h` must explicitly document the 1-based indexing and the `0` sentinel for unlisted providers.
- Remove the obsolete `Configuration` row from the general `amafu -h` screen.

### Ratified Exit Codes
- **`0`**: Successful command execution or help display (including `0\n` for unlisted order queries).
- **`2`**: Command-line syntax error (invalid selector, missing required argument, extra arguments).
- **`4`**: Configuration failure (missing configuration file, malformed JSON5, or named provider/observer not found).

---

## 5. Acceptance Test Criteria

| Test ID | Command | Expected Result |
| :--- | :--- | :--- |
| **AC-1** | `amafu list cloud OneDrive` | Raw expanded path ending with `/` + `\n`, exit code 0. Zero ANSI. |
| **AC-2** | `amafu list order OneDrive` | `1\n`, exit code 0. |
| **AC-3** | `amafu list order NonExistent` | `0\n`, exit code 0. |
| **AC-4** | `amafu list observer Mzansi` | `rsb@Mzansi\n`, exit code 0. |
| **AC-5** | `amafu list all` | Fails with exit code 2 and helpful usage guidance on stderr. |
| **AC-6** | `amafu list cloud all` | Formatted table matching `{badge} {name}\n\t"{path}"\n` with exactly one path-indent tab. |
| **AC-7** | `amafu list order all` | Badged provider names in `DefaultCloudOrder` sequence with leading 2 spaces. |
| **AC-8** | `amafu list order -h` | Context-specific help explaining 1-based order and `0` sentinel, even if config is missing. |
| **AC-9** | Non-existent observer lookup | Fails with exit code 4 and error message on stderr; stdout is empty. |
| **AC-10** | Non-destructive verification | Configuration file modification time and bytes remain byte-identical after queries. |

---

## 6. Implementation & Package Target

- **Component:** `Amafu` CLI and standalone formatter.
- **Target Release:** RAIkeep `v4.5.17`.
- **Sync Requirement:** Pass `python3 scripts/sync-cli-style.py --check`.

— Ratified on 2026-11-02 by Adele (`7010`, PM AIA Platform)
