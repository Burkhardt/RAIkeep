# CR078: AIA to RAIkeep — rail Must Inspect Every Supplied Source Path

> **Document Path:** `doc/CR078_AIA_to_RAIkeep_Rail_Multi_Path_Input_Completeness.md`  
> **Status:** **Ratified & Dispatched to RAIkeep (Ready for Provider Implementation)**  
> **Date:** 2026-11-05  
> **Requesting Agent / PM:** Adele (`7010`, Product Manager, AIA Platform) / Zébio (`7011`, API & Storage Lead)  
> **Target Provider / Repo:** Codex (`7001`, Custodian & Systems Architect) / `Burkhardt/RAIkeep` (`RaiGuard / rail`)  
> **Parent CR:** None — independent CLI correctness defect discovered during CR070 consumer verification  
> **Related CR:** [`CR070_AIA_to_RAIkeep_RAI007-Test-Run-Switches-and-RAI011-RAI015-Subject-Sites.md`](CR070_AIA_to_RAIkeep_RAI007-Test-Run-Switches-and-RAI011-RAI015-Subject-Sites.md)  
> **Target Version:** RAIkeep `v4.6.2`  
> **Immutability Rule:** The provider agent must NEVER rename or modify this document filename. Provider release notes must cite this exact filename.

---

## 1. Objective & Context

Ensure a successful `rail check` represents every source path supplied by the
caller. Silently ignoring later arguments can produce a misleading clean result
for an incomplete scan.

Zébio reported this invocation against AIA:

```zsh
rail check AIA.Core AIA.Api AIA.Core.Test AIA.Api.Test
```

Observed output:

```text
No proven guardrail violations found. Checked 80 files.
```

His separate invocations inspected 80 / 61 / 60 / 63 files: 264 in total. Each
individual scan was clean, so this report does not dispute that measured
baseline. It identifies a coverage defect in the combined invocation. Counts
are observations of that checkout, not constants to hardcode in tests.

Provider source inspection confirmed the cause in `RaiGuard/rail/Program.cs`:
`PositionalArg` returns the first positional token, and dispatch passes a single
path to `RunCheck` or `RunFix`. Remaining positional inputs are not rejected.
An explicit `-p` / `--path` also takes precedence over positional input instead
of combining the requested targets. `ResolveSourceFiles` can return an empty
set for an invalid path, which currently permits a successful zero-file result.

This is separate from the earlier stale-binary observation: Zébio verified that
`rail` 4.6.1 honors the CR070 rule exemption. No exemption or analyzer-rule change
is requested here.

## 2. Desired Behavior & Constraints

### 2.1 Complete, explicit target selection

Proposed public forms:

```text
rail check [<path> ...] [--rule <id>] [--group <name>] [--json]
rail fix [<path> ...] [--rule <id>] [--group <name>] [--dry-run]
```

- Accept one or more source files or directories. With no supplied paths, keep
  the current-directory default.
- Support repeated `-p <path>` / `--path <path>` and combine them with positional
  paths. Every supplied target participates; no option silently overrides one.
- Parse values of `--rule`, `--group` and path options as their values, never as
  source targets. Preserve documented aliases and allow options between targets.
- Support `--` to terminate option parsing so a path beginning with `-` can be
  supplied. Preserve shell-quoted paths containing spaces.
- Apply the same complete-input behavior to the existing implicit check form
  (`rail <path> ...`). `rules` and `groups` retain their own argument contracts.

### 2.2 Resolve once, inspect each file once

- Expand all directories using the existing C# source selection and generated
  `bin`, `obj` and `.git` exclusions, with platform-correct path handling.
- Normalize file paths and deduplicate repeated targets and overlapping directory
  roots using filesystem-appropriate case comparison. Avoid unconditional
  lowercasing on case-sensitive filesystems. Symbolic-link alias identity is
  outside this proposal; do not introduce new link-following behavior.
- Produce a deterministic unique file set and construct semantic analysis from
  the combined set, rather than issuing isolated per-directory checks.
- `Checked N files` must count the complete unique set actually inspected.
- Preserve `check` as read-only. Preserve existing rule/group filtering,
  exemptions and diagnostic semantics.

### 2.3 Reject incomplete or invalid input honestly

- Validate all supplied targets before analysis or fixes. Missing paths,
  unsupported explicitly supplied files, unreadable targets and enumeration
  failures must identify the offending path and return a nonzero result.
- Reject unknown options and missing option values rather than silently ignoring
  them. A supplied option must never cause an intended target to disappear.
