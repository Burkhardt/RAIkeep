# RAIkeep

`RAIkeep` is the umbrella workspace for the related `JsonPit`, `OsLib`, `RaiUtils`, and `RaiImage` libraries.

It keeps the child repositories available together for local integration work while preserving each package's own identity, solution files, and release flow.

## Current Aligned Version

The current aligned workspace version is `3.6.0` for:

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`

## 3.6.0 Decisions

- As of version `3.6.0`, `OsLib` fixes the `CanonicalFile` constructor crash that caused a `StackOverflowException` on directory-style paths.
- All four packages advance to version `3.6.0` together on the aligned package line.

## Included repositories

- `JsonPit`
- `OsLib`
- `RaiUtils`
- `RaiImage`

## Local validation

From the repository root:

- `dotnet test RAIkeep.slnx`
- `dotnet test RaiImage/RaiImage.slnx`
