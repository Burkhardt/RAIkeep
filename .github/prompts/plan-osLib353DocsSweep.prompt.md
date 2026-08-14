## Plan: OsLib 3.5.3 Docs Sweep

Documentation-only update for OsLib: move the OsLib docs from 3.5.2 to 3.5.3, refresh the diagrams that expose OsLib types, and document CanonicalPath as deprecated/legacy without touching source, tests, or package metadata.

**What I would update**

1. OsLib markdown docs
2. OsLib PlantUML diagrams
3. Root-level dependency diagrams that mention OsLib types
4. Tracked rendered diagram artifacts only if they are expected to stay in sync with the .puml sources

**Planned steps**

1. Update the primary OsLib markdown docs from 3.5.2 to 3.5.3.
   Files:
   [OsLib/README.md](https://github.com/Burkhardt/OsLib/blob/main/README.md)
   [OsLib/API.md](https://github.com/Burkhardt/OsLib/blob/main/API.md)
   [OsLib/ARCHITECTURE-ALIGNMENT.md](https://github.com/Burkhardt/OsLib/blob/main/ARCHITECTURE-ALIGNMENT.md)

2. Add a new OsLib 3.5.3 release-notes document and repoint the OsLib docs to it.
   Reference template:
   [OsLib/RELEASE_NOTES_3.5.2.md](https://github.com/Burkhardt/RAIkeep/blob/main/doc/OsLib_RELEASE_NOTES_3.5.2.md)
   Planned new file:
   OsLib/RELEASE_NOTES_3.5.3.md

3. Update CanonicalPath documentation wording so it is clearly marked deprecated/legacy and readers are directed toward RaiPath-based usage.
   Affected docs:
   [OsLib/README.md](https://github.com/Burkhardt/OsLib/blob/main/README.md#L79)
   [OsLib/API.md](https://github.com/Burkhardt/OsLib/blob/main/API.md#L322)
   [OsLib/API.md](https://github.com/Burkhardt/OsLib/blob/main/API.md#L345)

4. Update the OsLib file hierarchy diagram to show CanonicalPath as deprecated, while keeping it visible because it still exists in source.
   Files:
   [OsLib/RaiFile-Hierarchy.puml](OsLib/RaiFile-Hierarchy.puml)
   [OsLib/RaiFile-Hierarchy.svg](OsLib/RaiFile-Hierarchy.svg)

5. Update the umbrella diagrams that currently surface CanonicalPath so they stay consistent with the OsLib docs.
   Files:
   [RAIkeep-Library-Dependencies.puml](RAIkeep-Library-Dependencies.puml#L54)
   [RAIkeep-Package-Dependencies.puml](RAIkeep-Package-Dependencies.puml#L21)

6. Run a final verification sweep for remaining 3.5.2 and CanonicalPath references in the targeted doc surface.

**Files I would leave alone**

- [OsLib/OsLib.csproj](OsLib/OsLib.csproj)
Reason: changing this would be a package/version implementation change, not documentation-only.

- [OsLib/CanonicalFile.cs](OsLib/CanonicalFile.cs)
Reason: source already marks CanonicalPath obsolete; no code changes requested.

- [OsLib/OsLib.Tests/PathConventionsTests.cs](OsLib/OsLib.Tests/PathConventionsTests.cs)
Reason: test/code scope, not docs.

- [OsLib/Os-ClassDiagram.puml](OsLib/Os-ClassDiagram.puml)
Reason: it does not document CanonicalPath.

- Generated files under bin/ and obj/
Reason: never edit manually for a docs-only pass.

**CanonicalPath status I would document**

- CanonicalPath still exists in source
- It is already obsolete in code
- The docs should describe it as deprecated/legacy
- The docs should not say it has been removed unless implementation scope is approved later

**Scope boundary**

Included:
- OsLib markdown docs
- OsLib PlantUML docs
- Root dependency diagrams that mention OsLib types

Excluded:
- csproj/package metadata
- source files
- tests
- build artifacts
- downstream package docs in JsonPit, RaiUtils, and RaiImage unless you want a full workspace-wide 3.5.3 doc sweep

**Verification**

1. Search the targeted docs and .puml files for 3.5.2 and confirm only intentional historical references remain.
2. Search the targeted docs and .puml files for CanonicalPath and confirm each remaining mention is explicitly marked deprecated/legacy where appropriate.
3. Confirm README/API links point to the intended latest OsLib release notes.
4. If SVGs are tracked, confirm they match the updated .puml source.

Two decisions would tighten the handoff:

1. Create a new OsLib 3.5.3 release-notes file, or keep 3.5.2 as the latest formal notes and treat 3.5.3 as an unreleased docs pass.
Recommendation: create a new 3.5.3 notes file.

2. Update only OsLib docs plus the root diagrams, or also sweep all workspace docs that mention OsLibCore 3.5.2.
Recommendation: keep this pass limited to OsLib plus the two root diagrams.
