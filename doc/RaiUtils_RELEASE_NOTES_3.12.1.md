# RaiUtils 3.12.1 Release Notes

## Summary

- Releases `RaiUtils` version `3.12.1`.
- Aligns the coordinated package baseline with `OsLibCore 3.12.1`.
- Carries forward the current docs and class-diagram release markers without public API changes from `3.12.0`.

## Validation

- `dotnet test RaiUtils.slnx --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.
