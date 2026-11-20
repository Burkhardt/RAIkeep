# Windows distribution and code-signing pilot — RAIkeep 4.6.7

Date: November 19, 2026

Audience: Adele and the RAIkeep / Engenho team

Status: Pilot complete; decision supplied by Rainer

## Decision

RAIkeep retains its existing distribution channels. This pilot does not authorize
WinGet as a remedy for Windows Smart App Control blocks, signing work, or
automatic switching between installation formats. Further evaluation requires a
separate decision.

## Reported results

Testing took place on **Themba-win, the native Windows 11 environment**, with
Smart App Control enforced. These are not results from Themba's WSL environment.

| CLI, version 4.6.7 | Isolated NuGet / .NET tool | Standalone Windows ZIP |
| --- | --- | --- |
| `pits` | Passed startup and seed/export | Blocked at executable launch |
| `raid` | Blocked at tool-launcher execution | Passed startup, diagram import and validation |

All inspected executables and assemblies were unsigned and lacked
`Zone.Identifier`. The isolated installations contained byte-identical
`OsLib.dll` files, and `pits` successfully exercised that library. The evidence
does not identify OsLib as a universally blocked component.

Neither tested packaging method provided a common successful route for both
CLIs on this Windows configuration. The precise reason for the different
acceptance decisions remains unestablished. WinGet itself was not tested, and
the pilot provides no evidence that it would remove the observed blocks.

The working combinations are useful for local operation. They do not establish
compatibility across future releases, other Windows machines or enterprise
policies. Standalone `raid`'s visual SVG review remains pending; this does not
reopen the completed pilot or authorize further execution.

## Team actions

- Preserve Rita's original logs, artifact hashes, test results and generated
  output, including the SVG awaiting visual review.
- Leave global installations and Windows security settings unchanged under
  this pilot.
- Keep WinGet remediation and signing evaluation paused pending a separate
  decision. Do not implement automatic installation-format fallback.
- Do not advertise general Smart App Control compatibility or ask users to
  disable protections.
- Treat Windows execution compatibility as an unresolved distribution limitation,
  distinct from application functionality.

## Evidence and historical instructions

This decision records the supplied pilot findings. It does not claim a new test
run or an independent inspection of the raw logs and hashes. Their exact values
and storage locations were not included in the decision; keep the originals with
Rita's evidence rather than reconstructing or inventing them here.

The historical test briefs are retained as procedural context, not raw results:

- [Standalone CLI pilot](RITA_WINDOWS_STANDALONE_PILOT_4.6.7.md)
- [.NET tool follow-up](RITA_WINDOWS_DOTNET_TOOL_FOLLOWUP_4.6.7.md)

This decision supersedes their proposed next steps, including a possible WinGet
trial and global installation checks. No further tests, updates or provisioning
are authorized by those archived briefs.

**The pilot identified working artifact combinations for the tested release,
but did not establish a dependable, suite-wide solution for unsigned execution
under enforced Smart App Control.**
