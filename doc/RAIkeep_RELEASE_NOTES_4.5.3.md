# Release Notes: RAIkeep v4.5.3

RAIkeep 4.5.3 delivers CR051: multi-account cloud storage discovery, named shortcuts, deterministic personal OneDrive selection, noninteractive configuration reconciliation, and OsLib recognition of arbitrary named cloud roots. All nine C# packages and internal package dependencies align to 4.5.3. JsonPit distributed persistence and live-object mutation behavior remain unchanged.

## Multi-account discovery and reconciliation (CR051)

- **Multiple Google Drive accounts**: Discovers all Google Drive accounts (e.g. `GoogleDrive-rainer.burkhardt@gmail.com` -> `GoogleDriveRainer`, `GoogleDrive-yebo@umshadisi.com` -> `GoogleDriveYebo`). Each account independently selects its `GDriveData` subfolder, or `My Drive` when absent.
- **Multiple OneDrive accounts**: Discovers personal and corporate OneDrive roots. Exactly one personal OneDrive root is selected under the compatible `OneDrive` key; corporate roots (e.g. `OneDriveAfricaStage`, `OneDriveContoso`) retain independent qualified keys.
- **Deterministic personal OneDrive selection**: Explicit `--onedrive-personal <folder>` takes precedence; otherwise an existing valid configured root is retained; otherwise the longest folder name wins (with highest numeric suffix and ordinal path order as tie-breakers). Commands never prompt interactively.
- **Noninteractive reconciliation**: `amafu reconcile` previews newly discovered accounts and migration to `~/.CloudStorage` shortcuts without writes. `amafu reconcile --apply` creates shortcuts, backs up existing configuration with a unique timestamped suffix, and safely updates `Cloud` and `DefaultCloudOrder` while preserving all unrelated JSON5 settings, comments, and order.
- **Collision safety**: Case-insensitive account name collisions report both conflicting roots and fail before filesystem writes. Duplicate aliases of the same physical root are deduplicated.
- **Symbolic shortcut classification**: OsLib's `ConfiguredCloudPaths` reads all configured string roots in `Cloud` without provider enum restrictions, and resolves symbolic links and existing ancestors so `~/.CloudStorage` shortcuts receive cloud-safe in-place atomic writes.
- **CLI account key resolution**: PitSeeder (`pits -c <name>`) accepts any configured account key in `Cloud` and `DefaultCloudOrder`.

## Coordinated Package Alignment

All nine C# packages align to the 4.5.3 line:
- `Amafu` 4.5.3: multi-account discovery, reconciliation, personal OneDrive selection.
- `OsLibCore` 4.5.3: unrestricted string cloud roots, symbolic link classification.
- `RaiUtils` 4.5.3: synchronized dependency alignment.
- `RaiImage` 4.5.3: synchronized dependency alignment.
- `RaiDiagram` 4.5.3: synchronized diagram line alignment.
- `RaidSeeder` 4.5.3: synchronized CLI and dependency alignment.
- `JsonPit` 4.5.3: synchronized persistence line alignment.
- `ImgSeeder` 4.5.3: synchronized CLI and dependency alignment.
- `PitSeeder` 4.5.3: multi-account CLI resolution and synchronized alignment.

## Python Parity & Coordination

Adele coordinates `jsonpit-python`/`jpit` 4.5.3 separately. Python `jsonpit` is updated to 4.5.3 with link-resolving cloud path classification matching OsLib, and published to PyPI prior to deployment. The C# release chain publishes only the .NET stack.

## Verification

- **Amafu**: 60 passed, 0 failed, 0 skipped.
- **OsLib**: 147 passed, 0 failed, 0 skipped.
- **PitSeeder**: 87 passed, 0 failed, 0 skipped.
- Release validator: all checks passed.
- Preflight clean across all nine component repositories.
