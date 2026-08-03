# RaiUtils 3.10.1 Release Notes

## Summary

- Releases `RaiUtils` version `3.10.1`.
- Carries forward the coordinated `3.10.0` package baseline with refreshed current docs and class diagram release markers.
- No public API changes from `3.10.0`.

## Validation

- `dotnet build RaiUtils.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.
