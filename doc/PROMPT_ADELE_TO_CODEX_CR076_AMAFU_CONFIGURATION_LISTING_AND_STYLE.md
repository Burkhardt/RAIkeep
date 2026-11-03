# Dispatch Prompt: Adele (AIA PM) to Codex (RAIkeep Agent) — CR076

```text
You are Codex, Lead Systems Architect and Custodian for RAIkeep (Burkhardt/RAIkeep).

Adele, Product Manager for AIA, has ratified Change Request CR076 on behalf of AIA Platform Governance, Engenho, and Dr. Rainer Burkhardt (RAI).

Authoritative Specification:
doc/CR076_AIA_to_RAIkeep_Amafu_Configuration_Listing_and_Provider_Style.md
(Parent: CR044, CR051, CR057, CR058)

### Mission Objective:
Implement Deliverables in RAIkeep (Amafu and CliHelpStyle), targeting Release v4.5.17:

1. Public Command Syntax & Contract (`amafu list`):
   - amafu list temp                 -> Raw expanded absolute path + \n (exit 0)
   - amafu list backup               -> Raw expanded absolute path + \n (exit 0)
   - amafu list order <provider>     -> 1-based position or "0\n" sentinel if absent (exit 0)
   - amafu list order all            -> Badged provider names in order with 2 leading spaces (exit 0)
   - amafu list cloud <provider>     -> Raw expanded absolute directory path + \n (exit 0)
   - amafu list cloud all            -> Exact tab-aligned table with badged names and quoted paths (exit 0)
   - amafu list observer <name>      -> Raw configured SSH target string + \n (exit 0)
   - amafu list observer all         -> Space-aligned table: "  {name}:  {target}\n" (exit 0)

2. Strict Output Separation:
   - Script Mode (single scalar lookups):
     * Pure raw value + terminating \n on stdout.
     * ZERO ANSI escape codes, zero glyphs, zero quotes, zero headers, zero trailing spaces.
     * All diagnostics/errors strictly on stderr.
   - Interactive Mode (collection lookups):
     * "order all": 2 leading spaces, badged names separated by single space.
     * "cloud all": Exact format "\t{badge} {provider}\t\t\"{path}\"\n" (tab-indented, two tabs separating name and quoted path).
     * "observer all": Space-padded table alignment.

3. Provider Badges & Visual Styling:
   - Match jpit / CliHelpStyle standard:
     * OneDrive: 󰰕 (U+F0C15)
     * Dropbox: 󰯴 (U+F0BF4)
     * GoogleDrive: 󰯽 (U+F0BFD)
     * ICloudDrive: 󰰃 (U+F0C03)
   - Color palette cycling: 96, 92, 94, 91, 35, 95, 36, 34.
   - Auto-strip ANSI escapes if stdout is redirected or NO_COLOR / TERM=dumb is set.
   - Run `python3 scripts/sync-cli-style.py --check` and ensure style parity.

4. Syntax Rejections & Contextual Help:
   - Reject "amafu list all" with exit code 2. ("all" only valid under order, cloud, observer).
   - Bare "amafu list" prints usage to stderr with exit code 2.
   - Dedicated contextual help for each selector: "amafu list temp -h", "amafu list order -h", etc.
   - Help flags must never fail even if ~/.config/RAIkeep.json5 is missing.
   - Remove the obsolete "Configuration" row from "amafu -h".

5. Exit Codes:
   - 0: Success / Help display / Unlisted order query (sentinel "0\n").
   - 2: CLI syntax error (invalid sub-command, missing argument, bare list, "list all").
   - 4: Configuration error (missing config file, corrupt JSON5, named provider/observer not found).

6. Non-Destructive Invariant:
   - Strictly READ-ONLY. Zero config modifications, zero filesystem writes, zero network/SSH calls.

7. Acceptance Criteria & Test Suite:
   - Implement unit and integration tests covering AC-1 through AC-10 in CR076.
   - Run `dotnet test RAIkeep.slnx` before handing over.
```
