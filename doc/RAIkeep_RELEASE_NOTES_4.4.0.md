# RAIkeep 4.4.0 Release Notes

RAIkeep 4.4.0 is the synchronized eight-package delivery of accepted
[`CR036_AIA_to_RAIkeep_Raid_CLI.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR036_AIA_to_RAIkeep_Raid_CLI.md).

## Raid model interchange

- Adds the independent `RaidCli` repository and NuGet tool package. Installing
  `RaidCli 4.4.0` provides the `raid` command.
- `raid import --puml <diagram.puml> [--out <dir>] [--name <id>]` imports modern
  PlantUML activity and class diagrams into canonical `.raid` plus hydratable
  `aim-*` SVG.
- `raid validate <file.raid|file.svg>` validates the manifest or public
  RaidCanvas hydration contract.
- RaiDiagram adds `IModelImporter`, `PlantUmlModelImporter`,
  `RaidDiagramModel`, typed deterministic canvas geometry, and `AimSvg`.
- The real `doc/ChangeRequestWorkflow.puml` fixture is covered end to end.

## Comment-tolerant seed files

`pits seed` accepts JSON5 line and block comments before the root array or
keyed object map. Parsing is deliberate and single-pass; malformed content is
still rejected rather than retried after broadly stripping text.

## Tag and GitHub Release synchronization

Beginning with v4.4.0, pushing the umbrella tag runs
`.github/workflows/publish-release.yml`. The workflow requires this exact notes
file and creates GitHub Release `RAIkeep v4.4.0`. The release chain waits for
and verifies that release before package tagging begins.

All filesystem reads and writes in `raid` remain on the OsLib boundary.
`TextReader`/`StringReader` are used only for in-memory parser interchange.
Publication remains behind RAI's manual `scripts/release-chain.sh 4.4.0` gate.
