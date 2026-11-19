# RAIkeep 4.6.6 release preflight

Verified November 18, 2026. This is a candidate for Rainer's manual Engenho run.
No release chain, publication, release tag or fleet provisioning was started by
this preparation. Version 4.6.6 was unused on all 14 distribution endpoints when
checked before the version bump.

## Contents

- Synchronize all 13 active package repositories, producing 11 NuGet packages
  and three PyPI distributions at 4.6.6.
- Put the SignPath Foundation application notice near the top of every tracked
  README and include it in registry package descriptions. The notice explicitly
  says that signing is not active.
- Publish the Windows artifact inventory, form text, NuGet/PyPI download links
  and Rita's signing integration handover.
- Add three Umgodi CR087 regression cases covering historical Save and CLI
  maintenance. The runtime fix was already released. Frozen jsonpit has only
  documentation changes and is not included in the release DAG.

## Verification

| Check | Result |
| --- | --- |
| `.release-venv/bin/python scripts/validate-release.py 4.6.6` | All 146 checks passed, including Python suites, CLI parity, workflow/ref guards and metadata |
| Local .NET solution tests | 1,255 passed; remote OneDrive replication suites excluded |
| Inqaba/Umgodi package preflight | 21 Inqaba and 220 Umgodi tests passed; wheel/sdist builds, Twine, fresh installation, imports, dependency checks and both CLI versions passed |
| Vikela | Suite passed through release validator; wheel/sdist builds, Twine, fresh installation, dependency check and CLI version passed |
| Release-tool tests | 9 passed |
| CLI style source synchronization | Passed |
| NuGet Release builds | All 11 packages built successfully using local coordinated sources |
| Package README inspection | All 11 NuGet and three wheel metadata descriptions contain the policy link and planned-signing notice |
| NuGet CLI installation | Fresh temporary tool-path installs of amafu, pits, iorg, raid and rail report 4.6.6 |
| Whitespace/diff checks | Passed across umbrella and components |

The full local .NET command was:

```sh
dotnet test RAIkeep.slnx -p:UseLocalRAIkeepSources=true \
  --filter 'FullyQualifiedName!~RemoteSyncTests&FullyQualifiedName!~RemoteCloudConcurrencyTests'
```

The initial sandboxed full run could not access OsLib's configured TempDir; the
verified run had the required local filesystem access. Isolated Python preflight
used its existing disposable configuration fixture. NuGet CLI smoke tests set
`DOTNET_ROOT` for the test processes to the same Homebrew .NET 10.0.14 runtime
used to build the candidate; the machine's other default runtime directory held
an older patch. No persistent runtime configuration was changed.

This verifies local candidate builds and installation on macOS. Windows signing
and Smart App Control acceptance remain future integration tests after Foundation
approval. The live remote replication suites were not run.

## Manual release and application follow-up

```sh
engenho release 4.6.6
```

After the chain succeeds, provisioning can be started separately:

```sh
engenho provision all --release 4.6.6
```

Verify the published NuGet/PyPI 4.6.6 pages and their rendered notices before
resuming the [SignPath application](SIGNPATH_APPLICATION.md). Use OsLibCore's
NuGet page as the form's Download URL. The application has not been submitted.
The [Rita handover](HANDOVER_TO_RITA_Engenho_SignPath.md) covers signing integration
and the generated global-tool launcher issue. Signing is not enabled by 4.6.6.
