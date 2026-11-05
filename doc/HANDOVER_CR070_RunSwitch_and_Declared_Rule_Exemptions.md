# CR070 implementation and release acceptance — 4.6.1

Request: CR070_AIA_to_RAIkeep_RAI007-Test-Run-Switches-and-RAI011-RAI015-Subject-Sites.md.
Target: the complete synchronized RAIkeep 4.6.1 suite, including optional Vikela.

## Programmer-visible contract

- Os.RunSwitch(string name) reads only the process environment, returns null when
  unset, and does not cache the value or consult Os.Config. No setter is added.
- OsLib.RaiRuleExemptionAttribute(ruleId, justification) applies to a method or
  class, permits multiple rule-specific declarations, and requires a nonblank
  justification. It is not inherited by derived classes.
- RaiGuard resolves the actual attribute symbol, including aliases and partial
  declarations. It never treats a similarly named unrelated attribute as an
  exemption. Blank reasons, unrelated rule IDs, and wildcard-like declarations
  do not silence a finding.
- The declared scope suppresses only the specified rule. Neighbors and other
  rules stay audible. Compiler analyzers and semantic rail inspection share this
  contract; there is no blanket test-project exemption.
- RAI007 guidance distinguishes developer/CI invocation switches (RunSwitch),
  persistent machine/storage configuration (Os.Config), and host settings
  (WebApplicationFactory.UseSetting). Direct process-wide environment writes
  remain prohibited.

Os previously initialized its runtime snapshot and probed the configured temp
folder on any Os access. Those operations now initialize together, once, on first
configured-runtime access. This is necessary for RunSwitch to work at test
selection/discovery time without initializing storage. The existing fail-fast
writable-temp validation remains mandatory when configured runtime is used.

## AIA adoption and acceptance

Seven Environment.GetEnvironmentVariable calls in five test files now use
Os.RunSwitch. The default-parser date-coercion regression uses a method-scoped
RAI015 exemption with a justification; its JObject.Parse assertion remains intact.
The centralized runtime/analyzer package pins move together to 4.6.1.

The current AIA.slnx contains four .NET projects (Core, Api, and their two test
projects), rather than the five mentioned in the older CR. Every current solution
project is included in the acceptance build. The workbench is verified separately.

Candidate package build: **0 warnings / 0 errors**, using a private local NuGet
feed and cache. No pragma warning disable, editorconfig diagnostic bypass,
NoWarn, or disabled analyzer was introduced in AIA. The repository scan found no
such bypasses in the active project inputs.

Consumer tests: **1,766 passed / zero failed / six existing opt-in live checks
skipped**. These skips retain their explicit run-switch contracts; they were not
added to manufacture this result. The required workbench build passed.

## Framework verification

The new OsLib tests passed (five added cases plus the existing temp contract).
The eight new analyzer tests passed, covering raw reads/writes, method/class
scopes, aliases/partial classes, invalid and unrelated declarations, neighboring
findings, derived types, and a separate compiler analyzer through the suppressor.
Python runtime: 131 passed. Vikela: 71 passed. Candidate wheels/sdists built and
passed Twine metadata checks. The complete .NET suite includes an existing remote
OneDrive/Mzansi test; its exact result and recheck are recorded below.

The isolated packaged-dependency RaiGuard CI rehearsal also passed: zero build
warnings/errors, 117 analyzer tests and 23 rail tests. The suite consistency
validator passed 141 checks.

Initial full solution run: 1,204 passed and one failed. RemoteSync's file and active
master lease reached Mzansi, but the installed remote seed command exceeded its
120-second timeout before returning. The failure was retained; the isolated
recheck uses the same normal timeouts. No services, mounts, or cloud client
settings were changed.

## Release execution

The user authorized `engenho release 4.6.1`. Release orchestration, immutable tags,
registry visibility, and the final umbrella step use Engenho, not release-chain.sh.
The manifest points Python publication at the fresh 4.6.1 candidate artifacts and
preserves companion jpit / RaiGuard.Analyzer visibility checks. No fleet
provisioning is part of this release instruction.

AIA's adoption is local commit f65d2115d44c1d5dc90d0b444b02eeeda1788d98
(not pushed or deployed). The final child source SHAs and candidate artifact
hashes are captured in the CR070 evidence receipt. Publication results and the
published-package acceptance build are recorded after Engenho completes.

## Logs

- /private/tmp/cr070-aia-candidate-build.log
- /private/tmp/cr070-aia-tests.log
- /private/tmp/cr070-aia-workbench-build.log
- /private/tmp/cr070-solution-tests.log
- /private/tmp/cr070-remote-recheck.log
- /private/tmp/cr070-consistency.log
