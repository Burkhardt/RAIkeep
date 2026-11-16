# RAIkeep 4.6.4 release preparation

The standalone 0.1.0 wheels and source distributions for Inqaba and Umgodi were published on November 15, 2026. All four public SHA-256 hashes matched the preflight artifacts. Installing `umgodi-json==0.1.0` from PyPI in a fresh environment installed Inqaba and exposed both `jpit` and `umgodi`.

- [Inqaba 0.1.0 on PyPI](https://pypi.org/project/inqaba/0.1.0/)
- [Umgodi JSON 0.1.0 on PyPI](https://pypi.org/project/umgodi-json/0.1.0/)
- [Frozen jsonpit-python repository and migration notice](https://github.com/Burkhardt/jsonpit-python#jsonpit)

The legacy distribution carries the successor link in its documentation-only post-release. [PyPI sunset notice](https://pypi.org/project/jsonpit/4.6.3.post1/)

## Coordinated release

The 4.6.4 manifest includes ten .NET repositories and the three Python distributions Inqaba, Umgodi JSON and Vikela. Engenho waits for Inqaba before dispatching Umgodi. The two Python workflow files are on their default branches. Each uses the GitHub environment `pypi` and verifies the dispatch tag against the package version and checkout.

The remaining account setup is to register each new project's GitHub Trusted Publisher on PyPI using owner `Burkhardt`, its matching repository name, workflow `publish-pypi.yaml` and environment `pypi`. The standalone upload used a PyPI credential and therefore did not exercise GitHub OIDC.

RAI starts the coordinated chain manually from the umbrella checkout with `engenho release 4.6.4`. The completed 4.6.3 checkpoint belongs to the previous release. The active installer selects Umgodi starting at 4.6.4. Older versions of the installer contract retain the frozen distribution.

## Verification scope

The candidate includes CR087 and ordinary-open change retirement coverage. [Provider report](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR087_Provider_Review.md)

The candidate passed the coordinated validator, local .NET tests, Python tests, package builds, and isolated installs. The two Nkosikazi–Mzansi replication suites still use OneDrive. Their live execution and the destructive opt-in sequence run are outside this local verification. Zébio's downstream work is independent of release execution.

[Candidate evidence](https://github.com/Burkhardt/RAIkeep/blob/main/doc/verification/Release_4.6.4_candidate.json) · [Dropbox isolation results](https://github.com/Burkhardt/RAIkeep/blob/main/doc/verification/Dropbox_Isolation_4.6.4_Preparation.json)
