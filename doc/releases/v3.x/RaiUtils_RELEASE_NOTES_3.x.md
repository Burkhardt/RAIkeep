# RaiUtils Release Notes 3.x

## 3.13.1

### Summary

`RaiUtils 3.13.1` is the coordinated dependency-alignment release for `OsLibCore 3.13.1`.

### Changes

- Updated package version and release metadata to `3.13.1`.
- Aligned the OsLibCore package baseline with `3.13.1`.
- Refreshed README, API documentation, centralized release-note links, and the class-diagram release marker.

### Compatibility

- No RaiUtils production API or behavior changed from `3.13.0`.
- Configuration behavior remains unchanged.

### Validation

- `RaiUtils.Tests`: `21` passed, `0` failed in the coordinated validation run.
- The umbrella `RAIkeep.slnx` build succeeds with the local `3.13.1` sources.

### Release sequencing

`RaiUtils` is second in the coordinated release chain. Its GitHub push/tag must wait for OsLibCore workflow success, flat-container visibility, and the full `330`-second hold. `RaiImage` must wait for the same checks after RaiUtils publishes.

---

## 3.12.1

### Summary

- Releases `RaiUtils` version `3.12.1`.
- Aligns the coordinated package baseline with `OsLibCore 3.12.1`.
- Carries forward the current docs and class-diagram release markers without public API changes from `3.12.0`.

### Validation

- `dotnet test RaiUtils.slnx --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.12.0

### Summary

- Releases `RaiUtils` version `3.12.0`.
- Aligns the coordinated package baseline with `OsLibCore 3.12.0`.
- Carries forward the current docs and class-diagram release markers without public API changes from `3.11.5`.

### Validation

- `dotnet test RaiUtils.slnx --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.4

### Summary

- Releases `RaiUtils` version `3.11.4`.
- Aligns the coordinated package baseline with `OsLibCore 3.11.4`.
- Carries forward the current docs and class-diagram release markers without public API changes from `3.11.3`.

### Validation

- `dotnet build RaiUtils.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.2

### Summary

- Releases `RaiUtils` version `3.11.2`.
- Aligns the coordinated package baseline with `OsLibCore 3.11.2`.
- Carries forward the current docs and class-diagram release markers without public API changes from `3.11.1`.

### Validation

- `dotnet build RaiUtils.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.1

### Summary

- Releases `RaiUtils` version `3.11.1`.
- Aligns the coordinated package baseline with `OsLibCore 3.11.1`.
- Carries forward the current docs and class-diagram release markers without public API changes from `3.11.0`.

### Validation

- `dotnet build RaiUtils.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.0

### Summary

- Releases `RaiUtils` version `3.11.0`.
- Aligns the coordinated package baseline with `OsLibCore 3.11.0`.
- Carries forward the current docs and class-diagram release markers without public API changes from `3.10.2`.

### Validation

- `dotnet build RaiUtils.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.2

### Summary

- Releases `RaiUtils` version `3.10.2`.
- Carries forward the coordinated package baseline with refreshed current docs and class-diagram release markers.
- No public API changes from `3.10.1`.

### Validation

