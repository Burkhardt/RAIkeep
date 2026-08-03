# RaiImage 3.13.1 Release Notes

## Summary

`RaiImage 3.13.1` aligns RaiImage with `OsLibCore 3.13.1` and `RaiUtils 3.13.1` while carrying forward the current image-tree and PlantUML feature set.

## Changes

- Updated package version, release metadata, and fallback dependency pins to the coordinated `3.13.1` line.
- Updated the `ImageTreeFile.FromName(...)` acceptance-test reference to the centralized resolved CR in the RAIkeep `doc/` directory.
- Refreshed README/API documentation and the maintained PlantUML diagrams for the current release line.
- Carries forward `ImageTreeFile.RenderPlantUml(...)`, `PlantUmlCommand`, `PlantUml`, and `PlantUmlRenderResult`.
- Carries forward `WordCase` as the supported replacement for the retired `CamelCase` helper.

## Compatibility

- No RaiImage production API or runtime behavior changed from `3.13.0`.
- Existing image-tree naming and PlantUML rendering behavior remain unchanged.

## Validation

- `RaiImage.Tests`: `94` passed, `0` failed in the coordinated validation run.
- The umbrella `RAIkeep.slnx` build succeeds with the local `3.13.1` dependencies.

## Release sequencing

`RaiImage` is third in the coordinated release chain. Its GitHub push/tag must wait for RaiUtils workflow success, flat-container visibility, and the full `330`-second hold. `JsonPit` must wait for the same checks after RaiImage publishes.
