# RaiUtils 3.13.1 Release Notes

## Summary

`RaiUtils 3.13.1` is the coordinated dependency-alignment release for `OsLibCore 3.13.1`.

## Changes

- Updated package version and release metadata to `3.13.1`.
- Aligned the OsLibCore package baseline with `3.13.1`.
- Refreshed README, API documentation, centralized release-note links, and the class-diagram release marker.

## Compatibility

- No RaiUtils production API or behavior changed from `3.13.0`.
- Configuration behavior remains unchanged.

## Validation

- `RaiUtils.Tests`: `21` passed, `0` failed in the coordinated validation run.
- The umbrella `RAIkeep.slnx` build succeeds with the local `3.13.1` sources.

## Release sequencing

`RaiUtils` is second in the coordinated release chain. Its GitHub push/tag must wait for OsLibCore workflow success, flat-container visibility, and the full `330`-second hold. `RaiImage` must wait for the same checks after RaiUtils publishes.
