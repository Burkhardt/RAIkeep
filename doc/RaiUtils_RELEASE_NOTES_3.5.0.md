# RaiUtils 3.5.0 Release Notes

## Highlights

- Version bumped to `3.5.0`.
- RaiUtils documentation now aligns with the shared `3.5.0` package line used in `RAIkeep`.
- The documented package-stack support claim now names `OneDrive`, `GoogleDrive`, and `Dropbox`.
- RaiUtils package metadata was aligned with the `3.5.0` workspace release.

## Cross-Package Alignment

- RaiUtils continues to avoid a direct runtime dependency on OsLib types.
- The docs now explicitly align with JsonPit's `Id`-based identifier contract and legacy `Name` normalization behavior.

## Validation

- The package remains a lightweight utility layer in the `RAIkeep` stack and keeps its existing runtime behavior.
- RaiUtils remained green in the full workspace validation run for `3.5.0`.
