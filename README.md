# RAIkeep

`RAIkeep` is the umbrella workspace for the related `JsonPit`, `OsLib`, `RaiUtils`, and `RaiImage` libraries.

It keeps the child repositories available together for local integration work while preserving each package's own identity, solution files, and release flow.

## Current Aligned Version

The current aligned workspace version is `3.7.3` for:

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`

## 3.7.3 Decisions

- Patch release: corrects the NuGet publish order. OsLibCore is now published before RaiUtils, RaiImage, and JsonPit.

## Included repositories

- `JsonPit`
- `OsLib`
- `PitSeeder`
- `RaiUtils`
- `RaiImage`

`PitSeeder` is included in the umbrella workspace so the CLI can build against the local `JsonPit` and `OsLib` source projects while package publishing catches up.

## Local validation

From the repository root:

- `dotnet build RAIkeep.slnx`
- `dotnet test RAIkeep.slnx`
- `dotnet test RaiImage/RaiImage.slnx`
