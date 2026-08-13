# JsonPit 4.1.0

Aligns JsonPit with the CR008 OsLibCore/RaiUtils 4.1 boundaries and fixes the
abandoned-instance path-registration regression.

- `FileSystemWatcher` callbacks capture a weak `Pit` owner rather than retaining
  the instance through native watcher event handlers.
- Debounce work also reacquires weak ownership only when needed and does not keep
  an abandoned instance alive across its delay.
- Forced collection can therefore remove the weak registry target and make the
  canonical path reopenable.
- The finalizer remains deliberately free of watcher disposal, recovery
  publication, and filesystem I/O.
- The real OneDrive/SSH synchronization regression now waits for authoritative
  `Master.flag` contents to arrive on Mzansi, not merely a placeholder pathname.

Focused finalizer verification passed. The complete JsonPit Release suite is a
required release gate.
