# Release Notes: RAIkeep v4.7.2

## 1. Release scope

This patch coordinates the thirteen active component repositories. The changes to media imports implement CR094_AIA_to_RAIkeep_Iorg_Adaptive_Streaming_and_Manifest_Types.md.

## 2. Streaming assets

RaiImage recognizes CMAF segments, DASH manifests, HLS playlists, WebVTT and JSON metadata. ImgSeeder preserves item filenames in each video's leaf, including compound suffixes. An album catalog belongs directly under its eight-character album folder.

## 3. Copy and verification

Every eligible input is written and SHA-256 verified. Receipts count new files as Copied and successful rewrites as Updated, including identical replays. Streaming imports preserve sibling posters and videos. See [CR094 acceptance](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RELEASE_NOTE_CR094.md) for the example paths and tests.

## 4. Amafu independence

The Amafu application and tests build without RaiGuard. The Amafu publishing workflow checks both restored dependency graphs. The umbrella enforces the exemption at compile time.

## 5. Cross-language verification

The CR077 replica uses Umgodi with an InqPath directory. Vikela checks the three intentional protected-attribute mutations by exact file, operation and diagnostic rule.

## 6. Release status

The [preflight record](https://github.com/Burkhardt/RAIkeep/blob/main/doc/RELEASE_PREFLIGHT_4.7.2.md) records candidate checks and the manual handoff to Engenho.
