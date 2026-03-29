# RAIkeep

`RAIkeep` is the umbrella workspace for the related `JsonPit`, `OsLib`, `RaiUtils`, and `RaiImage` libraries.

It keeps the child repositories available together for local integration work while preserving each package's own identity, solution files, and release flow.

## Current Aligned Version

The current aligned workspace version is `3.7.0` for:

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`

## 3.7.0 Decisions

- Patch release: corrects the NuGet publish order. OsLibCore is now published before RaiUtils, RaiImage, and JsonPit.

## Included repositories

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`

## Local validation

From the repository root:

- `dotnet test RAIkeep.slnx`
- `dotnet test RaiImage/RaiImage.slnx`
