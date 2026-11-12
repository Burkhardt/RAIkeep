# RAIkeep 4.6.4 release preparation

Date: 2026-11-12. Status: local preparation; not ready for release execution.
The approved next release target is **4.6.4**. Current coordinated metadata is
still **4.6.3**; Inqaba and Umgodi package metadata is still **0.1.0**.

## Committed scope

| Repository | Local commit | Delivered behavior |
| --- | --- | --- |
| JsonPit | `6fb4a829831fda2b9379308caf46be469d8ddefd` | Local cloud fixtures use unique Dropbox run roots; shared startup deletion is removed; fixture disposal precedes cleanup. |
| PitSeeder | `853d8fc923ece438fefafede65c5d56a6e343d1a` | Check Dropbox root resolution and preserve read-only explicit OneDrive AIA/AfricaStage resolution. |
| umgodi-json | `a9c006bf12bb798b8e231b91462c38760944ce3b` | Allocate sequence roots beneath configured Dropbox and reject root/provider overrides that escape that boundary. |

RemoteSyncTests and RemoteCloudConcurrencyTests remain unchanged and continue to
exercise the actual Nkosikazi ↔ Mzansi OneDrive channel in
`RAIkeep/jsonpit-remote-sync-tests/{testId}` and
`RAIkeep/jsonpit-cr003-remote/{testId}`. They are separate from the local test run.
The frozen JsonPit.Python repository is unchanged.

## Verification available

- JsonPit local tests: 234 passed, plus the new isolation regression run separately
  with 1 passed. Both runs had zero skips and zero failures.
- PitSeeder cloud-root checks: 5 passed, zero skips and zero failures.
- Umgodi: 210 passed, including 9 new isolation checks.
- The opt-in destructive sequence suites and both remote replication suites were
  not executed. The passing Python count must not be presented as execution of
  the declarative sequence suites.
- JsonPit.Tests and pits.Tests use xUnit v3 3.2.2; Assert.Skip is valid here.
  AIA/AfricaStage remain on xUnit 2.x and need their supported custom attributes
  or standard skip patterns.
- Re-running `bash scripts/check-markdown-document-links.sh` exits 1 for existing
  document links, including the umbrella README and older CR handovers. New
  preparation documents use absolute GitHub document links.

Structured results and commands are in
[the isolation evidence](https://github.com/Burkhardt/RAIkeep/blob/main/doc/verification/Dropbox_Isolation_4.6.4_Preparation.json).

## Pending before the coordinated version bump and release

1. **Zébio's configuration CR:** add canonical `TestCloud: "Dropbox"` beside
   `DefaultCloudOrder` in RAIkeep.json5. The CR must define consumers and missing
   key behavior. Today's local helpers explicitly select Dropbox; they do not
   yet read TestCloud. Preserve the remote OneDrive exception and production
   DefaultCloudOrder. No machine configuration was edited for this preparation.
2. **Frozen Python release handling:** the current version bumper still targets
   JsonPit.Python files and rebuilds its standalone artifact. Its manifest entry
   also references temporary 4.6.3 jsonpit/jpit candidates. Reconcile these with
   the freeze before running the bumper; do not silently rewrite or republish
   the frozen implementation as 4.6.4.
3. **New Python publishing:** supply the requested `publish-pypi.yaml` workflows
   and matching Trusted Publishers for Inqaba and Umgodi. Reconcile Umgodi's
   `extraPackages`: `umgodi` and `jpit` are console entry points in its current
   wheel, and do not themselves prove separate distribution artifacts exist.
   Resolve compatibility distribution ownership before publishing any jpit shim.
4. **Release documentation and metadata:** register new package release histories,
   apply the agreed version policy, complete release notes and fix the outstanding
   umbrella Markdown-link CI failure. The draft highlights are in
   [the consolidated release history](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#464).
5. **Final candidate checks:** run the coordinated release validator, package
   builds/fresh-install checks and relevant tests against the final CR and bumped
   sources. Keep remote acceptance separate and report its actual result.

The existing 4.6.3 Engenho checkpoint is completed, not an interrupted release
to resume. Once the gates above are resolved, the next release-chain run is a
fresh **4.6.4** run through Engenho. This handover records preparation only;
no push, tag, publish, provisioning or release dispatch has occurred.
