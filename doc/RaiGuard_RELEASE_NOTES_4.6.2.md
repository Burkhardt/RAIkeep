# Release Notes: RaiGuard / rail v4.6.2

**Date:** 2026-11-05

**Author / Delivering Agent:** Codex (`7001`), RAIkeep Custodian / Provider

**Delivered Version:** v4.6.2 local candidate

**Target Consumers:** AIA (Adele / Zébio), RAIkeep CLI consumers, Engenho

**Status:** Provider implementation and verification complete — awaiting independent consumer CDAT; not published by this work

## 1. Summary

`rail check`, the implicit check form and `rail fix` now resolve every supplied
source path into one validated, deterministic file set. Repeated path options
combine with positional paths; overlapping inputs are inspected once. Invalid
or unreadable targets fail explicitly instead of silently reducing the scan.

The requested four-project AIA invocation now reports **264 inspected files**,
matching separate scans of **80 / 61 / 60 / 63** files on the same checkout.
Both local-source and packaged-candidate scans report no proven violations.
This is provider verification, not a substitute for Adele/Zébio's independent
acceptance or the compiler analyzer's project-context validation.

## 2. Resolved Change Requests (CRs)

- [CR078_AIA_to_RAIkeep_Rail_Multi_Path_Input_Completeness.md](CR078_AIA_to_RAIkeep_Rail_Multi_Path_Input_Completeness.md)
  — Accepted for implementation by the provider on 2026-11-05; candidate
  correction and verification delivered for requester evaluation. All twelve
  acceptance scenarios have provider evidence below. Consumer signoff is pending.

CR070 remains a separate accepted CR. Its rule-exemption behavior is preserved
and regression-tested; this delivery does not reopen its requirements or change
analyzer rule semantics.

## 3. Root Cause Analysis & Technical Resolution

### Root cause

The previous `PositionalArg` returned only the first positional token. Dispatch
passed a single path to `RunCheck` / `RunFix`, and an explicit `-p` / `--path`
overrode positional input. Later targets were accepted without being inspected.
The resolver also returned an empty set for missing targets, allowing an invalid
selection to look like a successful zero-file scan.

### Implementation

- `RaiGuard/rail/RailArguments.cs` parses targets and options in one pass. It
  accumulates positional and repeated path options, consumes filter values only
  as filters, supports `--`, and rejects unknown options or missing values.
- `RaiGuard/rail/SourceSelection.cs` resolves and validates the complete input set
  before analysis or edits. It reads actual directory-entry spelling to
  normalize case aliases without merging distinct files on case-sensitive Unix
  volumes. Windows path comparisons also handle drive-letter case. Results are
  sorted and deduplicated. Directory expansion excludes `bin`, `obj` and `.git`
  before descending into them; explicit single-file selection remains supported.
- `RaiGuard/rail/Program.cs` uses that shared selection for checks, implicit
  checks, fixes and dry runs. It rejects source targets combined with group-listing
  mode rather than silently discarding them. Operational failures identify the
  path on stderr and return 2. A failed check emits no overall clean-success
  message. A failed JSON check emits `[]` only, with its error on stderr.
- `RaiGuard/rail/MutationCompilation.cs` builds one semantic compilation from the
  complete source set. Source trees are reused during analysis, avoiding a second
  read of every source file. Declaration/helper and partial-exemption information
  can therefore cross target boundaries.
- A small internal filesystem boundary supports deterministic access-denial and
  later read/write-failure tests. Production execution uses the real filesystem;
  no permission changes or cloud operations are needed to test these cases.
- `RaiGuard/rail.Tests/MultiPathTests.cs` adds 30 regression cases. They share the
  existing CLI test class to serialize console/working-directory changes.

Fixes validate every target and enumerate all selected files before the first
write. A file that becomes unreadable or unwritable after validation still fails
with exit 2. If an earlier file was already modified, stderr lists it along with
the failing path. No whole-batch transactional rollback is promised by CR078.

Symbolic-link aliases are not given a new identity/deduplication contract. This
change does not add speculative source rewrites or change supported fixes.

## 4. Public Contract & API / Package Changes

