# CR019 — `WordCase` seam positions and placement in RaiUtils

**Requesting product:** AIA

**Requesters:** Zébio (Dev, AIA), Adele (PM, AIA), and RAI

**Receiving product:** RAIkeep (`RaiUtils` and `RaiImage`)

**Provider acceptance owner:** Codex (Owner, RAIkeep)

**Target release:** Coordinated RAIkeep v4.2.6

**Date reviewed:** 2026-09-02

**Status:** Formally accepted, implemented, verified, and prepared for RAI's manual release gate
**Reviewed AIA request:** [CR019 at the immutable AIA commit](https://github.com/Burkhardt/AIA/blob/9b4e98e810409067a477c4c798980ad27f163975/doc/CR019_AIA_to_RAIkeep_WordCase_Seams_and_Placement.md)

## Provider acceptance

RAIkeep accepts CR019 as an additive, coordinated v4.2.6 patch. The accepted
behavioral contract is the normative contract and acceptance table in the
reviewed AIA document:

- `WordSeams()` returns strictly increasing UTF-16 offsets into the unchanged
  source string.
- Pascal/camel transitions, acronym endings, digit-run openings, and the
  documented delimiter set produce the specified seams.
- Unicode text elements remain intact. Seams do not divide surrogate pairs or
  a base character from its combining marks.
- The operation is a lossless display projection. It does not validate an
  identifier, define AIA's identifier grammar, normalize text, generate HTML,
  or recover an identifier from rendered markup.
- `DependsOn[ScheduleRehearsal_Nomsa]` is a structured condition label, not one
  identifier. It remains an acceptance fixture because it proves punctuation
  preservation.
- General-purpose word-case behavior belongs in `RaiUtils`; `RaiImage` becomes
  a consumer rather than its implementation home.

## Provider correction to the requested CLR mechanism

The behavioral and package-boundary requirements are accepted. Section 5.2's
specific type-forwarding mechanism is replaced by an equivalent CLR-safe
compatibility mechanism for two technical reasons:

1. A .NET type forward can move a type between assemblies only while retaining
   its fully qualified namespace and type name. It cannot forward
   `RaiImage.WordCase` to the differently named `RaiUtils.WordCase`.
2. The existing public `WordCase` is constructible and stateful. It cannot
   simultaneously become the `static WordCase` extension container shown in
   the proposed signature.

The accepted implementation therefore uses:

- the canonical constructible `RaiUtils.WordCase` class;
- canonical `RaiUtils.StringHelper` extension methods, including
  `WordSeams`, `WordSplit`, `CamelSplit`, and `ToTitle`;
- a small derived `RaiImage.WordCase` facade retaining the old binary type and
  constructor/member resolution;
- ordinary, non-extension `RaiImage.StringHelper` forwarding methods retaining
  old static binary call signatures without creating extension ambiguity.

This realizes CR019's explicitly accepted source transition: recompiled
extension-method callers add `using RaiUtils;`. Existing compiled calls retain
their old CLR targets through the compatibility facades. No second word-case
implementation remains in RaiImage.

## Release authority

Implementation, verification, documentation, and coordinated v4.2.6 package
preparation are authorized. Tagging, pushing, NuGet publication, and execution
of the release chain remain behind RAI's separate manual release gate.
