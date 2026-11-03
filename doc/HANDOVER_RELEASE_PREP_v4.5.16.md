# RAIkeep 4.5.16 release preparation

Prepared on 2026-11-02. CR075 is implemented; publication remains at RAI's manual gate.

## Start manually

```zsh
cd /Users/RSB/Projects/GitHub/RAIkeep
scripts/release-chain.sh 4.5.16
```

Use the established zsh release environment with GitHub authentication and
`PYPI_TOKEN` available. The chain uses `~/.venvs/raikeep-release`. The prepared
children and umbrella are committed locally; preparation does not push main,
create tags, dispatch publication or install tools. The umbrella remains last.
Engenho owns provisioning after the packages have been published.

## Included changes

- CR075: `iorg list --long --json`, optional `--checksum sha256`, metadata-only
  `--all-files`, case-insensitive pattern selection, and execution-host provenance.
  Existing filename JSON remains unchanged.
- `iorg duplicates`: streamed size/SHA-256/byte confirmation, or explicit
  `--match visual --visual-profile strict-v1`. Literal selectors return arrays;
  wildcard selectors return relative-path dictionaries with empty unique entries.
- Shared typed inventory and evidence models, cloud-relative request factories
  that resolve on the execution host, and bounded decoder process pipes.
- RAI002 file-size guidance and a semantic Roslyn code fix for `RaiFile.Length`.
- The release gate now runs CR075 and file-size regression tests before publishing.

Visual comparison uses complete frames, with audio explicitly excluded. The
profile's eight-million-pixel bound, SDR/alpha/tool restrictions, normalization
and SSIM thresholds are documented in
[IORG-OPERATIONS.md](https://github.com/Burkhardt/RAIkeep/blob/main/doc/IORG-OPERATIONS.md#cr075-structured-inventory-and-content-matching).
Unsupported/incomplete comparisons fail instead of reporting false uniqueness.
Visual matches do not authorize canonical file replacement. AIA and Engenho
consumer migrations are separate from this substrate release.

## Verification

- Final `dotnet test RAIkeep.slnx -p:UseLocalRAIkeepSources=true`: **1,103 passed,
  zero failed, zero skipped**, across eleven assemblies. The final iorg-only run
  also passed all **92** tests after the help clarification.
- **137 coordinated release checks passed**, including CR075 and file-size tests,
  formatter parity, Python tests, pits/jpit parity and packaged OsLib contracts.
- Python: **125 passed**. Run pytest from `JsonPit.Python`, or use the validator's
  configured Python module path; invoking it from the umbrella without that path
  does not import the source package correctly.
- **11 NuGet packages** built. Unpacked tool checks verified all five CLI versions
  and plain redirected help. Packaged iorg inventory piped through real jq, and
  literal/wildcard byte searches preserved source contents and modification times.
- Both Python packages built as wheels and source archives; Twine validation,
  isolated installation, both entry-point versions/help and standalone jpit passed.
- Release-tool tests: **9 passed**. Stubbed release-order and Amafu recovery tests,
  absolute Markdown links and shared/standalone formatter checks passed.
- Typed `IorgCommand` SSH tests ran against Ingwe's **actual configured iCloudDrive**:
  structured inventory returned five MOV files with Ingwe provenance and byte
  discovery returned a valid five-source dictionary. An unpublished runtime was
  staged under `/tmp`; installed CLIs and provider configuration were untouched.

The first full run hit an existing Mzansi master-handover assertion with an empty
flag read. An isolated retry passed, followed by the final full solution passing
all 1,103 tests. No mounts, cloud applications or authentication settings were
changed to obtain that result.

Verification logs and package artifacts are under `/private/tmp/raikeep-4516-*`
on the preparation machine. They are temporary evidence, not release assets
uploaded by this preparation.

## Consumer adoption

Use `IorgListRequest.ForCloud(pattern, cloud)` with `Long = true`, `Json = true`
and optionally `IgnoreCase = true` / `Checksum = "sha256"`. `.OverSsh(target)` or
request `Options.RemoteTarget` delegates to that host's configuration. Do not
construct controller-local paths for a remote CloudDrive request.

Engenho can replace its secondary Deno.stat inventory pass with these records,
mapping the PascalCase DTO fields to its existing response contract. AIA's
existing `master.Length` comparison remains only a size check: byte-identity
choices require byte-mode evidence. Visual evidence has AudioCompared false and
must stay distinct from file identity. Cross-host inventories are observations,
not a synchronization barrier or a distributed filesystem lock.

## Prepared child commits

| Repository | Commit |
| --- | --- |
| Amafu | `1965150` |
| OsLib | `fffd0a8` |
| RaiUtils | `eaa0acc` |
| RaiImage | `0cde6ab` |
| RaiDiagram | `cb4a901` |
| RaidSeeder | `0bbd34a` |
| JsonPit | `de2e576` |
| JsonPit.Python | `2358612` |
| ImgSeeder | `980e86b` |
| PitSeeder | `4bdcf67` |
| RaiGuard | `0a3070b` |

The final umbrella commit records these exact child commits. Its preflight checks
all repository branches, clean state, remote ancestry, version consistency and
matching pointers before the user's chain can start publishing.
