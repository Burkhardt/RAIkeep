# RAIkeep 4.3.1 Release Notes

RAIkeep 4.3.1 is the coordinated seven-package delivery of accepted
[CR026 Captured-Revision Fidelity and Object-Reference Stereotypes](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR026_AIA_to_RAIkeep_Diagram_Builder_Revision_Fidelity_and_Reference_Stereotypes.md).

## RaiDiagram repair and enhancement

- `DiagramModelIdentity.CapturedRevision` is treated as an opaque string across
  typed builders, model snapshots, JSON5 serialization, and `.raid` parsing.
- ISO 8601 values retain their exact characters, precision, and offset instead
  of becoming culture- or machine-time-zone-dependent strings.
- `OneUseCaseDiagramBuilder.AddObjectReference(...)` accepts an optional
  semantic stereotype; explicit verbs render directly while the existing
  bucket-derived label remains the default.
- Existing `.raid` JSON5 syntax and validation behavior remain compatible.

OsLibCore, RaiUtils, RaiImage, JsonPit, ImgSeeder, and PitSeeder have no
behavioral changes in this patch; they participate so all seven package and
fallback dependency versions remain aligned on 4.3.1.

CR027 class generalization is accepted separately for v4.3.2 and is not part of
v4.3.1. Tagging, GitHub labeling, workflow dispatch, and NuGet publication
remain behind RAI's manual `scripts/release-chain.sh 4.3.1` gate.
