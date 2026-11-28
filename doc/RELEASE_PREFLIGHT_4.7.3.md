# RAIkeep 4.7.3 candidate preflight

**RAIkeep 4.7.3 candidate signed off on November 27, 2026.** Rainer verified the corrected candidate in his interactive shell on the configured TestCloud. All 146 release checks passed. [CR095 acceptance and test selection](RELEASE_NOTE_CR095.md)

| Check | November 26 evidence |
| --- | --- |
| Version availability | The umbrella and all thirteen component remotes had no v4.7.3 tag. All fourteen exact-version registry lookups returned HTTP 404. No 4.7.3 Engenho checkpoint was present. |
| Candidate metadata | The coordinated version bumper updated the manifest and registered project, dependency, documentation and release-history entries. The metadata validator passed all 129 checks. |
| Local ticket tests | The 4.7.3 Release build passed all 245 JsonPit tests selected by the local filter in 19 seconds. |
| Python distributions | Built wheels and source archives for inqaba, umgodi-json and vikela. All six passed strict Twine checks. The three wheels installed together in a fresh environment, pip check passed, and umgodi, jpit and vikela each reported 4.7.3. |
| Python guardrails | Vikela checked 99 files and found only the three intentional negative fixtures. The fleet benchmark's three workload and reporting tests passed. |
| .NET build and packages | The Release solution build finished with zero warnings and zero errors. All eleven NuGet packages contained version 4.7.3 metadata and their declared README. Using only the local candidate feed and a fresh package cache, Amafu, PitSeeder, ImgSeeder, RaidSeeder and RaiGuard installed successfully. Their five CLI entry points each reported 4.7.3. |
| Full release validator | Four checks failed. The umgodi-json suite reported 177 passes, 50 failures and one skip. Its failures included access errors on the configured Dropbox timing file. CLI export parity and the two fixture seeds for list and contextual-help parity also encountered that access error. The inqaba and vikela suites passed all 22 and 120 tests respectively. |

## November 27 interactive verification

Rainer reported 13 CloudEffect passes, two SSH skips and two split-master recovery failures. Both affected tests now exercise the synchronous conflict scan in `Reload()`. One checks loser recovery after a returned turn. The other checks orphan retention and retirement while the same master ticket is held. Both use the configured TestCloud.

Rainer ran the following checks from the umbrella checkout after the corrections.

```zsh
cd /Users/RSB/Projects/GitHub/RAIkeep &&
  dotnet test RAIkeep.slnx -c Release -p:UseLocalRAIkeepSources=true --filter 'Category=CloudEffect' --logger 'console;verbosity=normal' &&
  .release-venv/bin/python -u scripts/validate-release.py 4.7.3 4.7.2
```

| Final check | Reported result |
| --- | --- |
| CloudEffect | 15 passed (14 JsonPit.Tests and one ImgSeeder.Tests), zero failed. Two SSH tests skipped because Mzansi and the local machine have different TestCloud roles. All CR090 and CR095 cloud checks passed. |
| Split-master recovery | `OrphanedConflictFlag_IsRetiredOnlyAfterExpiryPlusGrace_WithValidatedCriticalEvidence` passed in 221 ms. `MissedWatcherNotification_IsRecoveredAtTheNextOperationBoundary_WithoutPolling` passed in 2 s. |
| Release validator | Exit code 0. All 146 checks passed across stages 1–7, including umgodi-json, all 120 vikela tests, CLI theme and export parity, and the local list and WWWA help parity fixture seeds. |

Rainer will run the Engenho dry run and production release after remote commit verification.
