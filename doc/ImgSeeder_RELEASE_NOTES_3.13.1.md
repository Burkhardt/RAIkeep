# ImgSeeder 3.13.1 Release Notes

## Summary

`ImgSeeder 3.13.1` is the coordinated `iorg` CLI release aligned with the four `3.13.1` RAIkeep libraries.

## Changes

- Updated assembly, file, informational, and package versions to `3.13.1`.
- Updated fallback package defaults to `JsonPit 3.13.1`, `OsLibCore 3.13.1`, `RaiUtils 3.13.1`, and `RaiImage 3.13.1`.
- Updated test-project package defaults to the same release line.
- Carries forward `-rmc` as the short alias for cache deletion while retaining `--rm-cache`.
- Refreshed the README and centralized release-note link.

## Compatibility

- No `iorg` CLI behavior changed from `3.13.0`.
- Existing command names and options remain unchanged.

## Validation

- `ImgSeeder.Tests`: `8` passed, `0` failed in the coordinated validation run.
- The umbrella `RAIkeep.slnx` build succeeds with the local `3.13.1` dependency chain.

## Release sequencing

`ImgSeeder` is fifth in the coordinated release chain. Its GitHub push/tag must wait for JsonPit workflow success, flat-container visibility, and the full `330`-second hold. `PitSeeder` must wait for the same checks after ImgSeeder publishes.
