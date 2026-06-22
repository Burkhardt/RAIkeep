# CURRENT-STATUS

This file captures the current release-ready status of the `RAIkeep` workspace for the coordinated `3.11.1` patch line.

## Current focus

- Carry the already-prepared `3.11.0` workspace line forward to the next patch, `3.11.1`.
- Keep the release order unchanged: `OsLibCore -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- Keep `ImgSeeder`/`iorg` immediately before `PitSeeder` everywhere in docs, release notes, and release-prep notes.

## Completed in this run

- Local child repo heads are now:
  - `OsLib`: `c768c4b`
  - `RaiUtils`: `4f734d4`
  - `RaiImage`: `1d3a13e`
  - `JsonPit`: `104284b`
  - `ImgSeeder`: `b86da4f`
  - `PitSeeder`: `50a41ae`
- Added `RELEASE_NOTES_3.11.1.md` to every child repo/package.
- Refreshed `3.11.1` release wording in current package docs where this run still had control.
- Regenerated the tracked PlantUML SVGs that changed in this run.

## Validation

Previous `3.11.0` workspace notes recorded successful sequential validation and partial GitHub pushes, but this `3.11.1` run could not repeat those checks in the current sandbox.

Attempts blocked in this run:

- `dotnet test OsLib/OsLib.slnx --nologo -v minimal`
- `dotnet test RaiUtils/RaiUtils.slnx --nologo -v minimal`
- `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal`
- `dotnet test JsonPit/JsonPit.slnx --nologo -v minimal`
- `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal`
- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal`
- `dotnet test RAIkeep.slnx --nologo -v minimal`
- `dotnet vstest <existing test dll>`

Observed failure mode:

```text
System.Net.Sockets.SocketException (13): Permission denied
```

Additional note:

- Existing prebuilt `iorg` and `pits` binaries still report `3.9.1`, so they are stale artifacts and not valid `3.11.1` verification.

## Git and publishing state

- No `3.11.1` child repo commits were pushed from this run.
- No parent `RAIkeep` push was possible from this run.
- No `3.11.1` Sequential NuGet Release Chain run was dispatched.
- Shell GitHub access fails with:

```text
fatal: unable to access 'https://github.com/Burkhardt/<repo>.git/': Could not resolve host: github.com
```

- `gh auth status` also reports an invalid token in this session.
- The GitHub app is authenticated for inspection, but this session has no workflow-dispatch tool for the parent sequential release chain.

## Suggested resume prompt

```text
Please read CURRENT-STATUS.md first, then continue the prepared 3.11.1 umbrella patch release in an environment with working GitHub DNS/network access and .NET test socket support. Push the child repos in order, update the parent submodule pointers, and dispatch the parent Sequential NuGet Release Chain with publish_to_nuget=true.
```
