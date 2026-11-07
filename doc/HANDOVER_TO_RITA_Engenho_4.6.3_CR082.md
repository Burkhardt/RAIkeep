# Engenho handover: RAIkeep v4.6.3 / CR082

**Date:** 2026-11-07  
**Consumer gate:** Independently accepted by Adele for AfricaStage/AIA; see
[CR082_Accepted_Jpit_Default_Cloud_Resolution_and_Missing_Export_v4_6_3.md](CR082_Accepted_Jpit_Default_Cloud_Resolution_and_Missing_Export_v4_6_3.md).  
**Execution owner:** Dr. Rainer Burkhardt. Preparation does not execute release or provisioning.

## Release inputs

- `scripts/release-manifest.json` targets 4.6.3 across all twelve child repositories.
- The Python publication entry references fresh jsonpit/jpit wheels and source
  archives under `/private/tmp/raikeep-4.6.3-candidates/python/` on Nkosikazi.
  Both distributions must be published and become visible at the same version.
- Vikela's workflow and version remain coordinated at 4.6.3; it remains optional
  development tooling, with no new analyzer behavior in this point release.
- Preserve the existing dependency graph, Trusted Publishing policies, workflow
  names, immutable existing labels and umbrella-last release behavior. All new
  tags/publications belong to RAI's manual Engenho execution.
- Candidate metadata, package hashes, committed sources and checks are recorded
  in [CR082_4.6.3_Release_Preparation.json](verification/CR082_4.6.3_Release_Preparation.json).

## Runner behavior

CR082 changes Python jpit read-side root resolution and export failure reporting:

```text
jpit export Object -r AfricaStage --json -n
jpit export Object -r AfricaStage --out-dir <directory> -n
```

With no explicit cloud, a bare tenant resolves via the configured default cloud.
Use `-r ./AfricaStage` for a relative local path. Missing canonical snapshots exit
1 with empty stdout and the full `.pit` path on stderr; existing output files
remain unchanged. A valid empty snapshot still exits 0 and returns `[]`.
WWWA export requires all four source snapshots.

Check process exit status before consuming stdout or an existing output file.
No changes to Engenho source are required for callers already respecting exit
status. Tenant mutations still require an explicit provider or local path under
CR069. C# pit contracts, source formats and mutation semantics are unchanged.

## Manual execution after preparation

All 141 release checks and candidate artifact checks pass. The separate live
replication retry repeated the 600-second visibility timeout despite using direct
SSH. Mzansi's rclone mounts have been verified active; the earlier claim that
OneDrive was inactive is retracted. One live case failed and the other was not
completed; neither is included in the 1,244 passing .NET tests. See the preparation
report/evidence and obtain RAI's release-readiness decision on this exception.

From the prepared RAIkeep workspace:

```zsh
engenho release 4.6.3
```

After release completion and registry visibility:

```zsh
engenho provision all
```

Provision through Engenho using its established configuration and selection
policy. Keep Vikela development tooling off production nodes unless explicitly
selected. Do not run the legacy install script or shell release chain.
