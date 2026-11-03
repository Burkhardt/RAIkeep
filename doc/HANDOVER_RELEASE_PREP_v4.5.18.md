# RAIkeep 4.5.18 release preparation

Prepared locally on 2026-11-03 for RAI's manual release-chain run.
Preparation does not push, tag, publish, install tools, or provision machines.
Engenho remains responsible for provisioning after publication.

## Start manually

```zsh
cd /Users/RSB/Projects/GitHub/RAIkeep
scripts/release-chain.sh 4.5.18
```

Use the established release environment with GitHub CLI authentication and
`PYPI_TOKEN` available. The chain uses `~/.venvs/raikeep-release`, checks every
prepared child first, publishes in dependency order, and publishes the umbrella
last after all exact package versions are available. Existing v4.5.17 tags are
unchanged; this release creates new v4.5.18 tags on the prepared commits.

## Included changes

- Amafu, pits, iorg, raid, rail, jsonpit and jpit end their human-readable
  banner headings with `on <machine>`. The value comes from the executing
  operating system, including its own hostname under WSL, rather than an
  Observer alias. Version-only, scalar and JSON output do not acquire a banner.
- The complete heading remains bold cyan. Both regular cyan decorative rules
  match its full visible width, including short headings and the machine name.
  The C# formatter and standalone Amafu copy remain identical; Python uses the
  same rule. The approved contract is recorded in
  [cli-style.md](https://github.com/Burkhardt/RAIkeep/blob/main/doc/cli-style.md).
- RaiUtils removes its tracked legacy 2.3.1 packages. Its publishing workflow
  packs into a run-specific temporary directory, checks that the only package
  has the expected filename and embedded package ID/version, and uploads that
  explicit filename. This incorporates the isolated correction from the
  completed v4.5.17 recovery; no old tag is rewritten.
- Release preflight rejects tracked NuGet packages and symbol packages.
  The validator now runs those checks, recovery-order failure gates, the
  RaiUtils package-selection regressions, and real CLI banner-width checks.
  Python artifact checks verify the installed entry points and standalone
  binary, including their new banner text and rule lengths.

## Verification

The read-only chain preflight passed for the umbrella and all eleven children.
The final full solution suite passed all 1,144 tests across eleven assemblies,
with zero failures and zero skips, including all 229 JsonPit tests. The first
run passed 1,143 tests
and failed one existing Mzansi master-transfer test when its remote seed exceeded
the unchanged 120-second SSH timeout. Its first three phases passed. The same
live test then passed all phases unchanged in 3m22s. The final full-suite rerun
then passed. No source, configuration, service or timeout changes were made
to obtain these passes.
Completed checks:

- All 141 release checks passed, including real CLI headings/rule widths,
  Python parity and the publication/recovery regressions.
- Real-PTY output confirmed matching cyan rules and a bold cyan complete
  host heading in every CLI implementation.
- Eleven NuGet packages built locally; all five packaged .NET CLI banners,
  exact versions, plain redirected output and no-logo behavior passed.
- Both Python distributions and the standalone CLI passed build, Twine,
  isolated installation, version and banner checks. No installed fleet tools
  were changed.
- Nine release-tool tests, four Trusted Publishing guard tests, seven RaiUtils
  package-scope tests, actionlint, recovery-order/failure gates, tracked-package
  guards, shared formatter synchronization and Markdown-link checks passed.
- All twelve remote repositories were checked: v4.5.18 is unused.

## Prepared child commits

| Repository | Commit |
| --- | --- |
| Amafu | `14b32ff505640738ff0bb664db31de6fef01d4ce` |
| OsLib | `273b222233cf4101688ec89eda169eee92545374` |
| RaiUtils | `50a0fa31610d7b317f7820cd2eb540c68052b910` |
| RaiImage | `1c9757fe46315ec7791642b44c119dba7d5a9c6a` |
| RaiDiagram | `9748fdd72b8855163fb958ca6a9a2f5c25f55907` |
| RaidSeeder | `2511601e0debfa7dd73a1577b450b6db790744f0` |
| JsonPit | `4bf4439ef07887dec825683830d8d71097ce18c0` |
| JsonPit.Python | `4e326ab5eb7879129d94d4f2fb778faba8c5988b` |
| ImgSeeder | `042b3314dc3fa9f599ceabf1a15696f0f3ae730e` |
| PitSeeder | `f98e2fa626641f79bdcd668ccd5ebe5279ffe126` |
| RaiGuard | `044259a3aea46c15b5442106d19c40da1ca6800a` |

## Local preview

```zsh
env -u NO_COLOR bash scripts/preview-cli-help.sh all
```

This runs the locally built binaries and Python checkout. It does not update
installed tools. The established Amafu preview path has also been refreshed to
the final v4.5.18 source:

```zsh
env -u NO_COLOR dotnet /private/tmp/raikeep-amafu-list-config/amafu/bin/Debug/net10.0/amafu.dll -h
```