```text
rail check [<path> ...] [--rule <id>] [--group <name>] [--json]
rail fix [<path> ...] [--rule <id>] [--group <name>] [--dry-run]
rail <path> ...
```

Examples:

```zsh
rail check AIA.Core AIA.Api AIA.Core.Test AIA.Api.Test
rail check src/First -p src/Second --path 'src/Third Project'
rail check -- --directory-starting-with-a-dash
rail fix src/First src/Second --rule RAI001 --dry-run
```

- No targets still means the current directory. Single-file and single-directory
  invocations remain supported. An empty readable directory reports that no C#
  source files were found and returns 0; a missing target returns 2.
- Options can appear between targets. Repeated path options add targets rather
  than overriding them. Tokens after `--` are paths, even if named `--help`,
  `--version` or `--json`. Prefix a leading-dash path with `./` when supplying it
  as a `-p` value, or put it after `--` as a positional target.
- Check exits: **0** completed with no findings; **1** completed with findings;
  **2** invalid input or incomplete inspection. Fix errors also return 2;
  successful fix/dry-run behavior remains unchanged.
- `check --json` retains the existing diagnostic-array record schema: `RuleId`,
  `Message`, `File`, `Line`, `Column`, `Severity`, `Suggestion`, `Documentation`.
  Input/inspection errors emit `[]` and exit 2. An empty array alone does not
  establish successful coverage; consumers must check the process exit status.
- Help uses the existing shared style and now advertises multi-path input,
  repeated options, `--`, deduplication and check exit codes. README examples
  describe incomplete-scan and partial-fix behavior.
- Local `RaiGuard` and `RaiGuard.Analyzer` candidate package versions are 4.6.2.
  Analyzer/core rule behavior is unchanged. The full suite is now synchronized
  to 4.6.2 following Rainer's explicit release-preparation instruction. Candidate
  package-only verification uses the local 4.6.2 feed; nothing is published.

## 5. Validation & Acceptance Evidence

### Provider test results

```zsh
dotnet test RaiGuard/RaiGuard.sln --nologo --disable-build-servers \
  -nodeReuse:false -p:UseSharedCompilation=false
```

**117 analyzer tests + 53 CLI tests passed; zero failed, zero skipped.**
The CLI total consists of 23 existing tests and 30 new cases, including theory
rows. At the initial CR078 handover, the complete umbrella/cloud-sync suite was not
rerun. Subsequent bundled CR078/CR081 preparation ran it successfully: 1,246
passed, zero failed/skipped. See RAIkeep_RELEASE_NOTES_v4.6.2.md for current evidence.

`python3 scripts/sync-cli-style.py --check` passed. Packaged redirected help was
checked for the new contract, plain output and space-based alignment.

### Acceptance-criterion evidence

| Criterion | Provider verification |
|---|---|
| AC-1 | Four directories selected; finding only in the fourth is reported; exit 1 and four-file total verified. |
| AC-2 | Two clean directories report two files; adding a finding only to the second changes the result to exit 1. |
| AC-3 | Repeated files, parent/subdirectory overlaps and normalized relative paths produce one ordered file set and no duplicate findings. Local filesystem case-alias behavior is exercised without assuming that macOS means case-insensitive. |
| AC-4 | Mixed positional inputs, repeated `-p` / `--path`, interleaved filters, spaces and flag-like targets after `--` are covered. |
| AC-5 | Missing/unsupported later targets and injected real-operation access failures return 2 with path-specific stderr. Fixes write no files when selection/validation fails. |
| AC-6 | Unknown options and missing rule/group/path values fail explicitly; JSON remains parseable and files remain unchanged. |
| AC-7 | Clean/finding multi-path JSON checks preserve the array and exact record field names without banner or ANSI noise. |
| AC-8 | Invalid later input produces `[]`, path-specific stderr and exit 2. Later inspection-read failure also produces an incomplete result rather than success. |
| AC-9 | Dry-run reports candidates across multiple targets without writes; actual fixes write each unique source once. A later write failure reports the failed path and files already changed. |
| AC-10 | Current-directory default, one-path form, implicit multi-path checks, empty directory and generated-directory exclusions are covered. Existing rules/groups tests remain green. |
| AC-11 | Cross-target receiver declarations produce the expected semantic RAI011 finding. Method exemptions and a partial-class exemption declared in another target preserve CR070 behavior. |
| AC-12 | Read-only AIA candidate scan reports 264 files; individual scans report 80, 61, 60 and 63. Packaged candidate also reports 264 with exit 0. Independent consumer rerun/signoff remains required. |

