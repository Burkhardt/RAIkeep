# RaiImage Release Notes 3.x

## 3.13.1

### Summary

`RaiImage 3.13.1` aligns RaiImage with `OsLibCore 3.13.1` and `RaiUtils 3.13.1` while carrying forward the current image-tree and PlantUML feature set.

### Changes

- Updated package version, release metadata, and fallback dependency pins to the coordinated `3.13.1` line.
- Updated the `ImageTreeFile.FromName(...)` acceptance-test reference to the centralized resolved CR in the RAIkeep `doc/` directory.
- Refreshed README/API documentation and the maintained PlantUML diagrams for the current release line.
- Carries forward `ImageTreeFile.RenderPlantUml(...)`, `PlantUmlCommand`, `PlantUml`, and `PlantUmlRenderResult`.
- Carries forward `WordCase` as the supported replacement for the retired `CamelCase` helper.

### Compatibility

- No RaiImage production API or runtime behavior changed from `3.13.0`.
- Existing image-tree naming and PlantUML rendering behavior remain unchanged.

### Validation

- `RaiImage.Tests`: `94` passed, `0` failed in the coordinated validation run.
- The umbrella `RAIkeep.slnx` build succeeds with the local `3.13.1` dependencies.

### Release sequencing

`RaiImage` is third in the coordinated release chain. Its GitHub push/tag must wait for RaiUtils workflow success, flat-container visibility, and the full `330`-second hold. `JsonPit` must wait for the same checks after RaiImage publishes.

---

## 3.12.1

### Summary

- Releases `RaiImage` version `3.12.1`.
- Carries forward first-class PlantUML rendering support through `ImageTreeFile.RenderPlantUml(...)` with subscriber-tree persistence of `.puml` source and sibling `.svg` output.
- Carries forward `PlantUmlCommand`, `PlantUml`, and `PlantUmlRenderResult` for CLI integration, including direct binary and `java -jar` execution paths.
- Keeps the PlantUML rendering and jar execution regression coverage in `RaiImage.Tests`.
- Keeps `WordCase` as the supported replacement for the retired `CamelCase` helper.
- Aligns fallback package references to `OsLibCore 3.12.1` and `RaiUtils 3.12.1`.
- No public API changes from `3.12.0`.

### Validation

- Run `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal` from the RAIkeep workspace.

---

## 3.12.0

### Summary

- Releases `RaiImage` version `3.12.0`.
- Carries forward first-class PlantUML rendering support through `ImageTreeFile.RenderPlantUml(...)` with subscriber-tree persistence of `.puml` source and sibling `.svg` output.
- Carries forward `PlantUmlCommand`, `PlantUml`, and `PlantUmlRenderResult` for CLI integration, including direct binary and `java -jar` execution paths.
- Keeps the PlantUML rendering and jar execution regression coverage in `RaiImage.Tests`.
- Keeps `WordCase` as the supported replacement for the retired `CamelCase` helper.
- Aligns fallback package references to `OsLibCore 3.12.0` and `RaiUtils 3.12.0`.
- No public API changes from `3.11.5`.

### Validation

- Run `dotnet test RaiImage/RaiImage.slnx --nologo -v minimal` from the RAIkeep workspace.

---

## 3.11.4

### Summary

- Releases `RaiImage` version `3.11.4`.
- Carries forward first-class PlantUML rendering support through `ImageTreeFile.RenderPlantUml(...)` with subscriber-tree persistence of `.puml` source and sibling `.svg` output.
- Carries forward `PlantUmlCommand`, `PlantUml`, and `PlantUmlRenderResult` for CLI integration, including direct binary and `java -jar` execution paths.
- Keeps the PlantUML rendering and jar execution regression coverage in `RaiImage.Tests`.
- Keeps `WordCase` as the supported replacement for the retired `CamelCase` helper.
- Aligns fallback package references to `OsLibCore 3.11.4` and `RaiUtils 3.11.4`.
- No public API changes from `3.11.3`.

### Validation

- Run `dotnet test RaiImage/RaiImage.slnx --no-restore --nologo -v minimal` from the RAIkeep workspace.

