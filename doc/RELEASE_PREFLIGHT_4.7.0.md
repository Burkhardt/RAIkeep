# RAIkeep 4.7.0 release checks

The coordinated source candidate is umbrella commit `b1a9e9e`. The thirteen active component repositories contain fourteen distributions, including the separately packed RaiGuard.Analyzer. The compatibility jsonpit distribution stays on its frozen version.

| Check | Result |
| --- | --- |
| Source versions | Verified GitHub main metadata for every active component, the separate analyzer package and the umbrella manifest at 4.7.0 |
| Release metadata | 129 validator checks passed with external commands disabled |
| Engenho simulation | Candidate dependency graph and worktree checks passed |
| NuGet package inspection | Built eleven packages with local coordinated sources. Each embedded its declared README and reported 4.7.0 in its nuspec |
| Python distributions | Built three wheels and three source archives. All passed Twine checks. Installed the wheels into a fresh environment and checked imports and installed dependencies |
| Installed CLI versions | amafu, pits, iorg, raid, rail, umgodi, jpit and vikela all reported 4.7.0 |

The first active attempt encountered Amafu project metadata still at 4.6.7. The component version was corrected in `ccdc18c` and the umbrella pins that commit. A subsequent operator-initiated release began during external validation. This record distinguishes the checks completed before publication from verification performed while the release was active.

The external validator completed with one failing gate. Umgodi passed 222 tests locally and failed one. Its [publish workflow](https://github.com/Burkhardt/umgodi-json/actions/runs/45066535996) failed the same assertion with 219 passed and three skipped. The shipped-suite isolation test assumed the developer had selected Dropbox. The [fixture correction](https://github.com/Burkhardt/umgodi-json/commit/f58fb01) supplies an isolated Dropbox configuration. All nine sequence isolation tests passed with an empty home on that branch. The correction is outside the tagged candidate. Provisioning awaits a successfully completed coordinated release.
