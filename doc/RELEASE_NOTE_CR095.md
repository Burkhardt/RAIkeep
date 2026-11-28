# CR095 release note for the RAIkeep 4.7.3 candidate

RAIkeep accepts the amended request from Adele and RAI. A flagged local pit still requires an exclusive write ticket. Once eligible, its owner can save immediately. A cloud pit still needs time for competing claims to arrive, even when only one flag is visible. [CR095_AIA_to_RAIkeep_Propagation_Wait_On_Single_Participant_And_Local_Pits.md](https://github.com/Burkhardt/AIA/blob/0114addfefc72157609feb9437fde128b154fad9/doc/CR095_AIA_to_RAIkeep_Propagation_Wait_On_Single_Participant_And_Local_Pits.md)

## Requirements

| Requirement | Candidate behavior |
| --- | --- |
| R1 | OsLib classifies the canonical pit directory. Local claimants serialize ticket acquisition across processes. A winner writes immediately and explicitly returns the ticket. Its exact machine/subscriber/PID identity is ineligible until the cooldown expires, including across reopen. A refused save publishes pending edits as change files. |
| R2 | On a cloud drive the returning machine yields across PIDs. A new winner observes the flag and remaining pit propagation windows plus the buffer, then rechecks authority and conflict evidence before writing. |
| R3 | Synchronous and asynchronous saves expose the milliseconds spent waiting for propagation through `PitSaveResult.WaitedMs`. Disk I/O and merge time are excluded. Existing outcome and fragment-count fields retain their meaning. |
| R4 | Local cooldown is `SyncPitDurationSeconds + BufferSeconds`. Local lookup checks `JsonPit/timing.json5` under the pit directory’s grandparent. Compiled defaults give a 65-second cooldown and zero local propagation wait. A cloud pit uses its configured drive root. See the [JsonPit guide](../JsonPit/GettingStarted.md) and [ADR-0016 §5.1](https://github.com/Burkhardt/AIA/blob/0114addfefc72157609feb9437fde128b154fad9/doc/ADR-0016-JSONPIT-TIMING-CALIBRATED-MASTER-TICKET-AND-ZERO-FLAG-READS.md). |
| R5 | RAI021 allows the Exec fixture’s indexed `cloud` parameter to take `Os.TestCloud` or `Os.LiveCloud` in a JObject or dictionary initializer. A literal provider still produces a diagnostic. |
| R6 | RaiGuard retires the obsolete RAI013 diagnostic for `pit.Reload()`. RAI013 still diagnoses direct pit-directory existence checks. |

## Acceptance evidence

| Acceptance check | What the test exercises |
| --- | --- |
| 1 · ExplicitReturn | The two-process test reads the held and returned records on disk, checks the exact owner, machine, claim and completion timestamps, and verifies a change-only writer leaves the owner’s ticket intact. |
| 2 · LocalTurnTaking_TwoProcesses | B attempts a save during A’s held turn. A writes, returns, then retries while B is idle. A publishes changes and the same B process wins immediately with zero propagation wait. |
| 3 · LocalCooldown_ExpiryAndReopen | A saves, reopens the pit and tries again on either side of the deadline. Removing the returned flag exercises the in-process cooldown independently of disk evidence. |
| 4 · CloudFairness_RetainsMachineCooldownAndWait | On TestCloud a ticket returned by another PID on this machine blocks a claim. A returned ticket from a simulated remote writer permits a winning save after propagation. A companion collision case changes ownership during the wait and checks the original canonical bytes. These tests model peer evidence on disk. |
| 5 · PitSaveResult_ReportsWaitedMs | Checks 2 and 3 assert zero for local writes. The cloud winner and asynchronous collision cases check the measured wait in the receipt. |
| 6 · RAI021_AllowsExecCloudParam_WhenValueFromOsTestCloud | Both initializer forms exercise the two configured role properties and a literal OneDrive provider. Expected diagnostic counts are zero, zero and one. |
| 7 · RAI013_AllowsPitReload_On472Plus | The analyzer permits a valid Reload call and retains coverage of its other pit-path diagnostic. |

## Selecting the tests

Use `dotnet test` with `--filter 'Category!=CloudEffect'` on JsonPit.Tests or ImgSeeder.Tests for ordinary serialization, merge, change-file, reload, save, CLI and local concurrency coverage. The local fixtures retain ticket arbitration and use isolated directories. AIA owns the corresponding downstream fixture migration and its end-to-end timing measurement.

Use `--filter 'Category=CloudEffect'` for configured cloud boundaries, propagation, conflict copies and remote-sync fixtures. Cloud fixtures resolve TestCloud from the real read-only RAIkeep configuration. A missing prerequisite produces a skip with its reason. A skip leaves that acceptance result open.

## Candidate verification on November 26

JsonPit ran 261 tests in 24.42 seconds. It passed 246 and skipped 15. Acceptance 1, 2, 3 and the local half of 5 passed, including both attempts from the same peer PID. Thirteen cloud cases skipped because the runner could not read the configured Dropbox timing file. Two SSH integration cases skipped because the local and Mzansi TestCloud roles differed. That run left acceptance 4 and the cloud half of 5 open.

All 135 RaiGuard tests passed, including acceptance 6 and 7. All 94 ImgSeeder tests passed. The repository-wide Rail check reported zero findings. These durations and counts cover the RAIkeep candidate. The projected runtime for AIA.slnx requires a downstream measurement.

The coordinated 4.7.3 metadata passed all 129 checks. The Release build passed all 245 local JsonPit tests in 19 seconds. A separate retry of the two cloud acceptance cases again skipped on access to the configured timing file. [Candidate preflight](RELEASE_PREFLIGHT_4.7.3.md)

The Release solution built with zero warnings and zero errors. All five packaged .NET tools installed from the local candidate feed and reported 4.7.3. The November 26 validator run left four checks unresolved, covering the umgodi-json suite and three CLI parity checks.

## November 27 interactive cloud results

Rainer confirmed acceptance 4 and the cloud portion of acceptance 5 on the configured TestCloud. His CloudEffect run reported 13 passed, two SSH skips and two split-master recovery failures. The two fixtures now use the synchronous recovery scan in `Reload()` with explicit checks for the losing process and the current ticket holder. On the corrected candidate, both fixtures passed. Rainer recorded 15 CloudEffect passes, two SSH skips due to differing TestCloud roles and zero failures. The release validator exited successfully with all 146 checks passed. [Candidate preflight](RELEASE_PREFLIGHT_4.7.3.md)