---

## 3.11.2

### Summary

- Releases `RaiImage` version `3.11.2`.
- Adds first-class PlantUML rendering support through `ImageTreeFile.RenderPlantUml(...)` with subscriber-tree persistence of `.puml` source and sibling `.svg` output.
- Adds `PlantUmlCommand`, `PlantUml`, and `PlantUmlRenderResult` for CLI integration, including direct binary and `java -jar` execution paths.
- Adds regression coverage for PlantUML rendering and jar execution flows in `RaiImage.Tests`.
- Keeps `WordCase` as the supported replacement for the retired `CamelCase` helper.
- Aligns fallback package references to `OsLibCore 3.11.2` and `RaiUtils 3.11.2`.

### Validation

- Run `dotnet test RaiImage/RaiImage.slnx --no-restore --nologo -v minimal` from the RAIkeep workspace.

---

## 3.11.1

### Summary

- Releases `RaiImage` version `3.11.1`.
- Carries forward `WordCase` as the supported replacement for the retired `CamelCase` helper.
- Preserves the current filename-normalization flow used by `ImgSeeder`/`iorg`.
- Aligns fallback package references to `OsLibCore 3.11.1` and `RaiUtils 3.11.1`.

### Validation

- Run `dotnet test RaiImage/RaiImage.slnx --no-restore --nologo -v minimal` from the RAIkeep workspace.

---

## 3.11.0

### Summary

- Releases `RaiImage` version `3.11.0`.
- Carries forward `WordCase` as the supported replacement for the retired `CamelCase` helper.
- Preserves the current filename-normalization flow used by `ImgSeeder`/`iorg`.
- Aligns fallback package references to `OsLibCore 3.11.0` and `RaiUtils 3.11.0`.

### Validation

- Run `dotnet test RaiImage/RaiImage.slnx --no-restore --nologo -v minimal` from the RAIkeep workspace.

---

## 3.10.4

### Summary

- Releases `RaiImage` version `3.10.4`.
- Documents `WordCase` as the supported replacement for the retired `CamelCase` helper.
- Refreshes the live hierarchy diagram source so current API docs no longer advertise the removed `CamelCase` type.
- Keeps fallback package references on `OsLibCore 3.10.2` and `RaiUtils 3.10.2`.

### Validation

- Run `dotnet test RaiImage/RaiImage.slnx --no-restore --nologo -v minimal` from the RAIkeep workspace.

---

## 3.10.2

### Summary

- Releases `RaiImage` version `3.10.2`.
- Carries forward current filename-normalization behavior and acronym-preserving word-case behavior from `3.10.1`.
- Aligns fallback package references to `OsLibCore 3.10.2` and `RaiUtils 3.10.2`.
- Refreshes current markdown and PlantUML release markers for the coordinated package line.

### Validation

- `dotnet test RaiImage.Tests/RaiImage.Tests.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.1

### Summary

- Releases `RaiImage` version `3.10.1`.
- Carries forward separated and compact trailing digits as `ImageNumber` during `ImageFile.EasyFileName(...)` normalization.
- Carries forward all-uppercase token preservation in `WordCase` PascalCase output for acronym-heavy item ids.
- Aligns fallback package references to `OsLibCore 3.10.1` and `RaiUtils 3.10.1`.
- Refreshes current markdown and PlantUML release markers for the coordinated package line.
- No public API changes from `3.10.0`.

### Validation

- `dotnet test RaiImage.Tests/RaiImage.Tests.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.0

### Summary

- Releases `RaiImage` version `3.10.0`.
- Carries forward separated and compact trailing digits as `ImageNumber` during `ImageFile.EasyFileName(...)` normalization.
- Carries forward all-uppercase token preservation in `WordCase` PascalCase output for acronym-heavy item ids.
- Aligns fallback package references to `OsLibCore 3.10.0` and `RaiUtils 3.10.0`.
- Refreshes markdown and PlantUML release markers for the coordinated minor line.
- No public API changes from `3.9.1`.

### Validation

