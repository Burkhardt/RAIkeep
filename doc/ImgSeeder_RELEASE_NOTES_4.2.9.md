# ImgSeeder 4.2.9 Release Notes

ImgSeeder 4.2.9 implements its part of accepted
[CR022](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md).

- `iorg organize` no longer creates a subscriber staging tree in `Os.TempDir`.
- Each source image is copied directly to its final ItemTree path through the
  `RaiFile` boundary.
- The retained `tempRoot` API parameter is inert for binary and source
  compatibility; tests prove that it is never materialized.
- Configured-cloud regression coverage verifies direct final-path creation and
  preservation of the source file.

Fallback dependencies align to 4.2.9 and the CLI reports `iorg v4.2.9`.
