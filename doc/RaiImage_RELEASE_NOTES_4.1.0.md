# RaiImage 4.1.0

Implements the RaiImage portion of
`CR008_AIA_to_RAIkeep_OsLib_RaiImage_Boundary_Enhancements.md`.

- Adds `RaiImageIOException` and `RaiImageNotFoundException`.
- Missing lookup directories throw `RaiPathNotFoundException`; missing images in
  an existing lookup location throw `RaiImageNotFoundException`.
- Missing ImageMagick and PlantUML executables throw `ToolNotFoundException`
  instead of `System.IO.FileNotFoundException`.
- Image files accept asynchronous byte chunks through inherited
  `WriteFromAsync(IAsyncEnumerable<byte[]>, CancellationToken)`.
- The originally requested `RaiImageFileNotFoundException` name was deliberately
  refined during acceptance to distinguish missing paths from missing images.

Release verification: 97 RaiImage Release tests passed.
