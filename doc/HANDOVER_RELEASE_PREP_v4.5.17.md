# RAIkeep 4.5.17 release preparation

Prepared locally on 2026-11-02. This fresh coordinated release supersedes the
interrupted v4.5.16 publication. Existing v4.5.16 tags remain historical; the
manual chain will create new v4.5.17 tags on the prepared commits below.

## Start manually

```zsh
cd /Users/RSB/Projects/GitHub/RAIkeep
scripts/release-chain.sh 4.5.17
```

Use the established zsh release environment with GitHub CLI authentication and
`PYPI_TOKEN` available. The chain uses `~/.venvs/raikeep-release` and preflights
all repositories before publication. The umbrella is pushed and tagged last,
only after all children are published and visible. Engenho owns provisioning;
preparation does not install tools or execute the release chain.

## Recovery after RaiUtils upload

The user-run chain published Amafu and OsLibCore, then stopped at RaiUtils
workflow 41601478597. RaiUtils 4.5.17 was accepted by NuGet before a later push
failed: the broad artifacts wildcard also selected the tracked legacy packages
RaiUtils 2.3.1 and RaiUtilsCore 2.3.1. Trusted Publishing correctly refused the
unrelated RaiUtilsCore package. The earlier preflight missed these tracked
generated files; .gitignore does not exclude files already committed.

Both NuGet endpoints now return 200 for Amafu, OsLibCore and RaiUtils 4.5.17.
Resume manually with:

```zsh
scripts/release-chain.sh 4.5.17 --resume-after-raiutils
```

This mode verifies the three packages' availability and their existing remote
tags against the unchanged prepared child pointers, then starts at RaiImage.
It does not rerun RaiUtils's failed workflow, retag, or upload it again. The final
visibility check and umbrella-last publication remain mandatory.

Preflight now refuses tracked .nupkg and .snupkg artifacts in packages still to
be released. All eight remaining children were checked for these artifacts.
The RaiUtils correction is committed separately on the local branch
`codex/raiutils-package-scope`, commit
`6f148508ba23353b8e76fe192a48a54e38a3d570`, in
`/private/tmp/raikeep-raiutils-package-scope`. It removes the two tracked legacy
archives, packs into a run-specific temporary directory, validates the exact
package ID/version from its nuspec, and pushes one explicit filename.
Seven regression tests and actionlint passed. Hold that branch for the next
release preparation; do not change the v4.5.17 RaiUtils tag or current gitlink.
Recovery-order and failure-gate tests, plus tracked-artifact preflight tests,
passed without network or publication.

## Included changes

- CR076: Amafu configuration selectors for temp/backup paths, provider order,
  cloud roots and observer targets. Named queries emit clean scalar values;
  an absent order name returns 0. Contextual selector help works without a
  configuration. Top-level `amafu list all` is rejected.
- RAI's final cloud layout: provider badge/name at the left margin, then a
  newline and one literal tab before the double-quoted path. Provider glyphs
  and the cycling palette match the shared CLI formatter.
- OsLib, RaiUtils, RaiImage and JsonPit now publish through NuGet/login OIDC,
  without the expired static NUGET_API_KEY secret. All four workflows are named
  `publish-nuget.yaml`; all normal/recovery chain references use that filename.
- The workflow changes retain tag/version validation and add explicit immutable
  release-ref validation for manual recovery. Normal v4.5.17 publication uses
  each new v4.5.17 tag, not any old v4.5.16 source.
- CR075 media inventory/content matching and RAI002 file-size guidance from the
  interrupted v4.5.16 preparation are carried forward into this coordinated line.
- The release gate now checks the four publishing workflows and runs CR076
  selector regressions alongside CR075 and file-size regression tests.

## Verification

The final full solution run passed all 1,144 tests across eleven assemblies,
with zero failures and zero skips, including the live Mzansi synchronization
tests. The read-only chain preflight passed for all eleven children and the
umbrella; every child is committed and its umbrella pointer matches exactly.

Completed checks:

- 138 coordinated release checks passed, including Python tests, CLI parity,
  documentation, package versions, dependencies, formatter sync and new guards.
- Amafu: 110 tests passed. Live read-only queries returned 0 for an unlisted
  provider and rsb@Mzansi for the configured observer; configuration bytes and
  modification time were unchanged.
- Eleven NuGet packages built locally. All five packaged .NET CLI versions and
  redirected help verified; packaged Amafu's scalar/collection contracts and
  packaged iorg jq inventory/byte matching smoke checks passed.
- Both Python distributions built as wheels and source archives, passed Twine,
  and installed into an isolated temporary environment. Both entry points and
  standalone jpit report v4.5.17; no installed fleet tools were changed.
- Nine release-tool tests, four Trusted Publishing guard tests, actionlint,
  stubbed chain-order/Amafu-recovery tests, and Markdown-link checks passed.
- NuGet's private policy page was inspected read-only: the four new policies
  are active, scoped to their exact packages, and name publish-nuget.yaml.
  The user-run Amafu, OsLib and RaiUtils workflows have since demonstrated
  successful OIDC exchange and acceptance of their 4.5.17 packages.

The first 4.5.17 full run failed the existing Mzansi transfer test after an
incomplete remote seed/empty flag read. An unmodified isolated rerun passed.
The next full run exposed the underlying timing assumption: a renewed ticket
arrived after 375 seconds, beyond the production 60-second lease, so Mzansi
correctly took over while the test still expected Nkosikazi ownership.

The test now renews through the real configured cloud and requires a remote
ticket less than 20 seconds old before launching the client. It renews while
the client runs, checks remote seed success with the SSH wrapper's bounded
120-second timeout, and waits for post-seed ownership bytes. Production lease
duration and ownership assertions are unchanged. The corrected isolated live
test passed in 2m45s. No services, mounts, credentials, or cloud applications were
modified. The corrected final full suite passed, including all 229 JsonPit
tests; that assembly completed in 7m20s.

## Prepared child commits

| Repository | Commit |
| --- | --- |
| Amafu | `3386d424bb0bec120493985ea0a074002d2865ef` |
| OsLib | `46436c7f9fe29e005b10babb00151b50391a690b` |
| RaiUtils | `c5cad1e7e0981dd52a2bcdf05e6e58baf7483cd5` |
| RaiImage | `4cd8fc21e60b5dddfcc05a0be5de161e0a124ef7` |
| RaiDiagram | `04236ae3d47ec14dee635e85249b176e26d9b4f9` |
| RaidSeeder | `a01d6b6ca235c544e601883c799f50fa0d7d225a` |
| JsonPit | `5306b3efc463a1b2f095ae1ca9255128b04038ea` |
| JsonPit.Python | `697068e3fb9d77c1014d5b8ee3c8aa7ca606c4c1` |
| ImgSeeder | `550930302ab6ea920d419bcd1034829459a21736` |
| PitSeeder | `53fb7d40ecc99192390da946e4e19f1039e641bc` |
| RaiGuard | `7308af8de3d84d0fff6bc0d09041ce629165a894` |

## Local Amafu preview

The established preview path has been fast-forwarded and rebuilt for v4.5.17:

```zsh
dotnet /private/tmp/raikeep-amafu-list-config/amafu/bin/Debug/net10.0/amafu.dll -h
dotnet /private/tmp/raikeep-amafu-list-config/amafu/bin/Debug/net10.0/amafu.dll list cloud all -n
dotnet /private/tmp/raikeep-amafu-list-config/amafu/bin/Debug/net10.0/amafu.dll list order -h
```

Neither preview nor preparation changes installed tools. Source and artifacts
remain local until RAI starts the chain manually.
