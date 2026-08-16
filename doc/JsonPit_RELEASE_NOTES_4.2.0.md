# JsonPit 4.2.0

Coordinated release for the seven-package RAIkeep 4.2 line.

- Carries the 4.1.0 abandoned-instance watcher ownership fix forward.
- Forced collection can remove the weak registry target and make a canonical
  path reopenable.
- The finalizer remains deliberately free of recovery publication, watcher
  disposal, and filesystem I/O.
- Aligns fallback dependencies on OsLibCore and RaiUtils 4.2.0.
- Makes `UseLocalRAIkeepSources=false` force package references and removes
  duplicate direct OsLib/RaiUtils project references from the test project, so
  package-only release validation exercises the intended dependency graph.
- Stabilizes the real Nkosikazi-to-Mzansi client phase by renewing the exact
  owner lease after the initial cloud sync and waiting for that specific ticket
  timestamp before launching the remote CLI.

Release verification: the focused finalizer regression passed, and the complete
JsonPit Release suite passed 146 tests including configured cloud/remote
scenarios.
