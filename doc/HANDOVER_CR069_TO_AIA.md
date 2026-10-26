# CR069 adoption instructions for the AIA team

Apply these changes after the coordinated 4.5.14 packages are visible on NuGet.
RAIkeep has prepared the library and analyzer changes; AIA source was not edited.

## Upgrade package references

In AIA's `Directory.Packages.props`, update the existing coordinated RAIkeep
references to 4.5.14, including `OsLibCore` and `RaiGuard.Analyzer`. The analyzer
package includes the existing RAI011 fix for freshly generated items and the
updated RAI006 guidance/code fix. OsLibCore supplies the new tenant option and
factory documentation.

## Migrate TenantProvisioningService

In `AIA.Core/Services/TenantProvisioningService.cs`, keep the existing typed
`TextFile` creation, save, and `finally` cleanup in `SeedThroughPits`.
Replace the interpolated command string and raw RaiSystem execution inside the
`try` block with:

```csharp
var request = PitsSeedRequest.ForPit(pit, source) with
{
    Options = new PitsCommandOptions
    {
        Tenant = tenantName,
        CloudProvider = cloudProvider,
        NoLogo = true
    }
};
var result = new PitsCommand().Seed(request);
if (result.ExitCode != 0)
    throw new TenantProvisioningException(
        $"pits could not seed {pit} for '{tenantName}' (exit {result.ExitCode}). " +
        $"{result.StandardError.Trim()}".Trim());
```

The existing `source` variable is a `TextFile`, which derives from `RaiFile` and
can be passed directly to `ForPit`. Remove the unused `PitsExecutable` constant
and update the method's stale comment about waiting for a typed wrapper.
Keep `tenantName` as a string; constructing a `RaiPath` from it would turn it
into a filesystem address. `Tenant` and `PitRoot` cannot be supplied together.

The dynamic command string in this caller deliberately receives no automatic
code fix. The RAI006 lightbulb is limited to safely recoverable constant tokens.
Existing result/error handling and source cleanup should remain in place.

## Verify UseCaseInstantiator

Keep the fresh-item construction and `_activityPit.Add(item)` loops in
`AIA.Core/Services/UseCaseInstantiator.cs`. The updated analyzer no longer treats
these freshly generated collections as proven pit snapshots. Do not add warning
suppression or change the fresh-item insertion flow to silence RAI011.

Actual loaded snapshots still require sparse mutation. Retain that protection.

## Consumer acceptance checks

From the AIA repository, after upgrading package versions:

```bash
dotnet restore AIA.slnx --force
dotnet build AIA.slnx --no-restore
```

Confirm that RAI006 is absent at the migrated provisioning call and RAI011 is
absent at the fresh-item insertion sites, with no suppression added. Report any
unrelated warnings separately. Exercise tenant provisioning against a configured
test tenant and verify that records land beneath the intended cloud/tenant root.
The `pits` executable itself must also be upgraded to the coordinated version.