- `dotnet build RaiUtils.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.1

### Summary

- Releases `RaiUtils` version `3.10.1`.
- Carries forward the coordinated `3.10.0` package baseline with refreshed current docs and class diagram release markers.
- No public API changes from `3.10.0`.

### Validation

- `dotnet build RaiUtils.csproj --nologo -v minimal`
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.0

### Summary

- Releases `RaiUtils` version `3.10.0`.
- Aligns package metadata, docs, and class diagram release markers with the coordinated `RAIkeep` minor line.
- No public API changes from `3.9.1`.

### Validation

- `dotnet build RaiUtils.csproj --nologo -v minimal`
- NuGet publishing remains wired through the tag-triggered `publish-nuget.yml` workflow.

---

## 3.9.1

### Summary

- Releases `RaiUtils` version `3.9.1`.
- Aligns package metadata, docs, and class diagram release markers with the coordinated `RAIkeep` patch line.
- No public API changes from `3.9.0`.

### Validation

- `dotnet build RaiUtils.csproj --nologo -v minimal`
- NuGet publishing is handled by the tag-triggered `publish-nuget.yml` workflow.

---

## 3.9.0

### Summary

- Releases `RaiUtils` version `3.9.0`.
- Aligns package metadata, docs, and class diagram release markers with the coordinated `RAIkeep` release line.
- No public API changes from `3.8.15`.

### Validation

- `dotnet build RaiUtils.csproj --nologo -v minimal`
- NuGet publishing is handled by the tag-triggered `publish-nuget.yml` workflow.

---

## 3.8.15

### Summary

- Releases `RaiUtils` version `3.8.15`.
- Aligns package metadata, docs, and class diagram release markers with the coordinated `RAIkeep` release line.
- No public API changes from `3.8.14`.

### Validation

- `dotnet build RaiUtils.csproj --nologo -v minimal`
- NuGet publishing is handled by the tag-triggered `publish-nuget.yml` workflow.

---

## 3.8.14

### Summary

- Releases `RaiUtils` version `3.8.14`.
- Aligns package metadata, docs, and class diagram release markers with the coordinated `RAIkeep` release line.
- No public API changes from `3.8.12`.

### Validation

- `dotnet build RaiUtils.csproj --nologo -v minimal`
- NuGet publishing is handled by the tag-triggered `publish-nuget.yml` workflow.

---

## 3.8.12

### Summary

- Releases `RaiUtils` version `3.8.12`.
- Aligns package metadata, live README links, and PlantUML release markers with the coordinated `RAIkeep` patch line.
- No RaiUtils API changes from `3.8.11`.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`: 243 passed, 0 failed, 1 skipped.
- NuGet publishing and tag-triggered release workflows were intentionally not run.

---

## 3.8.11

### Summary

- Releases `RaiUtils` version `3.8.11`.
- Aligns the package metadata and live docs with the coordinated `3.8.11` package line.
- Refreshes tracked PlantUML release markers for the current release line.

### Validation

- Release published through GitHub Actions tag workflow.
- NuGet visibility is verified in the sequential release chain.

---

## 3.8.6

### Summary

- Coordinated release for `RaiUtils` version `3.8.6`.
- Refreshes markdown release-line references (including `README.md`) via automated scan.
- Refreshes all tracked PlantUML (`.puml`) release/version markers found in scope.

### Validation

- Release published through GitHub Actions tag workflow.
- NuGet visibility is verified in the sequential release chain.

---

## 3.8.1

### Summary

- Coordinated release for `RaiUtils` version `3.8.1`.
- Aligns the package line with `OsLibCore 3.8.1`.
- No RaiUtils API surface changes in this release.

### Documentation

- Updated `README.md` and `API.md` for the `3.8.1` package line.
- Refreshed `RaiUtils-ClassDiagram.puml` so the current diagram header matches the live release line.

### Validation

- `dotnet test RaiUtils.slnx --nologo -v minimal`
- Result: 21 passed, 0 failed, 0 skipped.

---

## 3.8.0

### Summary

- Coordinated release for `RaiUtils` version `3.8.0`.
- Aligns the package line with `OsLibCore 3.8.0`.
- No RaiUtils API surface changes in this release.

### Documentation

- Updated `README.md` and `API.md` for the `3.8.0` package line.
- Refreshed `RaiUtils-ClassDiagram.puml` so the current diagram header matches the live release line.

### Validation

- `dotnet test RaiUtils.slnx --nologo -v minimal`
- Result: 21 passed, 0 failed, 0 skipped.

---

## 3.7.11

### Summary

- Patch release for `RaiUtils` version `3.7.11`.
- Aligns the package line with `OsLibCore 3.7.11`.
- No RaiUtils API surface changes in this patch.

### Documentation

- Updated `README.md` and `API.md` for the `3.7.11` package line.
- Refreshed `RaiUtils-ClassDiagram.puml` so the current diagram header matches the live release line.
- Regenerated `RaiUtils-ClassDiagram.svg` from the updated PlantUML source.

### Validation

- `dotnet test RaiUtils.slnx --nologo -v minimal`
- Result: 21 passed, 0 failed, 0 skipped.

---

## 3.7.9

### Summary

- Patch release for `RaiUtils` version `3.7.9`.
- Aligns the package line with `OsLibCore 3.7.9`.
- No RaiUtils API surface changes in this patch.

### Documentation

- Updated `README.md` and `API.md` for the `3.7.9` package line.
- Refreshed `RaiUtils-ClassDiagram.puml` so the current diagram header matches the live release line.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- Result: 220 passed, 0 failed, 0 skipped.

---

## 3.7.7

### Summary

- Patch release for `RaiUtils` version `3.7.7`.
- Aligns the package line with `OsLibCore 3.7.7`.
- No RaiUtils API surface changes in this patch.

