# Previous release-chain.sh reference

**CR077 / 4.6.0 and Vikela 4.6.0 use Engenho.** Follow
[the handover for Rita](doc/HANDOVER_TO_RITA_Engenho_CR077_Vikela.md); do not use
the script below to launch this coordinated release. This document preserves
the previous script procedure for reference and earlier release recovery.

The existing script invocation shape is:

```zsh
cd /Users/RSB/Projects/GitHub/RAIkeep
scripts/release-chain.sh 4.6.0
```

Use a zsh session with `PYPI_TOKEN` available and GitHub CLI authentication for
the repositories. The chain uses `~/.venvs/raikeep-release`; that environment
must provide Python 3.12 or newer with `pytest`, `build`, and `twine`.
Do not print credentials when checking the environment.

Release preparation ends with clean child repositories and a clean umbrella
commit recording those exact child commits. Preparation does not create release
tags or publish packages. The manual chain owns the pushes, tags, and publication.

## Release order

The chain preflights all repositories before releasing a child. Each package's
publish workflow and package visibility checks must complete before the next
repository is released:

1. Amafu
2. OsLibCore
3. RaiUtils
4. RaiImage
5. RaiDiagram
6. RaidSeeder
7. JsonPit
8. JsonPit.Python: both `jsonpit` and `jpit` on PyPI
9. ImgSeeder
10. PitSeeder
11. RaiGuard and RaiGuard.Analyzer
12. RAIkeep umbrella GitHub Release

The umbrella is pushed and tagged last, after all child packages are visible.
Its tag records the prepared child commits and publishes no NuGet package.
Published tags are immutable: never move a tag to recover a failed release.

NuGet visibility requires HTTP 200 for both the exact `.nupkg` and registration
document. The chain retries transient network errors and stops after its bounded
wait if visibility does not arrive. Python visibility requires both exact PyPI
distribution versions. The Python step also creates its GitHub Release and
attaches the standalone CLI and package artifacts.

## Recovery

Read the failure before resuming. Confirm the last completed package is visible
and its tag identifies the prepared commit. Use the applicable checkpoint:

```zsh
scripts/release-chain.sh 4.6.0 --resume-after-amafu
scripts/release-chain.sh 4.6.0 --resume-after-oslib
scripts/release-chain.sh 4.6.0 --resume-after-raiutils
scripts/release-chain.sh 4.6.0 --resume-after-raiimage
scripts/release-chain.sh 4.6.0 --resume-after-raidiagram
scripts/release-chain.sh 4.6.0 --resume-after-raiguard
```

Choose one command for the actual stopping point. `--resume-after-raiguard`
verifies the completed child releases and finishes the umbrella step. Recovery
does not authorize retagging or changing child commits after preparation.

## Preparing the next version

```zsh
cd /Users/RSB/Projects/GitHub/RAIkeep
python3 scripts/bump-version.py 4.6.0
```

For a new release, supply the chosen unused version. The manifest-driven bumper
updates package versions, current documentation, tests, Python distributions,
and consolidated release histories. Author the new release highlights, run
`dotnet test RAIkeep.slnx` and the release validator, then commit the child
repositories before committing their matching umbrella pointers.

The version manifest is
[release-manifest.json](https://github.com/Burkhardt/RAIkeep/blob/main/scripts/release-manifest.json).
The release notes live under
[doc/releases](https://github.com/Burkhardt/RAIkeep/tree/main/doc/releases).

## Provisioning

After publication, Engenho owns installation and upgrades across the fleet.
Running the release chain does not provision hosts. Do not run the legacy fleet
installation scripts as part of this release procedure.
