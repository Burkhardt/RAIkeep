# Release Notes: RAIkeep v4.6.1

**Date:** 2026-11-05

**Author / Delivering Agent:** RAIkeep Codex Agent

**Delivered Version:** v4.6.1 candidate implementation

**Target Consumers:** AIA, AfricaStage, Engenho and RAIkeep package consumers

**Status:** Implementation and candidate validation complete; manual release and requester acceptance pending confirmation

## 1. Summary

CR070 gains an explicit process-invocation switch API and justified, rule-specific
exemptions for tests whose subject is the hazard being diagnosed. The AIA
candidate integration compiles with zero warnings without pragmas or analyzer
configuration bypasses. This provider report supplies implementation evidence;
acceptance belongs to the requesting team.

## 2. Resolved Change Requests (CRs)

- [CR070_AIA_to_RAIkeep_RAI007-Test-Run-Switches-and-RAI011-RAI015-Subject-Sites.md](CR070_AIA_to_RAIkeep_RAI007-Test-Run-Switches-and-RAI011-RAI015-Subject-Sites.md)
  — Implement the preferred named run-switch accessor, distinguish its guidance
  from persistent configuration, and support declared rule-subject exemptions.
  Submitted for requester evaluation, not self-accepted by the provider.

The original CR reported nine warnings. CR077 in 4.6.0 already cleared the RAI011
live-handle sites; this delivery addresses the seven remaining RAI007 reads and
the intentional RAI015 parser assertion, while providing a shared exemption
contract for explicit subjects of other RaiGuard rules.

## 3. Root Cause Analysis & Technical Resolution

RAI007 previously directed all environment reads toward machine configuration or
host settings. Neither models a disposable developer/CI opt-in, particularly
during test discovery before a host exists. `Os.RunSwitch` now expresses that
intent explicitly: it reads the current process environment directly, returns
null when unset, and never reads or writes `Os.Config`.

Previously, any `Os` access initialized configuration and probed the configured
temporary directory. A nested runtime holder now performs those operations once
on first configured-runtime access. This makes RunSwitch usable without storage
startup while preserving the existing writable-temp validation for configured
runtime use.

The intentional default-parser regression must retain `JObject.Parse`: replacing
it with the safe parser would remove the behavior the test is proving. RaiGuard
now resolves `OsLib.RaiRuleExemptionAttribute` semantically on the containing
method or class. Both compiler diagnostics and `rail` inspection honor matching
rule IDs with nonblank justifications. Aliases and partial declarations work;
unrelated attributes, blank reasons, other rules, neighboring methods and derived
classes do not gain an exemption. No blanket test-assembly exemption is added.

Primary implementation sites:

- `OsLib/Os.RunSwitch.cs`, `OsLib/Os.Config.cs` and
  `OsLib/RaiRuleExemptionAttribute.cs`.
- `RaiGuard/src/RaiGuard.Core/Rules/RuleExemptions.cs` and the architecture-rule
  diagnostic guidance.
- The RaiGuard compiler diagnostic suppressor, plus runtime and analyzer
  regression tests.

## 4. Public Contract & API / Package Changes

```csharp
string? enabled = Os.RunSwitch("AIA_LIVE_TENANT_SCAN");

[OsLib.RaiRuleExemption("RAI015",
    "Default parser date coercion is this regression's explicit subject.")]
public void TheDefaultParserTurnsAnIsoStringIntoADate()
{
    // Keep the intentional JObject.Parse assertion here.
}
```

- `Os.RunSwitch(string name)` is read-only, uncached and has no configuration
  fallback or setter.
- `RaiRuleExemptionAttribute(string ruleId, string justification)` applies to
  methods/classes, allows repeated declarations, and requires nonblank values.
  Class exemptions are not inherited by derived classes.
- RAI007 recommends RunSwitch for developer/CI invocation reads, Os.Config for
  persistent machine/storage configuration, and host-scoped settings where
  appropriate. Direct process-wide environment writes remain prohibited.
- Suite package versions are synchronized at 4.6.1, including optional Vikela.
  These are additive public APIs; existing machine-configuration and natural
  JsonPit mutation APIs remain available.

## 5. Validation & Acceptance Evidence

| Check | Observed result |
|---|---|
| AIA build against local 4.6.1 candidate packages | 0 warnings, 0 errors |
| AIA tests | 1,766 passed, 0 failed, 6 existing opt-in live tests skipped |
| AIA workbench build | Passed |
| OsLib targeted checks | 5 added cases and existing temp contract passed |
| New analyzer regression cases | 8 passed |
| Isolated RaiGuard package-dependency CI rehearsal | Build: 0 warnings/errors; 117 analyzer and 23 rail tests passed |
| Python runtime | 131 passed |
| Vikela | 71 passed |
| Release consistency | 141 checks passed |
| Candidate artifacts | 11 NuGet packages and 3 Python distributions, all version 4.6.1; metadata checks passed |

The current AIA solution contains four .NET projects rather than the five named
in the older CR. All four were built. Seven environment reads in five test files
now use RunSwitch; the parser regression has a method-only RAI015 exemption and
retains its original assertion. No pragma, editorconfig bypass, NoWarn setting,
or disabled analyzer was introduced to achieve the result.

The first full `dotnet test RAIkeep.slnx` run recorded 1,204 passes and one remote
OneDrive/Mzansi failure: the remote seed command exceeded its 120-second timeout.
The isolated rerun of that same test subsequently passed all six phases in
20 minutes 3 seconds with unchanged normal timeouts, including master handover,
receipt-aware cleanup and data integrity. The initial failure is retained as
evidence; the complete suite was not rerun after the isolated pass. No cloud
services, mounts or client settings were changed.

The AIA zero-warning result above uses candidate packages. A build against the
completed public release and independent requester acceptance are not yet
recorded here. AIA adoption is committed locally, not pushed or deployed.

Detailed evidence: [CR070 implementation handover](HANDOVER_CR070_RunSwitch_and_Declared_Rule_Exemptions.md)
and [candidate evidence receipt](verification/CR070_4.6.1_Evidence.json).

## 6. Upgrade & Consumption Instructions

1. After the user confirms publication, update centralized RAIkeep runtime and
   analyzer package pins to 4.6.1 together. Vikela remains optional development
   tooling and is not a runtime dependency of jsonpit or jpit.
2. Replace developer/CI invocation reads with `Os.RunSwitch(name)`. Keep durable
   machine/cloud settings in `Os.Config`; use host-scoped settings for test hosts.
3. For intentional rule-subject regressions, declare only the required rule on
   the specific test method with a concrete justification. Preserve the hazardous
   call that is the assertion subject; do not exempt the entire test assembly.
4. Run `dotnet build AIA.slnx --no-incremental` against the published packages,
   confirm zero warnings/errors without bypasses, and run the consumer tests.
5. The requesting PM/agent records independent acceptance or rejection using the
   requester evaluation template and references this exact release-notes filename.

Release and provisioning are separate user-controlled operations. The agent's
initial release run was stopped at the user's request; the user stated that they
would resume it manually. This report does not claim that the full release or
fleet provisioning has completed. No release, push, tag or provisioning command
was executed to produce this document.