The existing semantic-reference advisory appears on stderr for both combined
and individual AIA scans:

```text
rail: inspection compilation has unresolved or invalid code; RAI011/RAI012 report only proven cases.
```

The rest of that advisory recommends compiler-analyzer project-context validation.
CR078 preserves this behavior: complete file selection does not imply complete
project/assembly reference resolution. No source file was dropped to obtain the
clean result, and this CLI scan does not claim to replace an AIA compiler build.

### Local packaging

- `RaiGuard.4.6.2.nupkg` built with `UseLocalRAIkeepSources=false`, verifying
  package-only runtime dependencies rather than relying on adjacent source repos.
- `RaiGuard.Analyzer.4.6.2.nupkg` built successfully.
- Extracted tool package reports `rail v4.6.2`; help and the four-path AIA check
  were executed directly from the extracted package without installing a tool
  globally or provisioning any machine.
- Artifact paths, hashes and scan observations are captured in
  [CR078_4.6.2_Evidence.json](verification/CR078_4.6.2_Evidence.json).

Verification ran locally on Nkosikazi/macOS. No Windows or Linux execution is
claimed; the filesystem regression also runs on the host's actual case behavior
when executed by CI or consumers on those platforms.

## 6. Upgrade & Consumption Instructions

### Independent CDAT using the local candidate

From the AIA checkout:

```zsh
cd /Users/RSB/Projects/GitHub/AIA
dotnet /Users/RSB/Projects/GitHub/RAIkeep/RaiGuard/rail/bin/Debug/net10.0/rail.dll -v
dotnet /Users/RSB/Projects/GitHub/RAIkeep/RaiGuard/rail/bin/Debug/net10.0/rail.dll \
  check AIA.Core AIA.Api AIA.Core.Test AIA.Api.Test -n
```

Expected version: `rail v4.6.2`. Expected result on the measured checkout:

```text
No proven guardrail violations found. Checked 264 files.
```

Then independently compare the union of separate scans, place a controlled
violation in a disposable later-target fixture, test JSON/error statuses, and
exercise fix/dry-run only on disposable copies. Do not add a synthetic violation
to production code merely to run the acceptance scenario.

The package-based executable is also available locally at
`/private/tmp/cr078-packaged-rail/tools/net10.0/any/rail.dll`.
Candidate packages are in `/private/tmp/raikeep-cr078-candidates/`; these temporary
paths are review artifacts, not a registry release or fleet installation.

Adele/Zébio must independently evaluate this report against
`CR078_AIA_to_RAIkeep_Rail_Multi_Path_Input_Completeness.md`, run their consumer
checks and record acceptance or rejection using the requester evaluation
template, citing **RaiGuard_RELEASE_NOTES_4.6.2.md** exactly.

**Dual-Control Handover Gate:** provider delivery stops here for consumer CDAT.
After acceptance, Rainer controls subsequent release preparation and manual
Engenho execution. No `engenho release`, provisioning, remote deployment, tag or
package publication was performed as part of this implementation.

## Bundled preparation update — 2026-11-06

CR081 is now bundled at Rainer's request. The latest prepared package feed is
`/private/tmp/raikeep-4.6.2-candidates/nuget/`; current hashes, commit identities
and package-only smoke results are in
[CR081_4.6.2_Evidence.json](verification/CR081_4.6.2_Evidence.json). The earlier
CR078 evidence receipt is retained as an explicitly labeled historical measurement.

AIA has gained files since the original 264-file measurement. The final packaged
candidate checks 279 files, matching separate counts of 84 / 67 / 62 / 66. The
source-selection contract is complete coverage of the actual checkout, not a
hardcoded count. See [RAIkeep_RELEASE_NOTES_v4.6.2.md](RAIkeep_RELEASE_NOTES_v4.6.2.md)
for the combined CDAT handover. Consumer acceptance is still pending.