- Proposed exit contract for `check`: **0** = completed scan with no findings;
  **1** = completed scan with findings; **2** = invalid input or incomplete scan.
  Runtime inspection failures must also prevent a clean success result.
- An existing readable directory containing no eligible C# sources is not a
  missing path. It may complete with an explicit zero-file message; it must not
  claim that source files were inspected.
- If an input fails, do not print an overall clean-success message. If a later
  read fails after validation, report the failure and incomplete scan explicitly.

### 2.4 Multi-path fixes must have equally explicit scope

- `fix` and `fix --dry-run` must use the same complete, deduplicated target set.
- Validate and enumerate every requested target before the first source edit;
  an invalid target discovered at this stage must leave all source files intact.
- Preserve current supported transformations and dry-run behavior. Do not add
  speculative fixes or broaden which rules can rewrite source.
- A later execution failure returns nonzero and reports affected files. This
  proposal does not promise transactional rollback of an entire multi-file fix.

### 2.5 Output and documentation

- Preserve the `check --json` diagnostic-array schema. Write only JSON to stdout;
  operational errors and incomplete-scan diagnostics go to stderr. On input
  validation failure, emit `[]` with exit code 2; callers must inspect the exit
  code, not interpret an empty array alone as successful coverage.
- Update help and examples to advertise multi-path selection, repeated path
  options, overlap deduplication, and error/exit behavior. Follow `doc/cli-style.md`.
- Do not change successful single-path behavior, rule IDs, rule exemptions,
  release orchestration or fleet provisioning as part of this correction.

## 3. Suggested Acceptance Tests

Use small temporary fixtures with exact expected paths and counts. Include a
known violation only in a later target so checking the first alone cannot pass.

| ID | Scenario | Required result |
|---|---|---|
| AC-1 | Four directories; only the fourth contains a known violation | Every directory inspected; later violation returned; exit 1; correct total count |
| AC-2 | Two clean directories, then repeat with a violation only in the second | Combined clean count first; later finding and exit 1 second |
| AC-3 | Mix individual `.cs` files, directories, repeated targets and overlapping roots | Each normalized source file inspected once; no duplicate findings; stable ordering |
| AC-4 | Positional targets mixed with repeated `-p` / `--path`, interleaved filters, quoted spaces, and a leading-dash path after `--` | All intended paths selected; option values never treated as paths; filters preserved |
| AC-5 | Valid first target plus missing, unreadable or unsupported later target | Offending target named; exit 2; no clean-success message; no fix writes |
| AC-6 | Unknown option or missing option value | Explicit input error; exit 2; no scan/fix silently using reduced scope |
| AC-7 | `check --json` across multiple paths, both clean and with later findings | Pure diagnostic array; existing record shape; correct findings and exit status |
| AC-8 | `check --json` with an invalid later target | Parseable `[]` on stdout; explanatory stderr; exit 2 |
| AC-9 | Multi-path `fix --dry-run`, followed by `fix` on supported fixtures | Dry-run identifies fixes across all targets without editing; actual fix processes each selected file once |
| AC-10 | No path, one path, implicit check form, empty valid directory and generated-file exclusions | Documented defaults and compatibility retained; complete counts; explicit zero-file result where appropriate |
| AC-11 | Declaration/helper in one target used by code in another | Combined semantic inputs preserve supported analysis and CR070 exemption behavior |
| AC-12 | Consumer reruns the four AIA project paths with the candidate | Combined unique file count equals the union of separate scans on that same checkout; expected clean baseline; no ignored inputs |

Unreadable-target tests must exercise a real access/enumeration failure rather
than depend on permission bits when running as a privileged user. An injected
failure is acceptable for deterministic provider coverage.

## 4. Delivery and Consumer Acceptance

1. Adele has reviewed and confirmed the CR identity (`CR078`) and scope, formally adopting this requester-owned CR document.
2. RAIkeep (Codex `7001`) accepts the assignment, implements the correction and regression tests, and supplies `<Component>_RELEASE_NOTES_<Version>.md` following the provider release-notes template, referencing the exact adopted CR filename (`CR078_AIA_to_RAIkeep_Rail_Multi_Path_Input_Completeness.md`).
3. Zébio/Adele independently verifies the candidate in AIA, checks input coverage and every acceptance criterion (AC-1 through AC-12), and records acceptance or rejection with an improvement request. Provider tests alone do not constitute consumer signoff.
4. After consumer acceptance, Rainer may run the Engenho release manually. The version is released only once publication completes. No release or provisioning is authorized before formal consumer signoff.

Until a correction is accepted and published, run one path per `rail check` invocation and verify each reported file count.
