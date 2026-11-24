# CR094 release note for the 4.7.2 candidate

Accepted provider change for RaiImage and ImgSeeder (`iorg`). Governing request: `CR094_AIA_to_RAIkeep_Iorg_Adaptive_Streaming_and_Manifest_Types.md`.

| Requirement | Delivered behavior |
| --- | --- |
| R1 — media types and probing | RaiImage recognizes CMAF `.m4s`, DASH `.mpd`, HLS `.m3u8`, WebVTT `.vtt`, and JSON catalogs and metadata. These assets bypass EXIF probing even with `--exif '*'`. The video-container predicate still covers MP4, MOV, WebM, MKV and AVI. |
| R2 — exact placement | The importer preserves item filenames, including representation suffixes, segment numbers and the double extension in `RBVist2601.meta.json`. The item leaf is `{Sub}/RBVist26/RBVist2601/`. For `album.json`, supply `--item-id RBVist26` to select `{Sub}/RBVist26/album.json`. With a configured cloud, `-r AIA --subscriber Vanguard --item-id RBVist26` resolves to `AIA/Image/Vanguard/RBVist26/`. Unrelated JSON such as `info.json` is skipped. |
| R3 — overwrite and receipts | Every eligible input is copied and SHA-256 verified. ReceiptVersion 3 counts a new destination as `Copied` and every successful rewrite as `Updated`, including a byte-identical replay. `Skipped` and `Failed` retain their meanings. The compatibility field `Unchanged` stays zero. The CLI rejects the retired `--no-overwrite` option. Streaming and catalog writes bypass derivative invalidation. |
| R4 — filesystem guardrails | Routing, writing and verification use the existing OsLib and RaiImage file and path APIs. Rail reported zero findings for RaiImage, ImgSeeder and both of their C# test projects. |

## Acceptance evidence

1. **MediaTypes_AcceptsCmafSegmentsManifestsAndJson** covers all five extensions, case-insensitive classification and their exclusion from the video-container predicate. Existing video-container tests cover all five containers.
2. **Organize_CmafSegmentsAndManifests_RoutesToLeaf8x2** checks a nested source ZIP containing initialization and numbered segments, eight representation segments, manifests, a variant playlist, metadata and WebVTT. It verifies exact paths and contents, Completed status, receipt totals and absence of EXIF results. A separate nine-file directory import with a recording exiftool executable on PATH observed zero invocations.
3. **Organize_AlbumJson_RoutesTo8CharAlbumDirectory** checks the CLI receipt and the catalog on disk. A separate run of the named-cloud form above verified the extra Image directory using a disposable cloud root.
4. **Organize_AlwaysCopiesAndOverwrites_PreservesPosterAndMp4** checks both changed and identical overwrites, including destination modification times, shorter replacement contents, receipt counts and sibling contents. CLI tests check both help screens and rejection of the retired switch. The nine-file smoke test reported nine copied on first import and nine updated on replay, with zero skipped and zero failed on both passes.

The RaiImage suite passed 180 tests and the ImgSeeder suite passed 94. These checks used local fixtures. Fleet replication and publication are separate release activities.

The umbrella Rail scan passed with zero findings across the applicable projects. The standalone Amafu application and its tests are exempt.
