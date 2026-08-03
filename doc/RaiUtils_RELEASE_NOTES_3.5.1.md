# RaiUtils 3.5.1 Release Notes

## Highlights

- Version bumped to `3.5.1`.
- The NuGet package id is now `RaiUtils`.
- The previous split between `RaiUtils` and `RaiUtilsCore` on NuGet is consolidated onto the `RaiUtils` package id for current releases.

## Packaging

- `RaiUtils.csproj` now packs as `RaiUtils` instead of `RaiUtilsCore`.
- The runtime API and `RaiUtils` namespace stay unchanged.
- This change is intended to simplify downstream package references in `RaiImage` and `JsonPit`.

## Validation

- The package remains a lightweight utility layer in the `RAIkeep` stack.
