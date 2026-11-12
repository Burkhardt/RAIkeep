# Local test isolation and release status — 2026-11-12

Local high-frequency JsonPit cloud fixtures select configured Dropbox only.
Missing Dropbox produces an explicit prerequisite skip rather than a fallback
to OneDrive. Production defaults and Os.Config remain unchanged.

ConfiguredCloudPits supplies a process-specific `RAIkeep.Test.<guid>` directory.
RAIkeepTestEnvironment uses that directory and no longer recursively deletes a
shared root at startup. The real-world WWWA fixture disposes its Pits before
cleanup. Existing per-fixture cleanup stays scoped to that fixture's root.

The Umgodi sequence runner allocates a unique TemporaryDirectory beneath the
configured Dropbox root. All seven shipped suites derive RootName and PitRoot
from that directory. Overrides outside the owned directory are rejected before
commands run. The old hardcoded OneDrive paths have been removed.

RemoteSyncTests and RemoteCloudConcurrencyTests are unchanged: their genuine
Nkosikazi/Mzansi replication continues on OneDrive in isolated test-id folders.

## Verification

- JsonPit local suite excluding the two remote suites: 234 passed.
- Added Dropbox root-isolation regression, run separately: 1 passed.
- pits cloud-resolution checks: 5 passed, including Dropbox and read-only
  explicit OneDrive AIA/AfricaStage resolution.
- Umgodi suite: 210 passed, including 9 new sequence-isolation checks.
- Destructive declarative parity suites remain opt-in and were not enabled.
- No remote replication suite was executed for this change.

## Release position

The local Engenho checkpoint `~/.config/engenho/releases/4.6.3.json` reports
completed, updated 2026-11-07T15:24:26Z, with all twelve package entries indexed.
GitHub's latest umbrella release is v4.6.3. Current umbrella/.NET metadata remains
4.6.3; Inqaba and Umgodi remain 0.1.0.

On inspection, neither new Python distribution exists on PyPI (both JSON project
endpoints return 404), and neither GitHub repository has an Actions workflow.
The manifest requests `publish-pypi.yaml` for both. Their first publication is
outstanding; these packages were not included in the completed 4.6.3 checkpoint.

The approved next coordinated patch target is 4.6.4. Isolation changes are
committed locally in JsonPit (`6fb4a82`), PitSeeder (`853d8fc`) and Umgodi
(`a9c006b`). No push, version bump, tag, publication or Engenho dispatch was made.
See the [4.6.4 preparation handover](https://github.com/Burkhardt/RAIkeep/blob/main/doc/HANDOVER_RELEASE_PREP_v4.6.4.md)
for the remaining gates and the pending TestCloud CR.

Before the next release, prepare versions and release notes, supply publishing
workflows/trusted publishers, and reconcile the manifest's Umgodi extraPackages
with actual built distributions: console command names alone do not constitute
separate PyPI distributions. The umbrella's latest document-link CI run also
failed and needs resolution before release acceptance.

Use Engenho for the next run; the completed 4.6.3 checkpoint is not a pending
release to resume with altered package contents.

## xUnit boundary

JsonPit.Tests and pits.Tests both reference `xunit.v3` 3.2.2, where Assert.Skip
is supported. Their existing conditional skip pattern is retained. AIA and
AfricaStage use xUnit 2.x: downstream adaptations must use a custom FactAttribute
or another supported skip pattern, not Assert.Skip.
