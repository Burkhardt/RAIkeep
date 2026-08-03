# RaiUtils 3.7.11 Release Notes

## Summary

- Patch release for `RaiUtils` version `3.7.11`.
- Aligns the package line with `OsLibCore 3.7.11`.
- No RaiUtils API surface changes in this patch.

## Documentation

- Updated `README.md` and `API.md` for the `3.7.11` package line.
- Refreshed `RaiUtils-ClassDiagram.puml` so the current diagram header matches the live release line.
- Regenerated `RaiUtils-ClassDiagram.svg` from the updated PlantUML source.

## Validation

- `dotnet test RaiUtils.slnx --nologo -v minimal`
- Result: 21 passed, 0 failed, 0 skipped.
