# CURRENT_STATUS

Last updated: 2026-07-11

Current coordinated package line: `3.11.4`

## Release Truth

- The release baseline was the latest remote tag common to all six child repositories: `v3.11.3`.
- The completed release line is `v3.11.4`.
- Local unreleased `3.13.0` preparation was corrected back to `3.11.4` before publishing.

## Completed Package Order

Each package completed commit, tag, push, publish workflow success, NuGet flat-container visibility, and a 330-second indexing hold before the next package began:

1. `OsLib` / `OsLibCore` -> `v3.11.4`
2. `RaiUtils` -> `v3.11.4`
3. `RaiImage` -> `v3.11.4`
4. `JsonPit` -> `v3.11.4`
5. `ImgSeeder` / `iorg` -> `v3.11.4`
6. `PitSeeder` / `pits` -> `v3.11.4`

## Child Commits

- `OsLib` `4114720` (`v3.11.4`)
- `RaiUtils` `c1e13a9` (`v3.11.4`)
- `RaiImage` `f28f8b9` (`v3.11.4`)
- `JsonPit` `d49f2bf` (`v3.11.4`)
- `ImgSeeder` `2b9dc32` (`v3.11.4`)
- `PitSeeder` `8ae6767` (`v3.11.4`)

## NuGet Visibility

Final flat-container checks returned `200` for all six packages:

- `oslibcore/3.11.4/oslibcore.3.11.4.nupkg`
- `raiutils/3.11.4/raiutils.3.11.4.nupkg`
- `raiimage/3.11.4/raiimage.3.11.4.nupkg`
- `jsonpit/3.11.4/jsonpit.3.11.4.nupkg`
- `imgseeder/3.11.4/imgseeder.3.11.4.nupkg`
- `pitseeder/3.11.4/pitseeder.3.11.4.nupkg`

## Validation

- `dotnet test RaiUtils/RaiUtils.slnx --nologo -v minimal` -> `21 passed`
- `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal` -> `94 passed`
- `dotnet test JsonPit/JsonPit.Tests/JsonPit.Tests.csproj --filter FullyQualifiedName~DeletePropertyProjectionTests --nologo -v minimal` -> `7 passed`
- `dotnet test JsonPit/JsonPit.Tests/JsonPit.Tests.csproj --nologo -v minimal` -> `101 passed`, `1 skipped`
- `dotnet test ImgSeeder/ImgSeeder.slnx --nologo -v minimal` -> `8 passed`
- `dotnet test PitSeeder/PitSeeder.slnx --nologo -v minimal` -> `4 passed`

Existing non-blocking warning observed on JsonPit-dependent builds:

- `JsonPit.cs(95,32): warning CS1574: XML comment has cref attribute 'AddPreservingModified' that could not be resolved`

## Release Script

- `scripts/release-chain.sh` now derives the next patch version from remote tags when no version argument is supplied.
- The script order is `OsLib -> RaiUtils -> RaiImage -> JsonPit -> ImgSeeder -> PitSeeder`.
- The script enforces workflow success, NuGet flat-container visibility, and the 330-second hold per package before proceeding.
