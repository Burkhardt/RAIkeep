# ImgSeeder Release Notes 3.x

## 3.13.1

### Summary

`ImgSeeder 3.13.1` is the coordinated `iorg` CLI release aligned with the four `3.13.1` RAIkeep libraries.

### Changes

- Updated assembly, file, informational, and package versions to `3.13.1`.
- Updated fallback package defaults to `JsonPit 3.13.1`, `OsLibCore 3.13.1`, `RaiUtils 3.13.1`, and `RaiImage 3.13.1`.
- Updated test-project package defaults to the same release line.
- Carries forward `-rmc` as the short alias for cache deletion while retaining `--rm-cache`.
- Refreshed the README and centralized release-note link.

### Compatibility

- No `iorg` CLI behavior changed from `3.13.0`.
- Existing command names and options remain unchanged.

### Validation

- `ImgSeeder.Tests`: `8` passed, `0` failed in the coordinated validation run.
- The umbrella `RAIkeep.slnx` build succeeds with the local `3.13.1` dependency chain.

### Release sequencing

`ImgSeeder` is fifth in the coordinated release chain. Its GitHub push/tag must wait for JsonPit workflow success, flat-container visibility, and the full `330`-second hold. `PitSeeder` must wait for the same checks after ImgSeeder publishes.

---

## 3.12.1

### Summary

- Releases `ImgSeeder` version `3.12.1` with the `iorg` command.
- Carries forward `-rmc` as the short option alias for cache-delete mode while keeping `--rm-cache`.
- Keeps the aligned help output formatting and updates fallback package defaults to `JsonPit 3.12.1`, `OsLibCore 3.12.1`, `RaiUtils 3.12.1`, and `RaiImage 3.12.1`.
- Preserves the coordinated release order immediately before `PitSeeder`.
- No CLI behavior changes from `3.12.0`.

### Validation

- `dotnet test ImgSeeder.slnx --nologo -v minimal`
- Publication remains wired through the tag-triggered `publish-nuget.yml` workflow.

---

## 3.12.0

### Summary

- Releases `ImgSeeder` version `3.12.0` with the `iorg` command.
- Carries forward `-rmc` as the short option alias for cache-delete mode while keeping `--rm-cache`.
- Keeps the aligned help output formatting and updates fallback package defaults to `JsonPit 3.12.0`, `OsLibCore 3.12.0`, `RaiUtils 3.12.0`, and `RaiImage 3.12.0`.
- Preserves the coordinated release order immediately before `PitSeeder`.
- No CLI behavior changes from `3.11.5`.

### Validation

- `dotnet test ImgSeeder.slnx --nologo -v minimal`
- Publication remains wired through the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.4

### Summary

- Releases `ImgSeeder` version `3.11.4` with the `iorg` command.
- Carries forward `-rmc` as the short option alias for cache-delete mode while keeping `--rm-cache`.
- Keeps the aligned help output formatting and updates fallback package defaults to `JsonPit 3.11.4`, `OsLibCore 3.11.4`, `RaiUtils 3.11.4`, and `RaiImage 3.11.4`.
- Preserves the coordinated release order immediately before `PitSeeder`.
- No CLI behavior changes from `3.11.3`.

### Validation

- `dotnet test ImgSeeder.slnx --nologo -v minimal`
- `dotnet run --project ImgSeeder.csproj -- -h -c OneDrive -r LiveAfricaStageImage`
- Publication remains wired through the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.2

### Summary

- Releases `ImgSeeder` version `3.11.2` with the `iorg` command.
- Carries forward `-rmc` as the short option alias for cache-delete mode while keeping `--rm-cache`.
- Keeps the aligned help output formatting and updates fallback package defaults to `JsonPit 3.11.2`, `OsLibCore 3.11.2`, `RaiUtils 3.11.2`, and `RaiImage 3.11.2`.
- Preserves the coordinated release order immediately before `PitSeeder`.

### Validation

- `dotnet test ImgSeeder.slnx --nologo -v minimal`
- `dotnet run --project ImgSeeder.csproj -- -h -c OneDrive -r LiveAfricaStageImage`
- Publication remains wired through the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.1

### Summary

- Releases `ImgSeeder` version `3.11.1` with the `iorg` command.
- Carries forward `-rmc` as the short option alias for cache-delete mode while keeping `--rm-cache`.
- Keeps the aligned help output formatting and updates fallback package defaults to `JsonPit 3.11.1`, `OsLibCore 3.11.1`, `RaiUtils 3.11.1`, and `RaiImage 3.11.1`.
- Preserves the coordinated release order immediately before `PitSeeder`.

### Validation

- `dotnet test ImgSeeder.slnx --nologo -v minimal`
- `dotnet run --project ImgSeeder.csproj -- -h -c OneDrive -r LiveAfricaStageImage`
- Publication remains wired through the tag-triggered `publish-nuget.yml` workflow.

