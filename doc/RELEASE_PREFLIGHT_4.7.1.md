# RAIkeep 4.7.1 release preflight

**Status: candidate validated; release not started.** The 4.7.0 coordinated
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
| RaiGuard RAI021 | Four focused analyzer tests passed; the scan identified non-exempt synthetic OsLib tests, which were replaced and verified |
| Release tooling | Ten tests passed, including Vikela version and release ordering; CLI style source, trusted publishing, retired release-chain and package guard checks passed |
| Python packages | Three wheels and three source archives built and passed Twine; wheels installed offline with dependency and CLI checks |
| Installed Umgodi wheel | Persistence smoke passed in a run-owned directory on the configured Dropbox drive |
| Umgodi suite | Full rerun: 226 passed, one optional sequence test skipped; the separately enabled sequence suites passed |
| Optional Dropbox sequence suites | All seven suites passed after correcting real ticket timing; 16 minutes |
| Amafu bootstrap tests | 114 passed under the explicit exemption described below |
| Selected .NET release regressions | 73 passed, including exempt Amafu configuration-listing tests |
| Full release validation | All 146 checks passed; the Umgodi suite was collected before the final sequence-helper refactor, which was separately verified |
| Engenho dry-run | Passed; Inqaba and Vikela precede Umgodi in the release DAG |
| Candidate branches | Component and umbrella main branches pushed; the archived local JsonPit.Python checkout remains untracked |

Umgodi's release depends on both Inqaba and Vikela, so its publishing workflow
can install the coordinated Vikela version before running the repository gate.
Cloud-dependent tests must use the active real configuration and actual cloud
drive, or report a skip when those prerequisites are unavailable.

Dr. Burkhardt explicitly exempted the existing Amafu bootstrap, detection and
configuration tests, both locally and in GitHub Actions, from the prohibition
on substitute test configurations and simulated provider directories. This
exemption does not extend to other projects or permit modifying the real user
configuration.
