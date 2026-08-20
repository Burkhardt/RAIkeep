# ADR002 — RaiDiagram Subscriber-Scoped Artifacts and Style Lookup

**Status:** Accepted
**Date:** 2026-08-17
**Decision owners:** RAIkeep and AfricaStage
**Related request:** `CR010_AfricaStage_to_RAIkeep_RaiDiagram_Subscriber_Scoped_Artifacts_and_Styles.md`

## Context

RaiDiagram needs to keep an authoritative `.raid` manifest, generated PlantUML,
the exact render configuration, and resulting images together. Reusable themes
and style profiles also need local, deterministic placement so applications
such as AIA and subscriptions or tenants such as those in AfricaStage can keep
their artifacts separate.

RaiImage already provides that separation through a subscriber path segment,
`ItemTreePath`, and `PathConventionType`. Treating the subscriber as a new owner
or identity would add authentication, authorization, and lifecycle concerns
that do not belong in these open-source libraries.

## Decision

1. `Subscriber` remains an ImageTree storage-routing segment only. It is not a
   principal, authenticated identity, authorization subject, ownership record,
   or tenant-management abstraction.
2. RaiImage provides `ImageTreeTextFile`, derived from OsLib `TextFile`, so text
   artifacts can use the same subscriber root, item id, `ItemTreePath`, and path
   convention as `ImageTreeFile` without masquerading as images.
3. RaiDiagram supplies typed `.raid`, `.puml`, config, style, and theme files on
   that placement contract. Rendered SVG, PNG, WebP, and JPEG remain
   `ImageTreeFile` instances.
4. A diagram's `.raid`, clean generated `.puml`, resolved `_config.puml`, and
   rendered images occupy one subscriber-local item bucket.
5. The resolved config has extension `puml` and RaiFile `NameExt` value
   `config`; `CenterUseCase_config.puml` is canonical.
6. Reusable style lookup receives an explicit, ordered list of subscriber
   locations from least to most specific. RaiDiagram performs no directory
   ascent, organizational inference, remote lookup, or filesystem enumeration.
7. Common and diagram-kind-specific layers are applied deterministically.
   Exact source names and hashes are preserved in config comments and SVG
   provenance.
8. Checked-in defaults are copied into a local subscriber only through an
   explicit seeding call. Seeding performs no network access and preserves an
   existing local file unless replacement is requested.
9. Systems with identity management may map their own application concepts to
   subscriber strings outside RAIkeep. Systems without identity management use
   the same APIs unchanged.

## Consequences

- AIA and AfricaStage can choose distinct ImageTree locations without coupling
  RaiImage or RaiDiagram to their domain or identity models.
- Diagram and image files share placement rules while retaining truthful file
  types.
- Generated PlantUML remains presentation-free; PlantUML receives the resolved
  local configuration through `-config`.
- A render can be audited from the co-located config and SVG style provenance.
- Callers must provide every desired fallback location explicitly.
- Subscriber strings do not grant access and must not be used as proof of an
  authenticated caller.

## Rejected alternatives

- **Introduce `DiagramArtifactOwner` or `ImageTreeArtifactIdentity`:** rejected
  because it implies an identity and authorization subsystem outside the
  package purpose.
- **Infer application/subscription/tenant parents from paths:** rejected because
  the hierarchy is consumer-specific and inference would make resolution
  surprising.
- **Use remote GitHub themes at render time:** rejected because rendering must
  remain deterministic and available offline.
- **Store text artifacts as `ImageTreeFile`:** rejected because `.raid` and
  `.puml` are not images.
- **Put style directives in generated PlantUML:** rejected because generated
  source is a semantic renderer input, while style is separate presentation
  intent.
