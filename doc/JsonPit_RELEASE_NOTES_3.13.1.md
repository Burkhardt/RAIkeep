# JsonPit 3.13.1 Release Notes

## Summary

- Releases `JsonPit` version `3.13.1`.
- Aligns fallback package references to `OsLibCore 3.13.1` and `RaiUtils 3.13.1`.
- Carries forward the current concurrency coverage, packaged docs, and class-diagram release markers for the coordinated package line.
- Adds per-process activity flags and ownership-verified process-window release while keeping master writer tickets separate.
- Writes flag updates in place through OsLib, avoiding the OneDrive-sensitive delete/recreate cycle used by the previous flag save path.
- Carries forward `PitItem.DeleteProperty(...)` projection semantics: top-level null fragments act as attribute tombstones, so projected reads omit the deleted property instead of exposing a permanent null shadow.
- Adds the public `TryReleaseProcessWindow()` and process-flag ownership helpers used by finite clients such as PitSeeder.

## Validation

- `dotnet test JsonPit.Tests/JsonPit.Tests.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.
