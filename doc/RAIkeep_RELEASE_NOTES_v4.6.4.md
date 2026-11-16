# Release Notes: RAIkeep v4.6.4

November 15, 2026 · Local release candidate

## 1. Summary

Inqaba supplies the shared Python filesystem and configuration classes. Umgodi continues the original Python JsonPit implementation and provides both CLI names. The two standalone 0.1.0 releases precede their first coordinated release.

## 2. Scope

Local high-frequency fixtures use isolated Dropbox directories. The Nkosikazi–Mzansi remote suites continue to exercise the OneDrive production replication channel. [Fixture isolation handover](https://github.com/Burkhardt/RAIkeep/blob/main/doc/HANDOVER_Local_Test_Dropbox_Isolation.md)

## 3. Implementation

The manifest orders Umgodi after Inqaba and excludes the frozen Python distribution from future bumps. Tagged workflows build and test both active packages before publishing. The OsLib path regression covers nested hidden directories under the user's home.

## 4. Public contracts

Install `umgodi-json` and use `import umgodi`. Both `jpit` and `umgodi` belong to this distribution. Import the shared framework as `inqaba`. Existing installations pinned to legacy `jsonpit` 4.6.3 remain available. [Python migration notice](https://github.com/Burkhardt/jsonpit-python#jsonpit)

## 5. Validation

The coordinated validator passed 146 checks. The local .NET run passed 1,247 tests, followed by a five-test run including the new nested-directory regression. The Python suites passed 21 Inqaba, 210 Umgodi and 71 Vikela tests. Verification included 11 NuGet artifacts and clean Python wheel installs. The live remote suites and destructive sequence suites have separate execution requirements. [Verification record](https://github.com/Burkhardt/RAIkeep/blob/main/doc/verification/Release_4.6.4_candidate.json)

## 6. Manual release

RAI starts Engenho from the umbrella checkout after PyPI publisher setup. [Release handover](https://github.com/Burkhardt/RAIkeep/blob/main/doc/HANDOVER_RELEASE_PREP_v4.6.4.md)