- `dotnet test RaiImage.Tests/RaiImage.Tests.csproj --nologo -v minimal`
- NuGet publishing remains wired through the tag-triggered `publish-nuget.yml` workflow.

---

## 3.9.1

### Summary

- Releases `RaiImage` version `3.9.1`.
- Preserves separated and compact trailing digits as `ImageNumber` during `ImageFile.EasyFileName(...)` normalization.
- Preserves all-uppercase tokens in `WordCase` PascalCase output so acronym-heavy item ids normalize predictably.
- Aligns fallback package references to `OsLibCore 3.9.1` and `RaiUtils 3.9.1`.
- Refreshes markdown and PlantUML release markers for the coordinated patch line.

### Validation

- `dotnet test RaiImage.Tests/RaiImage.Tests.csproj --nologo -v minimal`
- NuGet publishing is handled by tag-triggered `publish-nuget.yml`.

---

## 3.9.0

### Summary

- Releases `RaiImage` version `3.9.0`.
- Adds naming-aware `ImageTreeFile.FromName(...)` factories for rooted short-name parsing without a dummy extension.
- Makes `ImageTreeFile.InferSourceNamingConvention(...)` public so caller-side parsing can stay aligned with RaiImage's own inference.
- Applies the naming-aware component constructor when creating tree-based render targets and aligns fallback package references to `OsLibCore 3.9.0` and `RaiUtils 3.9.0`.
- Refreshes markdown and PlantUML release markers for the coordinated minor line.

### Validation

- `dotnet test RaiImage.Tests/RaiImage.Tests.csproj --nologo -v minimal`
- NuGet publishing is handled by tag-triggered `publish-nuget.yml`.

---

## 3.8.15

### Summary

- Releases `RaiImage` version `3.8.15`.
- Fixes numbered render-target filenames so `AfricanPicnic_01` and `AfricanPicnic_02` render to distinct outputs such as `AfricanPicnic_01_Huge.webp` and `AfricanPicnic_02_Huge.webp`.
- Adds render regression coverage for numbered and unnumbered image items.
- Aligns fallback package references to `OsLibCore 3.8.15` and `RaiUtils 3.8.15`.
- Refreshes markdown and PlantUML release markers for the coordinated chain.

### Validation

- `dotnet test RaiImage.Tests/RaiImage.Tests.csproj --nologo -v minimal`
- NuGet publishing is handled by tag-triggered `publish-nuget.yml`.

---

## 3.8.14

### Summary

- Releases `RaiImage` version `3.8.14`.
- Aligns fallback package references to `OsLibCore 3.8.14` and `RaiUtils 3.8.14`.
- Refreshes markdown and PlantUML release markers for the coordinated chain.
- Keeps the image-number-aware source resolution behavior from the prior patch line.

### Validation

- `dotnet test RaiImage.Tests/RaiImage.Tests.csproj --nologo -v minimal`
- NuGet publishing is handled by tag-triggered `publish-nuget.yml`.

---

## 3.8.12

### Summary

