# RaiUtils 4.2.2

Coordinated dependency release for the accepted CR008, CR009, and CR010 RAIkeep
boundaries.

- Carries `RaiException` and `ToolNotFoundException` forward unchanged.
- Remains dependency-light and independent of OsLib, RaiImage, and RaiDiagram.
- Aligns the shared package line used by RaiImage, RaiDiagram, JsonPit, and
  ImgSeeder on 4.2.2.
- CR014 introduces no process wrapper in RaiUtils and preserves its
  dependency-light boundary; tool execution remains in OsLib and RaiImage.

No tag or publication is authorized by these notes. RAI starts the coordinated
release chain manually after reviewing the prepared commits and verification.

Release verification: 22 RaiUtils Release tests passed.
