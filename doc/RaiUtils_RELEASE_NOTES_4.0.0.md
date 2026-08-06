# RaiUtils 4.0.0 Release Notes

## Summary

`RaiUtils 4.0.0` is the coordinated dependency-alignment release for `OsLibCore 4.0.0`.

## Changes

- Updated package version and release metadata to `4.0.0`.
- Aligned the OsLibCore package baseline with `4.0.0`.
- Refreshed README, API documentation, centralized release-note links, and the class-diagram release marker.

## Compatibility

- No RaiUtils production API or behavior changed from `3.13.0`.
- Configuration behavior remains unchanged.

## Validation

- `RaiUtils.Tests`: `21` passed, `0` failed in the coordinated validation run.
- The umbrella `RAIkeep.slnx` build succeeds with the local `4.0.0` sources.

## Release sequencing

`RaiUtils` is second in the coordinated release chain. Its GitHub push/tag must wait for OsLibCore workflow success, flat-container visibility, and the full `330`-second hold. `RaiImage` must wait for the same checks after RaiUtils publishes.
