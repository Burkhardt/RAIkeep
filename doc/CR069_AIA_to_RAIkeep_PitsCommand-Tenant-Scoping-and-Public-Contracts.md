# CR069: Tenant-scoped PitsCommand requests and public contracts

Status: Accepted; implementation prepared for the coordinated 4.5.14 release.

## Contract

`PitsCommandOptions.Tenant` carries a bare tenant directory name unchanged as
`-r <tenant>`. `PitRoot` carries an explicit typed filesystem root as
`--pitroot <absolute-path>`. Setting both throws before process execution.
Tenant-scoped mutations require an explicit configured `CloudProvider`.
Empty names, path traversal, path separators, drive syntax, and option-shaped
tenant values are rejected.

```csharp
var request = PitsSeedRequest.ForPit("Person", sourceFile) with
{
    Options = new PitsCommandOptions
    {
        Tenant = "SampleTenant",
        CloudProvider = "OneDrive",
        NoLogo = true
    }
};
var result = new PitsCommand().Seed(request);
```

The generated tokens are `seed`, `Person`, `--source`, the source filename,
`-r`, `SampleTenant`, `--cloud`, `OneDrive`, and `--nologo`. No tenant-to-RaiPath
conversion occurs. Source paths used over SSH must exist on the remote host.

## Coordination and documentation

The process-local gate identity includes the effective execution host, cloud,
tenant or filesystem root, and pit. Same-target calls across wrapper instances
serialize; different tenants can execute independently. WWWA and single-pit
operations share the corresponding pit gates.

Public factories remain the entry points for `PitsSeedRequest`; the API does not
need a default request with missing required fields. The package ships XML
documentation for `PitsCommand`, `PitsCommandOptions`, `PitsSeedRequest`, and
`PitsTarget`, including a factory/with-expression example. Release validation
inspects the XML inside the actual OsLibCore package.

## RaiGuard

RAI006 documents the canonical typed request and links to this contract. Its
code fix handles only immediately executed seed requests whose arguments can be
recovered reliably. Unknown flags, dynamic/interpolated argument strings,
host-dependent quoting, buffered stdin, other verbs, and deferred process
execution receive guidance without an automatic rewrite. The fix requires the
updated public OsLib contract in the consuming compilation.

The release also includes the existing RAI011 correction from RaiGuard commit
`96817b5`: freshly generated items are not treated as proven pit snapshots.
Actual snapshot Read-Modify-Write remains diagnosed.

## Verification and adoption

- Exact-token tenant seeding, invalid addressing, and mutation-cloud checks.
- Same-tenant and different-tenant concurrency, including WWWA overlap.
- Packaged XML documentation for 49 public contract entries.
- RAI006 code-fix compilation and conservative refusal cases.
- RAI011 fresh-item and proven-snapshot regression cases.
- Coordinated 4.5.14 version and release validation.

The AIA team owns caller migration and consumer build verification; see the
[AIA handover](https://github.com/Burkhardt/RAIkeep/blob/main/doc/HANDOVER_CR069_TO_AIA.md).
RAI starts the release chain manually after preparation is complete.
