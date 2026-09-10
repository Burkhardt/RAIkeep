# RaiImage 4.2.9 Release Notes

RaiImage 4.2.9 implements its part of accepted
[CR022](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md).

- `ImageMagick.JpegTran` no longer moves an established image into `Os.TempDir`.
- The external tool receives isolated temporary input and output paths.
- A successful result is copied into the continuously present destination path;
  a failed invocation leaves the original bytes and pathname unchanged.
- Regression tests exercise success and failure against a real configured
  CloudDrive and verify that no delete or rename event occurs at the image path.

Fallback dependencies align to `OsLibCore 4.2.9` and `RaiUtils 4.2.9`.