### Documentation

- Updated `README.md` and `API.md` for the `3.7.7` package line.
- Refreshed `RaiUtils-ClassDiagram.puml` so the current diagram header matches the live release line.

### Validation

- `dotnet test RAIkeep.slnx --nologo -v minimal`
- Result: 214 passed, 0 failed, 0 skipped.

---

## 3.7.6

### Summary

- Patch release for `RaiUtils` version `3.7.6`.
- Aligns the package line with `OsLibCore 3.7.6`.
- No RaiUtils API surface changes in this patch.

### Documentation

- Current package docs now align the shared config contract on `RAIkeep.json5`.
- README and API notes now reflect the current `RAIkeep 3.7.6` package line.

---

## 3.7.2

### Highlights

- Aligns RaiUtils package version with OsLibCore 3.7.2 in the publish sequence.
- No RaiUtils API surface changes in this patch release.
- Updates release metadata and README references to the 3.7.2 line.

---

## 3.7.1

### Summary

- Patch release aligned with `OsLibCore 3.7.1`.
- Keeps API and behavior stable.
- Updates release-line documentation and package metadata.

### Package

- NuGet package version: `3.7.1`
- Package id: `RaiUtils`

---

## 3.6.1

### Highlights

- Patch release following `3.6.0`.
- Aligns RaiUtils with `OsLibCore 3.6.1` in the correct NuGet publish order.
- No API changes.

### Validation

- The package remains a lightweight utility layer in the `RAIkeep` stack.

---

## 3.6.0

### Highlights

- Version bumped to `3.6.0`.
- Continues publishing as the consolidated NuGet package `RaiUtils`.
- Aligns the utility package with `OsLibCore 3.6.0` and the shared `3.6.0` `RAIkeep` package line.

### Compatibility

- No API changes in this release.

### Validation

- The package remains a lightweight utility layer in the `RAIkeep` stack.

---

## 3.5.2

### Highlights

- Version bumped to `3.5.2`.
- Continues publishing the consolidated NuGet package id `RaiUtils`.
- Aligns the utility package with `OsLibCore 3.5.2` before downstream `RaiImage` and `JsonPit` fallback package updates.

### Packaging

- `RaiUtils.csproj` continues to pack as `RaiUtils`.
- The runtime API and `RaiUtils` namespace stay unchanged.
- This release supersedes the `3.5.1` package-id consolidation release for the shared aligned package line.

### Validation

- The package remains a lightweight utility layer in the `RAIkeep` stack.

---

## 3.5.1

### Highlights

- Version bumped to `3.5.1`.
- The NuGet package id is now `RaiUtils`.
- The previous split between `RaiUtils` and `RaiUtilsCore` on NuGet is consolidated onto the `RaiUtils` package id for current releases.

### Packaging

- `RaiUtils.csproj` now packs as `RaiUtils` instead of `RaiUtilsCore`.
- The runtime API and `RaiUtils` namespace stay unchanged.
- This change is intended to simplify downstream package references in `RaiImage` and `JsonPit`.

### Validation

- The package remains a lightweight utility layer in the `RAIkeep` stack.

---

## 3.5.0

### Highlights

- Version bumped to `3.5.0`.
- RaiUtils documentation now aligns with the shared `3.5.0` package line used in `RAIkeep`.
- The documented package-stack support claim now names `OneDrive`, `GoogleDrive`, and `Dropbox`.
- RaiUtils package metadata was aligned with the `3.5.0` workspace release.

### Cross-Package Alignment

- RaiUtils continues to avoid a direct runtime dependency on OsLib types.
- The docs now explicitly align with JsonPit's `Id`-based identifier contract and legacy `Name` normalization behavior.

### Validation

- The package remains a lightweight utility layer in the `RAIkeep` stack and keeps its existing runtime behavior.
- RaiUtils remained green in the full workspace validation run for `3.5.0`.

---

## 3.3.0

### Highlights

- Version bumped to `3.3.0`.
- RaiUtils documentation now aligns with the shared `osconfig.json` convention used alongside OsLib and JsonPit.
- Package metadata stays aligned with the current RAIkeep library set.

### Compatibility

- RaiUtils still has no direct runtime dependency on OsLib types.
- The documented cross-package configuration contract now points at `osconfig.json` and the nested `cloud` keys.

### Validation

- Full solution validation remained green after the version bump.
