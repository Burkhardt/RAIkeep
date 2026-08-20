# RaiImage 4.2.2

Coordinated patch release implementing the RaiImage portion of accepted
`CR010_AfricaStage_to_RAIkeep_RaiDiagram_Subscriber_Scoped_Artifacts_and_Styles.md`
and carrying accepted CR008 forward.

It also implements the RaiImage tool-boundary portion of accepted
`CR014_RAI_to_RAIkeep_Typed_CLI_Command_Wrappers.md`.

- Adds `ImageTreeTextFile`, a truthful OsLib `TextFile` placed with the existing
  subscriber root, item id, `ItemTreePath`, and `PathConventionType` contract.
- Keeps `.raid`, `.puml`, and `_config.puml` text artifacts in the same item
  bucket as SVG, PNG, WebP, and JPEG images without treating text as an image.
- Represents resolved configuration with `NameExt = "config"` and
  `Ext = "puml"`, producing names such as `ScheduleRehearsal_config.puml`.
- Extends the PlantUML boundary with local `-config` injection and typed
  source/config result handles while retaining the 4.2.0 compatibility handles.
- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.2.
- Routes all ImageMagick facade calls through `ImageMagickCommand` and adds
  public `OptiPngCommand` and `JpegTranCommand` wrappers.
- Passes optimizer paths/options as discrete process tokens and retains
  synchronous/asynchronous `RaiSystemResult` output and exit-code behavior.
- Confirms PlantUML remains behind `PlantUmlCommand`, including the deliberate
  headless `java -jar` launch owned inside that wrapper.

No identity-management abstraction, direct theme download, tag, or publication
is introduced by this preparation.

Release verification: 104 RaiImage Release tests passed in one run, including
the real ImageMagick transparency integration.
