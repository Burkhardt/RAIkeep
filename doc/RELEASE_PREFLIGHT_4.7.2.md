# RAIkeep 4.7.2 readiness review

**Hold publication until the full release validator passes.** The release operator runs the active Engenho chain after verification. See [Release preparation](../ReleasePrep.md).

| Preparation check | Candidate result |
| --- | --- |
| Version availability at preparation | No v4.7.2 tags on the umbrella or thirteen components, no local Engenho checkpoint, and all fourteen exact registry version queries returned 404. |
| Source versions | All 129 metadata checks passed. The thirteen component revisions were pushed to main and verified against their remotes. |
| Tests | 180 RaiImage, 94 ImgSeeder, 114 Amafu, two cross-language replica tests, 22 Inqaba and 120 Vikela tests passed. Ten release-tool and four trusted-publishing tests passed. See [CR094 acceptance](RELEASE_NOTE_CR094.md). |
| Build and guardrails | The Release solution build produced zero warnings and errors. Rail reported zero findings across the included projects. Vikela reported three expected negative-fixture findings and zero unexpected findings. Amafu and its tests passed the standalone dependency check. |
| Packages | Built coordinated packages, checked NuGet metadata and READMEs, and validated all six Python artifacts with Twine. Fresh installs passed dependency checks and all eight CLI entry points reported 4.7.2. |
| Full release validator | Dropbox-backed Umgodi tests and three CLI parity checks encountered a permission error reading the configured Dropbox timing file. Finder shows the calibrated values, but the release process needs read access to verify these checks. |
| Optional replication sequences | The full validator skips the opt-in sequence suite by default. |
| Engenho simulation | The 4.7.2 dry run passed for the pushed candidate at 2cc3e8c, including all thirteen components and DAG preflight. |
