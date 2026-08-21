# RaiDiagram 4.2.2 Release Notes

**Accepted requests:**
`CR009_AIA_to_RAIkeep_RaiDiagram_Package.md` and
`CR010_AfricaStage_to_RAIkeep_RaiDiagram_Subscriber_Scoped_Artifacts_and_Styles.md`,
with the CR014 external-call audit

- Confirms the CR009 consumer construction surface:
  `DiagramModel.FromManifest(...)` and
  `DiagramDestination.CreateSubscriberRoot()` are public.
- Adds typed `DiagramArtifactSet`, `RaidFile`, `PumlSourceFile`,
  `PumlConfigFile`, `PumlStyleFile`, and `PumlThemeFile` placement.
- Resolves common and diagram-kind style layers from an explicit
  least-to-most-specific list of local subscriber locations.
- Performs no identity management, authorization, inferred hierarchy, parent
  traversal, remote theme lookup, or implicit filesystem seeding.
- Applies one deterministic, co-located `_config.puml` through PlantUML
  `-config`; generated `.puml` remains presentation-free.
- Embeds config, render, style, and ordered style-layer provenance in SVG.
- Includes the synchronized `ScheduleRehearsal` `.raid`, `.puml`,
  `_config.puml`, and official PlantUML SVG example.
- The CR014 external-call audit confirms rendering remains exclusively behind
  `RaiImage.PlantUmlCommand`; RaiDiagram contains no independently baked
  PlantUML process launch.

The subscriber is an ImageTree storage-routing segment only. The architectural
decision is recorded in
`ADR002_RaiDiagram_Subscriber_Scoped_Artifacts_and_Style_Lookup.md`.

No tag or publication is authorized by these notes. RAI starts the coordinated
release chain manually after reviewing the prepared commits and verification.

Local release verification: all 34 RaiDiagram Release tests passed through the
real PlantUML renderer. The four real-renderer tests are categorized as
`PlantUMLIntegration`; environments without a complete PlantUML/Graphviz
installation report them as skipped while continuing to enforce the remaining
30 tests. `RAIDIAGRAM_REQUIRE_REAL_PLANTUML=1` makes an unavailable renderer a
hard failure for dedicated integration environments.
