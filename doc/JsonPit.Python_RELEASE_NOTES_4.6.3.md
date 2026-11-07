# Release Notes: jsonpit-python / jpit v4.6.3

**Date:** 2026-11-07  
**Delivering agent:** Codex, RAIkeep Custodian  
**Delivered version:** v4.6.3 local Python candidate  
**Consumers:** AfricaStage (Sipho / Eliza), AIA (Adele), Engenho (Rita)  
**Status:** Independently accepted by Adele for AfricaStage/AIA on 2026-11-07; coordinated release preparation authorized. Publication and provisioning remain manual operations for RAI.

## 1. Summary

`jpit export Object -r AfricaStage --out-dir ./exports` now uses the configured
default cloud when `-c` is absent. It no longer interprets the tenant as a local
directory or reports a missing snapshot as a successful empty export.

## 2. Addressed change request

[CR082_AfricaStage_to_RAIkeep_Jpit_Default_Cloud_Resolution_and_Missing_Export.md](CR082_AfricaStage_to_RAIkeep_Jpit_Default_Cloud_Resolution_and_Missing_Export.md)
records RAI's requested correction and the provider's acceptance scenarios.
Requester acceptance is recorded in
[CR082_Accepted_Jpit_Default_Cloud_Resolution_and_Missing_Export_v4_6_3.md](CR082_Accepted_Jpit_Default_Cloud_Resolution_and_Missing_Export_v4_6_3.md).

## 3. Root cause and technical resolution

`resolve_command_pit_root` previously returned an absolute local path for a bare
root whenever cloud was omitted. Export and WWWA audit/maintenance used this
resolver, while single-pit status used OsConfig's cloud resolution. The command
resolver now uses the same configured default for bare tenant roots. Explicit
paths still resolve locally. A shared syntax classifier prevents a coincident
local directory from changing a tenant name's meaning; list retains its existing
configured-order discovery and `--all` behavior.

Grep's default-target form previously inspected the working directory before
considering `-r`. It now enumerates the supplied resolved root. Existing
single-pit get, history, list, status, audit and maintenance default-cloud behavior
is covered by regression tests. Explicit local roots also work without cloud
configuration in the shared pit-target resolver.

The storage engine intentionally permits opening a missing pit for creation.
Export must not use that permissive behavior as evidence that its source exists.
It now resolves the canonical snapshot and checks its existence before opening
the read-only pit. All projections complete before destination creation or writes;
missing input leaves existing exports untouched.

## 4. Public contracts and package changes

- Bare `-r AfricaStage` means a configured cloud tenant. Use `-r ./AfricaStage`
  for a relative local root, or an absolute / home-relative path. This distinction
  also holds when a same-named directory already exists locally.
- Missing export snapshots produce exit **1**, a diagnostic containing the full
  `.pit` path on stderr, and **empty stdout**. This covers directory, stdout,
  compatibility file, jq, timestamp and WWWA export. A valid empty pit returns
  0 and `[]`; WWWA export requires all four snapshots.
- Cloud selection remains configurable, with explicit `-c` overrides. There is
  no local fallback on missing configuration/provider and no fallback to another
  provider merely because a selected pit is absent.
- CR069's explicit-destination mutation guard remains. A same-named local
  directory no longer qualifies a bare tenant as an explicit local destination.
  The independent acceptance explicitly confirms that this safeguard is preserved.
- Python package metadata, companion dependency and standalone banner target
  **4.6.3**. The coordinated suite repositories and Engenho manifest are also
  synchronized to **4.6.3** during the subsequent authorized release preparation.
- No storage format, sparse-delta, tombstone, leasing or C# analyzer changes.

## 5. Provider verification and evidence

- Before the correction, the initial regression set reproduced **24 failures
  across 34 cases**, including false successful empty exports and local fallback.
- The final Python suite passes **198 tests**, including **50 CR082 cases** and
  the existing C#/Python seed interoperability tests. Initial sandbox-only
  failures in three existing C# interoperability cases cleared when their
  configured temporary-directory probes were permitted.
- All **50 CR082 cases also pass against the extracted candidate wheel**.
  Both Python wheels and sdists build cleanly and pass `twine check`. Separate
  subprocess smoke checks exercise the source CLI, wheel and regenerated
  standalone for version, default-cloud JSON/directory export, missing-source
  exit 1, unchanged source bytes and absence of process flags.
- Tests use disposable roots and configurations, not live tenant data. Coverage
  includes cloud order/overrides, root aliases, local decoys, explicit offline
  paths, read-command routing, missing snapshots/output preservation, complete
  and partial WWWA sets, valid empty pits, and CR069 mutation guards.

Packaging and standalone evidence is recorded in
[CR082_4.6.3_Evidence.json](verification/CR082_4.6.3_Evidence.json).
These are provider checks. Adele's separate CDAT record confirms 312 exported
AfricaStage Object entities (including `Themba.NomsaBandWeb`), the approximately
260 KB directory export, the missing-source error/output-preservation contract,
and 198 passing Python tests. No fleet installation has been performed by this work.

## 6. Consumer review and Engenho handover

Run the local candidate without changing installed tooling:

```zsh
python3 /Users/RSB/Projects/GitHub/RAIkeep/JsonPit.Python/bin/jpit --version
python3 /Users/RSB/Projects/GitHub/RAIkeep/JsonPit.Python/bin/jpit export Object -r AfricaStage --json
```

Independent consumer CDAT has passed; retain the acceptance record with the
release evidence. The local invocation remains available for inspection before
RAI starts the release.

Rita's runner must check the exit status before treating an export as complete;
an empty result alone cannot prove success. No runner implementation change or
release-chain.sh investment is requested by this fix. See the
[coordinated preparation report](RAIkeep_RELEASE_NOTES_v4.6.3.md) for the suite
checks and artifacts. RAI alone runs release and provisioning manually.