---

## 3.11.0

### Summary

- Releases `ImgSeeder` version `3.11.0` with the `iorg` command.
- Carries forward `-rmc` as the short option alias for cache-delete mode while keeping `--rm-cache`.
- Keeps the aligned help output formatting and updates fallback package defaults to `JsonPit 3.11.0`, `OsLibCore 3.11.0`, `RaiUtils 3.11.0`, and `RaiImage 3.11.0`.
- Preserves the coordinated release order immediately before `PitSeeder`.

### Validation

- `dotnet test ImgSeeder.slnx --nologo -v minimal`
- `dotnet run --project ImgSeeder.csproj -- -h -c OneDrive -r LiveAfricaStageImage`
- Publication remains wired through the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.4

### Summary

- Releases `ImgSeeder` version `3.10.4` with the `iorg` command.
- Adds `-rmc` as the short option alias for cache-delete mode while keeping `--rm-cache`.
- Aligns help output formatting to a fixed option column so glyph icons stay visually aligned.
- Preserves runtime behavior from `3.10.3`.

### Validation

- `dotnet test ImgSeeder.slnx --nologo -v minimal`
- `dotnet run --project ImgSeeder.csproj -- -h -c OneDrive -r LiveAfricaStageImage`
- Publication remains wired through the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.3

### Summary

- Releases `ImgSeeder` version `3.10.3` with the `iorg` command.
- Aligns runtime metadata (`AssemblyVersion`, `FileVersion`, and `InformationalVersion`) with package version `3.10.3` so `iorg -v` matches the published package.
- Keeps fallback package references at `JsonPit 3.10.2`, `OsLibCore 3.10.2`, `RaiUtils 3.10.2`, and `RaiImage 3.10.2`.
- Preserves CLI behavior from `3.10.2`.

### Validation

- `dotnet test ImgSeeder.slnx --nologo -v minimal`
- Publication remains wired through the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.2

### Summary

- Releases `ImgSeeder` version `3.10.2` with the `iorg` command.
- Aligns fallback package references to `JsonPit 3.10.2`, `OsLibCore 3.10.2`, `RaiUtils 3.10.2`, and `RaiImage 3.10.2`.
- Keeps `ImgSeeder`/`iorg` immediately before `PitSeeder` in the coordinated sequential release chain.
- Preserves the CLI behavior from `3.10.1`, including the current RaiImage filename-normalization flow used for structured tree ingestion.

### Validation

- `dotnet test ImgSeeder.slnx --nologo -v minimal`
- Publication remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.1

### Summary

- Releases `ImgSeeder` version `3.10.1` with the `iorg` command.
- Aligns fallback package references to `JsonPit 3.10.1`, `OsLibCore 3.10.1`, `RaiUtils 3.10.1`, and `RaiImage 3.10.1`.
- Keeps `ImgSeeder`/`iorg` immediately before `PitSeeder` in the coordinated sequential release chain.
- Preserves the CLI behavior from `3.10.0`, including the current RaiImage filename-normalization flow used for structured tree ingestion.

### Validation

- `dotnet test ImgSeeder.slnx --nologo -v minimal`
- Publication remains wired through the parent sequential release chain and the tag-triggered `publish-nuget.yml` workflow.

---

## 3.10.0

### Summary

- Releases `ImgSeeder` version `3.10.0` with the `iorg` command.
- Aligns fallback package references to `JsonPit 3.10.0`, `OsLibCore 3.10.0`, `RaiUtils 3.10.0`, and `RaiImage 3.10.0`.
- Keeps `ImgSeeder`/`iorg` immediately before `PitSeeder` in the coordinated sequential release chain.
- Preserves the CLI behavior from `3.9.1`, including the current RaiImage filename-normalization flow used for structured tree ingestion.

### Validation

- `dotnet test ImgSeeder.slnx --nologo -v minimal`
- Publication remains wired through the tag-triggered `publish-nuget.yml` workflow and the parent sequential release chain.

---

## 3.9.1

### Summary

- Releases `ImgSeeder` version `3.9.1` with the `iorg` command.
- Aligns fallback package references to `JsonPit 3.9.1`, `OsLibCore 3.9.1`, `RaiUtils 3.9.1`, and `RaiImage 3.9.1`.
- Publishes `ImgSeeder` through the coordinated sequential NuGet release chain immediately before `PitSeeder`.
- Keeps the CLI aligned with RaiImage's current filename normalization behavior for structured tree ingestion.

### Validation

- `dotnet test ImgSeeder.slnx --nologo -v minimal`
- NuGet publishing is handled by the tag-triggered `publish-nuget.yml` workflow and the parent sequential release chain.
