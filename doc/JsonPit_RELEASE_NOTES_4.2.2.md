# JsonPit 4.2.2

Coordinated dependency release for the RAIkeep 4.2.2 package line.

- Carries the abandoned-instance watcher ownership and finalizer regression fix
  forward unchanged.
- Forced collection can remove the weak registry target and make the canonical
  path reopenable.
- The finalizer performs no recovery publication, watcher disposal, or
  filesystem I/O.
- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.2.
- Keeps `UseLocalRAIkeepSources=false` as the package-only release boundary.
- CR014 remote integration helpers construct preferred `pits seed` arguments
  through `OsLib.PitsCommand` and execute SSH through `SshSystem`; no JsonPit
  production behavior is moved into the wrapper tests.

Released as part of the coordinated RAIkeep v4.2.2 release.

Release verification: the focused finalizer regression passed and the complete
JsonPit Release suite passed 146 tests, including configured cloud/remote
scenarios.
