# RAIkeep 4.7.1 release preflight

**Status: incomplete. Do not start the release yet.** The 4.7.0 coordinated
release was incomplete; its published artifacts and tags remain unchanged.

| Check | Result |
| --- | --- |
| 4.7.1 remote tags | No tag found in the umbrella or active component repositories |
| 4.7.1 registries | PyPI and NuGet returned 404 for the coordinated distributions |
| Engenho checkpoint | No 4.7.1 checkpoint found |
| Coordinated .NET solution | Build passed with local sources, zero warnings and errors |
| .NET packages | Eleven packages built; identities, versions and declared README files verified |
| Inqaba tests | 22 passed using the real configuration |
| Vikela tests | 120 passed, including the IPython integration test |
| RaiGuard RAI021 | Four focused analyzer tests passed |
| Release tooling | Ten tests passed, including Vikela version and release ordering; CLI style source, trusted publishing, retired release-chain and package guard checks passed |
| Python packages | Three wheels and three source archives built and passed Twine; wheels installed offline with dependency and CLI checks |
| Installed Umgodi wheel | Persistence smoke passed in a run-owned directory on the configured Dropbox drive |
| Umgodi suite | Running with the real Dropbox root and local Vikela source; result pending |
| Amafu bootstrap tests | 114 passed under the explicit exemption described below |
| Selected .NET release regressions | 73 passed, including exempt Amafu configuration-listing tests |
| Full release validation and Engenho dry-run | Not completed |
| Commits and remote main branches | Component candidates committed locally; umbrella candidate and branch reconciliation pending. Nothing pushed yet |

Umgodi's release depends on both Inqaba and Vikela, so its publishing workflow
can install the coordinated Vikela version before running the repository gate.
Cloud-dependent tests must use the active real configuration and actual cloud
drive, or report a skip when those prerequisites are unavailable.

Dr. Burkhardt explicitly exempted the existing Amafu bootstrap, detection and
configuration tests, both locally and in GitHub Actions, from the prohibition
on substitute test configurations and simulated provider directories. This
exemption does not extend to other projects or permit modifying the real user
configuration.