- Releases `RaiImage` version `3.8.12`.
- Aligns fallback package references to `OsLibCore 3.8.12` and `RaiUtils 3.8.12`.
- Refreshes live README links and PlantUML release markers for the coordinated `RAIkeep` patch line.
- No RaiImage API changes from `3.8.11`.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`: 243 passed, 0 failed, 1 skipped.
- NuGet publishing and tag-triggered release workflows were intentionally not run.

---

## 3.8.11

### Summary

- Releases `RaiImage` version `3.8.11`.
- Tightens `ExtendToFirstExistingFile(...)` so source discovery respects item id, image number, color, naming-convention parsing, and case-insensitive extension matching.
- Adds regression coverage for image-tree source resolution and refreshes live markdown and PlantUML release markers for the `3.8.11` line.

### Validation

- Release published through GitHub Actions tag workflow.
- NuGet visibility is verified in the sequential release chain.

---

## 3.8.6

### Summary

- Coordinated release for `RaiImage` version `3.8.6`.
- Refreshes markdown release-line references (including `README.md`) via automated scan.
- Refreshes all tracked PlantUML (`.puml`) release/version markers found in scope.

### Validation

- Release published through GitHub Actions tag workflow.
- NuGet visibility is verified in the sequential release chain.

---

## 3.8.1

### Summary

- Changes `ImageTreeFile.mkdir()` from member hiding to a true override of `RaiFile.mkdir()`.
- Ensures base-class operations such as `WriteFromAsync(...)` dispatch to image-tree directory creation logic.
- Aligns fallback package references with `OsLibCore 3.8.1` and `RaiUtils 3.8.1`.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- Result: 223 passed, 0 failed, 0 skipped.

---

## 3.8.0

### Summary

- Coordinated release for `RaiImage` version `3.8.0`.
- Aligns fallback package references with `OsLibCore 3.8.0` and `RaiUtils 3.8.0`.
- Keeps the packaged README in the NuGet payload.
- No public RaiImage API surface changes in this release.

### Documentation

- Updated `README.md`, `API.md`, `TESTING.md`, and `ARCHITECTURE-ALIGNMENT.md` for the `3.8.0` package line.
- Refreshed the active RaiImage PlantUML headers so the current diagrams are labeled consistently with the live release.

### Validation

- `dotnet pack RaiImage.csproj --nologo -v minimal`
- Result: package builds successfully and the `.nupkg` contains `README.md` and `HardCastle.png`.

---

## 3.7.11

### Summary

- Patch release for `RaiImage` version `3.7.11`.
- Aligns fallback package references with `OsLibCore 3.7.11` and `RaiUtils 3.7.11`.
- No public RaiImage API surface changes in this patch.

### Documentation

- Updated `README.md`, `API.md`, `TESTING.md`, and `ARCHITECTURE-ALIGNMENT.md` for the `3.7.11` package line.
- Refreshed the active RaiImage PlantUML headers so the current diagrams are labeled consistently with the live release.
- Regenerated the rendered SVG diagram artifacts from the updated PlantUML sources.

### Validation

- `dotnet test RaiImage.slnx --nologo -v minimal`
- Result: 54 passed, 0 failed, 0 skipped.

---

## 3.7.9

### Summary

- Patch release for `RaiImage` version `3.7.9`.
- Aligns fallback package references with `OsLibCore 3.7.9` and `RaiUtils 3.7.9`.
- No public RaiImage API surface changes in this patch.

### Documentation

- Updated `README.md`, `API.md`, `TESTING.md`, and `ARCHITECTURE-ALIGNMENT.md` for the `3.7.9` package line.
- Refreshed the active RaiImage PlantUML headers so the current diagrams are labeled consistently with the live release.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- Result: 220 passed, 0 failed, 0 skipped.

---

## 3.7.7

### Summary

- Patch release for `RaiImage` version `3.7.7`.
- Aligns fallback package references with `OsLibCore 3.7.7` and `RaiUtils 3.7.7`.
- No public RaiImage API surface changes in this patch.

### Documentation

- Updated `README.md`, `API.md`, `TESTING.md`, and `ARCHITECTURE-ALIGNMENT.md` for the `3.7.7` package line.
- Refreshed the active RaiImage PlantUML headers so the current diagrams are labeled consistently with the live release.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- Result: 214 passed, 0 failed, 0 skipped.

---

## 3.7.6

### Summary

- Patch release for `RaiImage` version `3.7.6`.
- Aligns fallback package references with `OsLibCore 3.7.6` and `RaiUtils 3.7.6`.
- No public RaiImage API surface changes in this patch.

### Documentation

- README, API, testing, and architecture notes now reflect the current `RAIkeep 3.7.6` package line.

---

## 3.7.2

### Highlights

- Aligns RaiImage package version with the 3.7.2 release line.
- Updates fallback package references to `OsLibCore 3.7.2` and `RaiUtils 3.7.2`.
- No RaiImage API surface changes in this patch release.

---

## 3.7.1

### Summary

- Patch release aligned with `OsLibCore 3.7.1` and `RaiUtils 3.7.1`.
- Keeps public API and runtime behavior stable.
- Updates release-line documentation and package metadata.

### Package

- NuGet package version: `3.7.1`
- Package id: `RaiImage`

---

## 3.6.1

### Highlights

- Patch release following `3.6.0`.
- Aligns RaiImage with `OsLibCore 3.6.1` and `RaiUtils 3.6.1` in the correct NuGet publish order.
- Fallback `PackageReference` versions updated to `3.6.1`.
- No API or behavioral changes.

### Validation

- RaiImage should be validated with the local `RaiImage` test suite and package build before publishing.

---

## 3.6.0

### Highlights

- Version bumped to `3.6.0`.
- Aligns RaiImage with the shared `3.6.0` package line across `RAIkeep`.
- Fallback package references now align with `OsLibCore 3.6.0` and `RaiUtils 3.6.0`.

### Compatibility

- No API or behavioral changes in this release.

### Validation

- RaiImage should be validated with the local `RaiImage` test suite and package build before publishing.

---

## 3.5.2

### Highlights

- Version bumped to `3.5.2`.
- RaiImage documentation now aligns with the shared `3.5.2` package line used across `RAIkeep`.
- Fallback package references now align with `OsLibCore 3.5.2` and `RaiUtils 3.5.2`.
- The fallback utility package id is now `RaiUtils` rather than `RaiUtilsCore`.

### Cross-Package Alignment

- RaiImage remains compatible with the shared OsLib configuration model based on `osconfig.json`.
- Documentation continues to align with JsonPit's `Id`-based identifier contract across the package stack.
- RaiImage continues to consume the current OsLib `RaiPath`-based directory APIs without intentional behavioral changes in this patch.

### Validation

- RaiImage should be validated with the local `RaiImage` test suite and package build before publishing.

---

## 3.5.0

### Highlights

- Version bumped to `3.5.0`.
- RaiImage documentation now aligns with the shared `3.5.0` package line used across `RAIkeep`.
- The documented cloud-backed support claim now focuses on `OneDrive`, `GoogleDrive`, and `Dropbox`.
- RaiImage package metadata and fallback package references were aligned with the shared `3.5.0` package line.

### Cross-Package Alignment

- RaiImage remains compatible with the shared OsLib configuration model based on `osconfig.json`.
- Documentation now explicitly aligns with JsonPit's `Id`-based identifier contract across the package stack.
- RaiImage continues to consume the updated OsLib `RaiPath`-based directory APIs without behavioral regressions in the workspace test run.

### Validation

- RaiImage remained green in the full workspace validation run for `3.5.0`.

---

## 3.3.0

### Highlights

- Version bumped to `3.3.0`.
- `ImageMagick` was extracted from `ImageFile.cs` into its own source file.
- RaiImage no longer depends on `Os.winInternal` for the Windows retry path.
- Fallback package references now align with `OsLibCore 3.3.0` and `RaiUtilsCore 3.3.0`.

### Compatibility

- Public package version is now aligned with the rest of the current RAIkeep library set.
- Existing `magick`-based command invocation behavior remains in place.
- RaiImage stays compatible with OsLib's new `Os.Config` and `osconfig.json` cloud-root model.

### Validation

- Solution validation remained green after the refactor and version alignment.

---

## 3.2.0

### Highlights

- Version bumped to `3.2.0`.
- ImageMagick wrapper moved to modern CLI invocation style (`magick` + subcommands).
- Vulnerability warnings addressed in package dependencies.
- Project-reference-first development flow enabled for local sibling repos.
- Initial `RaiImage.Tests` xUnit suite added.

### Dependency and security updates

- `System.Drawing.Common` upgraded to `10.0.4`.
- Direct `Newtonsoft.Json` reference set to `13.0.4`.
- Removed redundant `System.Security.AccessControl` package reference that caused `NU1510`.

### Build and analyzer improvements

- Added platform guards for Windows-only API paths to resolve `CA1416` warnings.
- Removed hardcoded Windows executable paths from ImageMagick defaults.

### Compatibility

This release includes intentional breaking changes in command invocation assumptions.
See `MIGRATION_3.2.0.md` for upgrade guidance.
