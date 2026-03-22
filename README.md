# RAIkeep

`RAIkeep` is the umbrella workspace for the related `JsonPit`, `OsLib`, `RaiUtils`, and `RaiImage` libraries.

It keeps the child repositories available together for local integration work while preserving each package's own identity, solution files, and release flow.

## Current Aligned Version

The current aligned workspace version is `3.5.0` for:

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`

## 3.5.0 Decisions

- As of version `3.5.0`, the supported cloud-backed package stack in `RAIkeep` is `OneDrive`, `GoogleDrive`, and `Dropbox`.
- In `JsonPit`, `PitItem.Id` is now the canonical framework identifier.
- Legacy persisted items that still contain `Name` but not `Id` are normalized internally to `Id`, and the framework-managed `Name` field is dropped.
- Future use of `Name` as an application-defined custom field remains supported outside the framework identifier contract.

## Included repositories

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`

## Local validation

From the repository root:

- `dotnet test RAIkeep.slnx`
- `dotnet test RaiImage/RaiImage.slnx`
