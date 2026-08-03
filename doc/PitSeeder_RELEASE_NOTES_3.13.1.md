# PitSeeder 3.13.1 Release Notes

## Summary

- Releases `PitSeeder` version `3.13.1`.
- Aligns CLI package metadata and fallback package references to `JsonPit 3.13.1` and `OsLibCore 3.13.1`.
- Keeps `PitSeeder` last in the coordinated release order, immediately after `ImgSeeder`/`iorg`.
- Carries forward `pits` subscriber identity behavior and local ticket-window regression coverage from `3.12.0`.
- Releases finite CLI process activity windows by default after normal completion, exceptions, Ctrl+C, and process exit when ownership can be verified.
- Adds `--retain-window` for explicitly retaining the prior timeout-based process activity behavior.
- Preserves the master writer ticket after seed operations so overlapping writers remain protected by change-file fallback.
- Uses per-PID process activity flags and ownership-verified epoch tombstones, written in place without deleting the OneDrive-backed flag path.

## Validation

- `dotnet test PitSeeder.slnx --nologo -v minimal`
- Two immediate consecutive `--wwwa` read-only exports against the configured OneDrive `AIA` pit succeeded.
- NuGet publishing remains wired through the parent sequential release chain and the tag-triggered `publish-pitseeder-nuget.yml` workflow in `RAIkeep`.
