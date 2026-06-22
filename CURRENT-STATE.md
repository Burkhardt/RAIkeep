# CURRENT-STATE

This file captures the current working state of the `RAIkeep` umbrella workspace after the coordinated `3.11.0` release-prep pass.

## Active line

The active coordinated line is `3.11.0` for:

- `OsLib`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder`
- `PitSeeder`

## What changed

- Every child repo now has a `3.11.0` package version and a matching `RELEASE_NOTES_3.11.0.md`.
- Downstream fallback dependency defaults now point at `3.11.0`, including the `iorg` and `pits` tool projects.
- The current root docs and child live docs were refreshed to reflect the `3.11.0` line.
- PlantUML release markers were updated and the tracked SVG renders were regenerated locally.
- The `3.10.4` standalone RaiImage/ImgSeeder patch work is now folded into the coordinated `3.11.0` umbrella line.

## Behavioral payload carried forward

- RaiImage keeps the current filename-normalization flow for separated and compact trailing image numbers.
- `WordCase` remains the supported replacement for the retired `CamelCase` helper.
- `ImgSeeder`/`iorg` keeps `-rmc` alongside `--rm-cache` and remains immediately before `PitSeeder` in every release-order reference.

## Validation baseline

Commands verified successfully in this workspace state:

- `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal`
- `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal`
- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal`
- `dotnet test RAIkeep.slnx --nologo -v minimal`

Latest umbrella result:

- passed: 280
- failed: 0
- skipped: 1

## Git status baseline

Successful remote pushes from this run:

- `OsLib` -> `3268fbf`
- `RaiUtils` -> `69d2c32`

Prepared locally but not pushed because GitHub DNS resolution failed:

- `RaiImage` -> `c7e9e64`
- `JsonPit` -> `cbf0b6d`
- `ImgSeeder` -> `54a3bd2`
- `PitSeeder` -> `df2dc3a`

## Parent repo note

Update the parent repo submodule pointers and root docs together, but only push the parent after the remaining four child repos are reachable remotely. Until then, a parent push would publish broken submodule pointers.

## Suggested resume prompt

```text
Please read CURRENT-STATE.md first. The local 3.11.0 release-prep pass is complete and validated, but RaiImage, JsonPit, ImgSeeder, PitSeeder, and the parent RAIkeep push still need a working github.com DNS path.
```
