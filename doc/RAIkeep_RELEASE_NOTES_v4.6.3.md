# Release Notes: RAIkeep v4.6.3

**Date:** 2026-11-07  
**Delivering agent:** Codex, RAIkeep Custodian  
**Target version:** v4.6.3  
**Consumers:** AfricaStage, AIA, Engenho and RAIkeep users  
**Status:** CR082 independently accepted; coordinated local preparation completed. Live-replication verification remains outstanding as described below. RAI executes publication and provisioning manually.

## 1. Summary

Python jpit exports now resolve bare tenant names through configured cloud
storage. Missing input snapshots return an error without printing an empty
success result or overwriting existing exports. The suite remains versioned
together at 4.6.3 across all twelve child repositories, including optional Vikela.

## 2. Addressed change request and acceptance

- [CR082_AfricaStage_to_RAIkeep_Jpit_Default_Cloud_Resolution_and_Missing_Export.md](CR082_AfricaStage_to_RAIkeep_Jpit_Default_Cloud_Resolution_and_Missing_Export.md)
  — provider implementation and regression tests delivered in
  [JsonPit.Python_RELEASE_NOTES_4.6.3.md](JsonPit.Python_RELEASE_NOTES_4.6.3.md).
- [CR082_Accepted_Jpit_Default_Cloud_Resolution_and_Missing_Export_v4_6_3.md](CR082_Accepted_Jpit_Default_Cloud_Resolution_and_Missing_Export_v4_6_3.md)
  — independent Adele/AfricaStage/AIA CDAT accepted. The user reports the AIA mirror
  at commit `6f1fa12`; the acceptance record is included in the umbrella.

## 3. Root cause and technical resolution

Export's command-root resolver previously treated a bare tenant as a local
directory, unlike status's cloud resolver. Opening a missing source then yielded
an empty pit, producing a misleading successful `[]` export. The shared resolver
now selects the configured default cloud for bare roots; export validates its
canonical source snapshots before destination writes. WWWA audit/report-only
maintenance and root-scoped grep use the supplied root consistently.

Source behavior and tests are unchanged from the independently accepted Python
candidate. Subsequent preparation synchronizes package/dependency versions,
README/API references, current release notes, standalone jpit, Vikela metadata,
and the Engenho manifest. Other components have no package-local behavior change.

## 4. Public contracts and package changes

- All ten .NET child repositories plus jsonpit-python and Vikela target 4.6.3.
  Packaging produces eleven NuGet packages (including RaiGuard.Analyzer) and
  three Python distributions (jsonpit, companion jpit, Vikela).
- The jpit companion pins `jsonpit==4.6.3`. Neither Python runtime distribution
  depends on Vikela. Existing optional Pylint/notebook extras are preserved.
- Explicit `-c` selects a provider. Explicit local path syntax remains local;
  a bare tenant never falls back to a same-named working-directory folder.
- Missing canonical export snapshots exit 1, report their full path on stderr,
  produce zero stdout bytes and preserve output files. Existing empty snapshots
  remain successful; WWWA export requires all four snapshots.
- CR069's explicit write-destination gate, C# mutation semantics, tombstones,
  leasing and storage formats remain unchanged.

## 5. Validation and acceptance evidence

Consumer CDAT verified the real default-cloud AfricaStage export: 312 live Object
entities including `Themba.NomsaBandWeb`, an approximately 260 KB Object.json,
missing-source exit 1 with no stdout and unchanged existing output, and the full
198-test Python suite. The acceptance record belongs to the consumer; provider
checks do not replace it.

The coordinated test summaries, exact child commits, candidate artifact hashes,
metadata/dependency audit and packaged CLI smoke results are recorded in
[CR082_4.6.3_Release_Preparation.json](verification/CR082_4.6.3_Release_Preparation.json).
Candidates are built without publishing or installing tools. The .NET test
build may report existing xUnit/compiler warnings; this release does not claim a
new warning-free provider baseline or suppress those warnings.

- Release preflight: **141 checks passed**.
- Available .NET solution tests: **1,244 passed**, no failures or skips, across
  eleven test projects; two live replication tests are explicitly excluded from
  this count and are not being represented as successful.
- Python: **198 passed**; Vikela: **71 passed**; release preparation tools:
  **10 passed**.
- Eleven NuGet candidates and six Python wheel/sdist artifacts pass metadata,
  exact dependency-version, entry-point, asset and provenance checks. Extracted
  CLI versions, standalone source equality, cross-engine seed receipts and CR082
  source/wheel/standalone export smoke checks pass without installation.

### Live replication result and correction

The unfiltered .NET run encountered a 600-second timeout waiting for its local
master-claim file to become visible on Mzansi. It was stopped rather than spending
another ten minutes on the same visibility wait. This is not a full-suite pass.
A separate retry of the two live tests uses process-local direct SSH connections.

The initial provider diagnosis, “Mzansi has no active OneDrive service or
process,” was incorrect: only native `onedrive` units/processes had been checked.
Adele identified the actual rclone services. Provider verification then confirmed
all three rclone units active on Mzansi (`65.38.99.46`), OneDrive mounted as
`fuse.rclone`, 30-second directory-cache/poll intervals and full VFS caching.
The local OneDrive app, sync service and file provider are also running. Active
mounts alone do not explain the observed end-to-end visibility timeout; its cause
has not been established. No cloud services or persistent SSH settings were changed.

Keep the live-test result separate from CR082's accepted consumer behavior and
the green release-consistency gate. Do not claim both live tests passed until
their retry provides that evidence.

## 6. Upgrade and manual execution

The [Engenho handover](HANDOVER_TO_RITA_Engenho_4.6.3_CR082.md) identifies the
manifest inputs and exit-status handling. RAI runs `engenho release 4.6.3`
manually, then `engenho provision all` after successful publication and visibility.
Provisioning keeps optional development tooling off production servers according
to Engenho's established policy.

No release chain, registry upload, git push/tag, fleet installation or provisioning
has been executed by this preparation. Published 4.6.2 labels remain intact.
