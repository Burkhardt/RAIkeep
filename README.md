# RAIkeep

## CR070 in 4.6.1

RAIkeep 4.6.1 adds Os.RunSwitch for process-invocation opt-ins and justified,
rule-specific method/class exemptions in RaiGuard. See the
[CR070 acceptance and release handover](doc/HANDOVER_CR070_RunSwitch_and_Declared_Rule_Exemptions.md).
The suite, including optional Vikela, shares the same 4.6.1 version. Publication
uses `engenho release 4.6.1`; provisioning remains separate.

## CR077 and Vikela release orchestration

RAIkeep 4.6.0 includes optional [Vikela 4.6.0](vikela/README.md) Python development
guardrails. [CR077](doc/CR077_AIA_and_AfricaStage_to_RAIkeep_Vikela_and_JsonPit_Mutation_Guardrails.md)
governs implementation. Publication and selective provisioning use Rita's Engenho
runner; see the [CR077 handover](doc/HANDOVER_TO_RITA_Engenho_CR077_Vikela.md).
The legacy shell chain does not publish Vikela. Development lint tooling is not
installed on production servers by default.


## Terminal font for RAIkeep CLIs

Amafu (`amafu`), RaidSeeder (`raid`), ImgSeeder (`iorg`), PitSeeder (`pits`), and RaiGuard (`rail`) use embedded Nerd Font provider and numbered-option glyphs in their help output. Installation instructions for Blink on iPadOS, macOS, and Ubuntu—including the Blink CSS font-family stylesheet URL—are in [TERMINAL_FONTS.md](https://github.com/Burkhardt/RAIkeep/blob/main/doc/TERMINAL_FONTS.md).

`RAIkeep` is the umbrella workspace for shared .NET libraries and six command-line tools:

| Order | Repository | Package / command | Current or upcoming role |
|---:|---|---|---|
| 1 | `Amafu` | `Amafu` / `amafu` | Cloud configuration |
| 2 | `OsLib` | `OsLibCore` | Filesystem and system abstractions |
| 3 | `RaiUtils` | `RaiUtils` | Shared utilities |
| 4 | `RaiImage` | `RaiImage` | Image naming and tree paths |
| 5 | `RaiDiagram` | `RaiDiagram` | Diagram models and rendering |
| 6 | `RaidSeeder` | `RaidSeeder` / `raid` | Diagram artifact commands |
| 7 | `JsonPit` | `JsonPit` | Historical JSON persistence |
| 8 | `JsonPit.Python` | `jsonpit`, `jpit` / `jpit`, `jsonpit` | Python persistence and pit commands |
| 9 | `ImgSeeder` | `ImgSeeder` / `iorg` | Image organization and import |
| 10 | `PitSeeder` | `PitSeeder` / `pits` | Pit commands |
| 11 | `RaiGuard` | `RaiGuard`, `RaiGuard.Analyzer` / `rail` | Roslyn analysis and source refactoring |

Each child remains its own Git repository, package, solution, and release
workflow. The umbrella workspace supplies local project wiring, coordinated
validation, dependency-order documentation, and sequential release automation.

## Current release line

The prepared coordinated release is `4.6.1`. CR075 adds structured media
inventory and read-only byte/visual content matching. RAI002 now gives specific
file-size guidance and a semantic RaiFile.Length replacement. All child package
versions and dependencies remain aligned.

All five C# CLI tools and the Python `jpit` CLI are coordinated through this
umbrella. The release chain validates the `jsonpit` Python test suite, checks
`pits list` / `jpit list` parity, and publishes both matching PyPI distributions
beside the NuGet packages.

All eleven child repositories participate in the coordinated line so fallback
package dependencies remain aligned throughout the release order. Engenho owns
fleet provisioning after publication; release preparation and the release chain
do not install or upgrade tools on hosts.

## Documentation

New to `pits`? Follow [First steps with pits](https://github.com/Burkhardt/RAIkeep/blob/main/doc/FirstSteps_pits.md) to create a pit in iCloud Drive and fill it with weather data from a `curl` call.

All change requests and release notes are centralized in [`doc/`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/README.md). Child repositories should not contain independent `CR_*.md` or `RELEASE_NOTES*.md` files.

The [RAIkeep Manifesto](https://github.com/Burkhardt/RAIkeep/blob/main/MANIFESTO.md)
explains why transparent, historical JSON matters for agentic engineering and
defines JsonPit's asynchronous persistence and eventual-durability model.

Prepared 4.6.1 release notes:

- [Amafu 4.6.1](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/Amafu_RELEASE_NOTES_4.x.md#461)
- [OsLibCore 4.6.1](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/OsLib_RELEASE_NOTES_4.x.md#461)
- [RaiUtils 4.6.1](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiUtils_RELEASE_NOTES_4.x.md#461)
- [RaiImage 4.6.1](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiImage_RELEASE_NOTES_4.x.md#461)
- [RaiDiagram 4.6.1](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiDiagram_RELEASE_NOTES_4.x.md#461)
- [RaidSeeder 4.6.1](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaidSeeder_RELEASE_NOTES_4.x.md#461)
- [JsonPit 4.6.1](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/JsonPit_RELEASE_NOTES_4.x.md#461)
- [JsonPit.Python 4.6.1](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/JsonPit.Python_RELEASE_NOTES_4.x.md#461)
- [ImgSeeder 4.6.1](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/ImgSeeder_RELEASE_NOTES_4.x.md#461)
- [PitSeeder 4.6.1](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/PitSeeder_RELEASE_NOTES_4.x.md#461)
- [RaiGuard 4.6.1](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiGuard_RELEASE_NOTES_4.x.md#461)
- [RAIkeep 4.6.1](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#461)

The prior coordinated line remains documented in [RAIkeep 4.1.0 release notes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#410).

Flag and coordination behavior is documented in [JsonPit flag files and concurrency](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit-FlagFiles-And-Concurrency.md). It explains the distinction between per-process activity windows and the stable master-writer lease without replacing the separate open concurrency CR.

## Local validation

From the workspace root:

```bash
dotnet build RAIkeep.slnx
dotnet test Amafu/Amafu.slnx
dotnet test OsLib/OsLib.Tests/OsLib.Tests.csproj
dotnet test RaiUtils/RaiUtils.slnx
dotnet test RaiImage/RaiImage.slnx
dotnet test RaiDiagram/RaiDiagram.slnx
dotnet test RaidSeeder/RaidSeeder.slnx
dotnet test JsonPit/JsonPit.slnx
dotnet test ImgSeeder/ImgSeeder.slnx
dotnet test PitSeeder/PitSeeder.slnx
```

The JsonPit suite includes real cloud/remote scenarios and a separately documented open concurrency regression. Use the validation scope stated in the JsonPit release notes rather than hiding those distinctions behind incidental test-runner parallelism or local configuration substitution.

## Release execution

For CR077 / 4.6.0 and Vikela 4.6.0, use Engenho with the
[handover for Rita](doc/HANDOVER_TO_RITA_Engenho_CR077_Vikela.md). The script
reference below records the previous mechanism; it is not the CR077 launch command.

Publication requires explicit approval. Preparing versions, documentation, commits, or packages does not authorize a push, tag, workflow dispatch, or NuGet publication.

### Previous local script (reference only)

The existing script remains available for earlier release recovery. Its invocation shape is:

```bash
cd /Users/RSB/Projects/GitHub/RAIkeep
scripts/release-chain.sh 4.6.1
```

Before publication begins, all eleven child release commits and their exact submodule pointers must already be committed on the umbrella `main`. The script preflights that state, then publishes each child in dependency order. Only after every child package is visible does it push and tag the umbrella commit. The umbrella tag creates the synchronized GitHub Release; it publishes no NuGet package.

It then processes packages in this exact order:

```text
Amafu → OsLibCore → RaiUtils → RaiImage → RaiDiagram → RaidSeeder → JsonPit → JsonPit.Python → ImgSeeder → PitSeeder → RaiGuard → RAIkeep umbrella
```

The Python `jsonpit` and `jpit` distributions follow C# `JsonPit` and are published to
PyPI before ImgSeeder and PitSeeder. Preflight builds both packages, checks their
installed commands and standalone download, and validates their documentation.
The chain also creates the Python GitHub Release. Set `PYPI_TOKEN` in the release
environment; the chain supplies it to Twine without placing it on the command
line.

For every package before the next repository is pushed/tagged:

1. Push the prepared repository `main` only if it is ahead.
2. Push that repository's requested version tag, such as `v4.5.2`, to trigger its publish workflow.
3. Wait for the matching GitHub workflow to finish successfully.
4. Verify the exact `.nupkg` and exact-version registration document are both visible from NuGet with HTTP `200`.
5. Only then continue to the next repository.

The chain waits on observed NuGet and PyPI availability rather than a fixed delay. Do not run multiple release mechanisms for the same version. The local script refuses to move an existing conflicting version tag and verifies the prepared submodule pointers before it tags the umbrella.

Detailed operational guidance is in [RunReleaseChain.md](https://github.com/Burkhardt/RAIkeep/blob/main/RunReleaseChain.md).

## Working conventions

- Preserve the real machine configuration file as the source of truth; do not substitute environment variables or rewrite configuration for test isolation.
- Keep the shared configured cloud-root contract aligned on `Dropbox`, `OneDrive`, `GoogleDrive`, and `ICloudDrive`.
- Use OsLib path/file abstractions in JsonPit and the CLIs instead of introducing direct filesystem operations where an OsLib API applies.
- Follow the mandatory [cloud-storage in-place invariant](https://github.com/Burkhardt/RAIkeep/blob/main/doc/Cloud-Storage-In-Place-Invariant.md): never move a TempDir-created file or directory into a configured cloud tree, and never replace an established cloud pathname as an implementation detail.
- Keep one in-memory `Pit` instance per distinct pit path in a long-running process and share it through the application container/singleton mechanism.
