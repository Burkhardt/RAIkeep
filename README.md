# RAIkeep

## Candidate 4.6.2 — CR078 and CR081

`rail` now inspects every supplied source path; `pits` and `jpit` report written
and unchanged source entries after required local persistence. See the
[formal implementation and preparation report](doc/RAIkeep_RELEASE_NOTES_v4.6.2.md).
Consumer CDAT is pending. Rainer runs release and provisioning manually through
Engenho after acceptance; preparation does not authorize publication or installation.

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

The prepared coordinated release is `4.6.2`. CR078 fixes multi-path coverage in
`rail`; CR081 adds truthful seed disposition counts and post-persistence receipts
in `pits` and `jpit`. All twelve child repositories, including optional Vikela,
share the same version and synchronized package dependencies.

Preparation includes local tests, metadata checks and candidate packaging.
Consumer acceptance precedes publication. Engenho owns manual release and
separately selected provisioning; neither operation runs during preparation.

## Documentation

New to `pits`? Follow [First steps with pits](https://github.com/Burkhardt/RAIkeep/blob/main/doc/FirstSteps_pits.md) to create a pit in iCloud Drive and fill it with weather data from a `curl` call.

All change requests and release notes are centralized in [`doc/`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/README.md). Child repositories should not contain independent `CR_*.md` or `RELEASE_NOTES*.md` files.

The [RAIkeep Manifesto](https://github.com/Burkhardt/RAIkeep/blob/main/MANIFESTO.md)
explains why transparent, historical JSON matters for agentic engineering and
defines JsonPit's asynchronous persistence and eventual-durability model.

Prepared 4.6.2 release notes:

- [Amafu 4.6.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/Amafu_RELEASE_NOTES_4.x.md#462)
- [OsLibCore 4.6.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/OsLib_RELEASE_NOTES_4.x.md#462)
- [RaiUtils 4.6.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiUtils_RELEASE_NOTES_4.x.md#462)
- [RaiImage 4.6.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiImage_RELEASE_NOTES_4.x.md#462)
- [RaiDiagram 4.6.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiDiagram_RELEASE_NOTES_4.x.md#462)
- [RaidSeeder 4.6.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaidSeeder_RELEASE_NOTES_4.x.md#462)
- [JsonPit 4.6.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/JsonPit_RELEASE_NOTES_4.x.md#462)
- [JsonPit.Python 4.6.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/JsonPit.Python_RELEASE_NOTES_4.x.md#462)
- [ImgSeeder 4.6.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/ImgSeeder_RELEASE_NOTES_4.x.md#462)
- [PitSeeder 4.6.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/PitSeeder_RELEASE_NOTES_4.x.md#462)
- [RaiGuard 4.6.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RaiGuard_RELEASE_NOTES_4.x.md#462)
- [RAIkeep 4.6.2](https://github.com/Burkhardt/RAIkeep/blob/main/doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md#462)

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

Rainer runs Engenho manually after the owning consumer accepts the candidate.
Provider implementation, tests, local commits and package builds do not constitute
consumer signoff and do not authorize publication or installation.

After CDAT acceptance, the manual release invocation is:

```zsh
cd /Users/RSB/Projects/GitHub/RAIkeep
engenho release 4.6.2
```

The manifest is `scripts/release-manifest.json`. All prepared child commits and
exact submodule pointers must be committed on umbrella `main` before execution.
Engenho publishes children in dependency order and creates the umbrella tag only
after package visibility gates pass. No tags are moved during preparation.

Provisioning is a separate manual Engenho operation after publication. Consult
Rita's current provisioning instructions for target selection; do not run the
legacy install script. The old shell chain remains historical recovery tooling,
not the v4.6.2 release procedure.

## Working conventions

- Preserve the real machine configuration file as the source of truth; do not substitute environment variables or rewrite configuration for test isolation.
- Keep the shared configured cloud-root contract aligned on `Dropbox`, `OneDrive`, `GoogleDrive`, and `ICloudDrive`.
- Use OsLib path/file abstractions in JsonPit and the CLIs instead of introducing direct filesystem operations where an OsLib API applies.
- Follow the mandatory [cloud-storage in-place invariant](https://github.com/Burkhardt/RAIkeep/blob/main/doc/Cloud-Storage-In-Place-Invariant.md): never move a TempDir-created file or directory into a configured cloud tree, and never replace an established cloud pathname as an implementation detail.
- Keep one in-memory `Pit` instance per distinct pit path in a long-running process and share it through the application container/singleton mechanism.
