# RAIkeep 4.6.7 release preflight

Verified November 19, 2026. Version 4.6.7 was unused on all 14 distribution
endpoints before preparation. The preceding 4.6.6 Engenho release is complete.
This candidate does not start publication, create release tags or provision hosts.

## Changes

- Remove withdrawn signing-application notices and policy links from all 19
  tracked READMEs, package descriptions and current documentation. Remove the
  obsolete application, policy and integration handover files.
- Restore `HardCastle.png` as the C# JsonPit NuGet icon. It is identical to the
  existing OsLib and RaiImage castle. Remove misplaced Python artwork copies
  from C# JsonPit and retain the original Python artwork unchanged.
- Coordinate all 13 active repositories at 4.6.7. Frozen jsonpit receives only
  documentation cleanup and remains outside the release DAG.
- Record [future public-adoption work](PUBLIC_ADOPTION_ROADMAP.md). This is a
  backlog; no outreach or external service integration is initiated.

## Verification

| Check | Result |
| --- | --- |
| Release validator | All 146 checks passed, including Python suites, CLI parity and workflow/release guards |
| Full local .NET suite | 1,255 passed; both live remote replication suites excluded |
| Python pair preflight | 21 Inqaba and 220 Umgodi tests passed; builds, Twine, fresh installation, imports, dependency checks and CLI versions passed |
| Vikela | Suite passed through the release validator; build, Twine, clean install, dependency check and CLI version passed |
| Release-tool tests | 9 passed |
| CLI style source synchronization | Passed |
| NuGet Release packages | All 11 built successfully using local coordinated sources |
| Packaged documentation | All 11 NuGet READMEs, three wheel descriptions and three Python source-distribution documentation sets checked for removed notices and links |
| JsonPit icon | Nuspec references `HardCastle.png`; embedded bytes match OsLib and RaiImage; no Python logo packaged |
| NuGet tool installation | Temporary clean installs of amafu, pits, iorg, raid and rail report 4.6.7 |
| Current tracked source/docs | No withdrawn provider references or policy links remain across umbrella and components; whitespace checks passed |

The full .NET suite used the existing configured local fixture directories with
filesystem access beyond the workspace sandbox. Python preflight used its
disposable configuration fixture. Temporary NuGet tool installs selected the
Homebrew .NET runtime through process-local `DOTNET_ROOT`; persistent machine
configuration was unchanged. These are macOS checks, not Windows signing tests.
Published historical packages and tags were not modified.

## Manual release

```sh
engenho release 4.6.7
```

After successful publication:

```sh
engenho provision all --release 4.6.7
```

NuGet and PyPI will display the updated documentation and icon after the new
packages are published and indexed. Earlier immutable package versions retain
their original packaged content.
