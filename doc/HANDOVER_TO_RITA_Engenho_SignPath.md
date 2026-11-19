# Rita: integrate SignPath into the RAIkeep release chain

Implement this after SignPath Foundation accepts RAIkeep and supplies the project
and signing policy configuration. RAIkeep 4.6.6 publishes the application notice;
it does not enable signing. Rainer starts releases and provisioning manually.

## Scope

Keep NuGet and PyPI as the package distribution channels. Cover the RAIkeep-owned
Windows binaries listed in the public
[signing policy](https://github.com/Burkhardt/RAIkeep/blob/main/README_codesigning.md#proposed-windows-artifact-inventory).
Include every shipped target-framework/runtime variant, analyzer/code-fix DLL,
and copy of our libraries bundled into CLI packages. Preserve upstream signatures;
do not submit third-party binaries as our own. Engenho's proprietary binaries are
outside this Foundation application. Python source distributions and pure-Python
wheels are not Authenticode targets.

## Build and signing sequence

1. Retain the existing dependency DAG and package-specific GitHub Actions builds.
   All jobs leading to the OSS signing request must use GitHub-hosted runners.
   Resolve the exact source commit and dependency versions before building.
2. Build final release outputs once, including generated Windows apphosts. Upload
   unsigned inputs as GitHub workflow artifacts with repository/run provenance.
3. Submit through SignPath's GitHub integration. Configure organization ID,
   project slug, artifact configuration and signing policy from the approved
   account. Keep the API token in GitHub secrets. Pin reviewed action revisions.
   Grant the SignPath GitHub App access only to the approved repositories.
4. Wait for the required human approval and signing completion. Engenho should
   report `awaiting signing approval`, the workflow URL and request identifier.
   Use bounded polling and resumable checkpoints; a pending approval is not a
   successful publication. Never substitute unsigned outputs after failure.
5. Retrieve the returned signed artifacts. Verify Authenticode validity, expected
   publisher, timestamp and complete artifact coverage on Windows. Record hashes,
   source SHA, signing request ID, package version, run and verification evidence.
6. Package the returned bytes without rebuilding or modifying signed PE files.
   If signing uses a configured archive/package input, use the returned archive
   and validate its contents instead. A NuGet package signature is a separate
   operation and is not a replacement for embedded PE Authenticode signatures.
7. Publish only verified final packages to NuGet. Gate consumers on the indexed
   signed dependency version. Retain existing PyPI publishing and verification.
   Complete the umbrella tag only after all package gates pass.

Consult the current official action interface before implementation:
[SignPath GitHub integration](https://docs.signpath.io/trusted-build-systems/github).
The documented flow uses `github-artifact-id`, `wait-for-completion: true`, and
`output-artifact-directory`. Artifact IDs must belong to the current verified
workflow, not arbitrary uploaded files.

## Resolve the global tool launcher before claiming success

The current framework-dependent `dotnet tool install` path generates a local
launcher such as `%USERPROFILE%\.dotnet\tools\pits.exe`. It does not possess a
RAIkeep signing certificate and does not sign that generated launcher. Signing
`pits.dll` and `OsLib.dll` alone does not establish a signature on `pits.exe`.

Prototype a NuGet-compatible path using SDK-supported prebuilt shims or .NET 10
RID-specific tools. Check actual SDK support and installed bytes; do not assume
that a platform-specific package automatically solves launcher signing. Preserve
cross-platform installation and document any minimum SDK version. If extra RID
packages are necessary, register every package in Engenho's publication/indexing
checks and resolve installation on supported architectures before rollout.

- [Microsoft global tool installation](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-tool-install)
- [Microsoft RID-specific tools](https://learn.microsoft.com/en-us/dotnet/core/tools/rid-specific-tools)

Test `amafu`, `pits`, `iorg`, `raid` and `rail` after a clean NuGet installation
and an upgrade on Windows with Smart App Control enabled. Verify signatures of
the executable actually resolved by `Get-Command`, plus RAIkeep DLLs loaded from
the tool store. Run `--help` and a disposable local smoke fixture. No production
pit changes, security-policy exceptions or local self-signing are acceptance
substitutes. Check ordinary `dotnet add package` consumption and analyzer loading
as well. Provisioning should install verified published artifacts, not sign them.

## Recovery and activation

Persist signing progress alongside existing Engenho release checkpoints. A retry
must retrieve the already approved artifact, or resume its request, rather than
rebuild different bytes under an existing version/tag. Keep published tags and
package versions immutable. Test rejected requests, expired waits, invalid or
missing signatures, missing artifacts and partial publication recovery.

Update the root policy, component README attribution and release notes only when
signing is actually active. Identify exactly which artifacts and installation
paths are covered. Foundation approval, MFA, human signing approval and a tested
Windows launcher remain activation prerequisites, not promises made by 4.6.6.

Deliver workflow changes, Engenho checkpoint/status changes, the Windows test
evidence and configuration instructions. Stop before starting a production
release or fleet provisioning; Rainer starts those manually.
