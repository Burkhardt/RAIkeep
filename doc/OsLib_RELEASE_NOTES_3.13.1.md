# OsLibCore 3.13.1 Release Notes

## Summary

- Releases `OsLibCore` version `3.13.1`.
- Carries forward the coordinated `RAIkeep` package line with refreshed package metadata, README links, and diagram release markers.
- Adds `TextFile.SaveInPlace()` for small coordination files that must update a cloud-synced path without a preceding delete or rename.
- Retains the normal cloud materialization check after an in-place write.

## Validation

- `dotnet build OsLib.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.
