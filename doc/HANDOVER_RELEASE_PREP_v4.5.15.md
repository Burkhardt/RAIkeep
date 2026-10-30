# RAIkeep 4.5.15 release preparation

Prepared on 2026-10-29. Publication remains at the manual gate.

## Start the release

```zsh
cd /Users/RSB/Projects/GitHub/RAIkeep
scripts/release-chain.sh 4.5.15
```

Use a shell with GitHub authentication and `PYPI_TOKEN` available. The configured
release environment at `~/.venvs/raikeep-release` has the required Python tools.
No credentials are included in this document.

The chain pushes and publishes the children sequentially and waits for package
visibility, then pushes/tags the umbrella last. Release preparation has created
local commits only: no release tags, package uploads, workflow dispatches, or
fleet installations have been performed.

## Delivered changes

- Shared help colors, aligned columns, syntax emphasis, and versioned headings
  across all .NET CLIs and jpit/jsonpit, including standalone Amafu.
- Public window and strict-ID aliases, contextual list/ls help, and compatible
  hidden spellings in pits and jpit.
- Python directory/WWWA exports aligned with pits; refreshed standalone jpit.
- Rail group descriptions wrap at 90 columns with hanging indents and consistent
  identifier colors.
- Release validation now checks formatter parity and built Python help. Current
  release notes and package metadata describe this release's changes.

## Verification

- `dotnet test RAIkeep.slnx -p:UseLocalRAIkeepSources=true`: **1,071 passed,
  zero failed, zero skipped**, across eleven test assemblies.
- Release validator: **136 checks passed**.
- Isolated release-tool tests: **9 passed**; release order and Amafu recovery
  checks passed using stubs, without executing the actual chain.
- Markdown document links and standalone/shared formatter source parity passed.
- **11 NuGet artifacts** built at 4.5.15. Help/version checks on all five
  temporarily unpacked .NET tools confirmed colored help bodies with banners
  suppressed, plus plain redirected help without tabs.
- Both Python distributions built as wheels and source archives; Twine checks,
  temporary-environment version/help checks, and standalone checks passed.
- Cross-runtime checks cover fourteen syntax cases, banners, cloud badges,
  shared option rows, and three directory-export scenarios.

Builds and package smoke tests used temporary artifact directories. Installed
CLI versions and PATH entries remain unchanged.

## Prepared child commits

| Repository | Commit |
| --- | --- |
| Amafu | `6130739` |
| OsLib | `4f334a6` |
| RaiUtils | `a751ecd` |
| RaiImage | `d7b90d4` |
| RaiDiagram | `9857d82` |
| RaidSeeder | `36776c0` |
| JsonPit | `bf1b53b` |
| JsonPit.Python | `8820e78` |
| ImgSeeder | `53ed408` |
| PitSeeder | `841bef0` |
| RaiGuard | `6bf064b` |

The final umbrella commit records these exact child commits. All repositories
are on `main`; the release chain verifies their state again before publication.

## Provisioning after publication

Engenho owns fleet installation and upgrades. Do not run the legacy fleet
installation scripts as a release step. Until Engenho provisions the new
packages, existing bare commands may continue to resolve to older installations.

See the [release procedure](https://github.com/Burkhardt/RAIkeep/blob/main/RunReleaseChain.md)
and [CLI style guide](https://github.com/Burkhardt/RAIkeep/blob/main/doc/cli-style.md).
