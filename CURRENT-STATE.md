# CURRENT-STATE

This file captures the current working state of the `RAIkeep` umbrella workspace after the coordinated `3.11.2` patch-release prep pass.

## Active line

The active coordinated line is `3.11.2` for:

- `OsLib`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder`
- `PitSeeder`

## What changed in this run

- Added `RELEASE_NOTES_3.11.2.md` to all six child repos/packages.
- Preserved the coordinated package order `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- Regenerated the tracked SVG renders for the PlantUML files changed in this run.
- Updated the root dependency diagrams so current package overviews show `WordCase` instead of the retired `CamelCase` type.
- Carried forward the already-prepared `3.11.0` workspace state to the next patch line `3.11.2`.

## Local child heads

- `OsLib` -> `c768c4b`
- `RaiUtils` -> `4f734d4`
- `RaiImage` -> `1d3a13e`
- `JsonPit` -> `104284b`
- `ImgSeeder` -> `b86da4f`
- `PitSeeder` -> `50a41ae`

These heads are local-only from the perspective of this run; push status could not be advanced because `github.com` DNS resolution failed in the shell.

## Validation note

- Earlier workspace notes for `3.11.0` record successful sequential validation, but this run could not repeat .NET validation in the current sandbox.
- Both `dotnet test` and `dotnet vstest` fail before execution with `System.Net.Sockets.SocketException (13): Permission denied`.
- Existing prebuilt `iorg` and `pits` binaries still report `3.9.1`, so they are not suitable evidence for the new line.

## Parent repo note

- The parent repo can carry the updated submodule pointers locally.
- The parent remote push and the Sequential NuGet Release Chain dispatch still require a working GitHub network path and a workflow-dispatch-capable session.

## Suggested resume prompt

```text
Please read CURRENT-STATE.md first. Continue the local 3.11.2 release-prep pass in an environment that allows GitHub network access and .NET test socket creation, then push the child repos in order, update the parent submodule pointers, and dispatch the parent Sequential NuGet Release Chain with publish_to_nuget=true.
```
