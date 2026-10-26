# Google Drive and OneDrive on Windows 11 with WSL2

This guide exposes Windows cloud-storage folders to Ubuntu in WSL2, then uses
Amafu to configure RAIkeep. Windows runs the cloud clients; WSL accesses their
files through mounted paths. Amafu discovers directories and writes configuration;
it does not mount Windows drives, download placeholders, or operate a sync client.

The commands below describe a setup to verify on your Windows machine. They have
not been exercised on Windows as part of this documentation review.

## Prepare the Windows folders

For Google Drive, this example uses a streaming drive assigned to `G:` with a
`My Drive\GDriveData` folder. Check the actual drive letter in Drive for desktop
settings and File Explorer. Streaming requires Drive for desktop to be running;
mirroring keeps a local copy instead. See Google's
[streaming and mirroring documentation](https://support.google.com/drive/answer/13401938?hl=en).

For OneDrive, locate the intended account's folder in File Explorer and create or
locate its `OneDriveData` directory. Select **Always keep on this device** for data
that must be available locally, then let downloading finish. See Microsoft's
[Files On-Demand documentation](https://support.microsoft.com/en-us/onedrive/save-disk-space-with-onedrive-files-on-demand-for-windows).

| Provider | Example Windows location | WSL location | Stable Linux path |
| --- | --- | --- | --- |
| Google Drive | `G:\My Drive\GDriveData` | `/mnt/g/My Drive/GDriveData` | `/srv/ServerData/GDriveData` |
| OneDrive | `C:\Users\ExampleUser\OneDrive\OneDriveData` | `/mnt/c/Users/ExampleUser/OneDrive/OneDriveData` | `/srv/ServerData/OneDriveData` |

Replace `ExampleUser` and any account-specific folder names with the actual paths.
Windows placeholders and virtual drives may behave differently through WSL than
through File Explorer. A drive-letter mount is an option to test, not a guarantee
that an `Input/output error` will disappear.

## Mount the Google Drive volume in WSL

Run these commands inside Ubuntu after the Windows drive is available. If `/mnt/g`
is already mounted correctly, use that mount instead of mounting it again.

```sh
sudo mkdir -p /mnt/g
sudo mount -t drvfs G: /mnt/g -o "metadata,uid=$(id -u),gid=$(id -g),umask=022"
ls -la "/mnt/g/My Drive/GDriveData"
```

DrvFs exposes Windows files to WSL. Its `metadata`, `uid`, `gid`, and mask options
control Linux permission handling; Windows permissions still apply. See
[Microsoft's WSL configuration reference](https://learn.microsoft.com/en-us/windows/wsl/wsl-config).

Verify that you can read an existing file's contents, rather than relying only on
a directory listing. If that fails, check the same file in Windows and its local
availability before configuring RAIkeep.

For mounting at WSL startup, print an `/etc/fstab` entry using your actual Linux
user and group IDs:

```sh
printf 'G: /mnt/g drvfs metadata,uid=%s,gid=%s,umask=022 0 0\n' "$(id -u)" "$(id -g)"
sudoedit /etc/fstab
```

Add the printed line once. WSL processes this file at startup when
`[automount] mountFsTab=true` in `/etc/wsl.conf` (the default). The Windows virtual
drive may become available later; if mounting at startup fails, start Drive for
desktop on Windows and then run `sudo mount /mnt/g` inside WSL.

## Create stable Linux paths

After both source directories are accessible, create their links. These commands
assume the two destination links do not already exist; inspect an existing entry
before changing it.

```sh
sudo mkdir -p /srv/ServerData
sudo ln -sT "/mnt/g/My Drive/GDriveData" /srv/ServerData/GDriveData
sudo ln -sT "/mnt/c/Users/ExampleUser/OneDrive/OneDriveData" /srv/ServerData/OneDriveData
ls -la /srv/ServerData/GDriveData/
ls -la /srv/ServerData/OneDriveData/
```

The links provide stable application paths while files remain in their Windows
cloud folders. They do not initiate synchronization.

## Detect and configure with Amafu

Preview discovery and the proposed configuration:

```sh
amafu detect --json --dry-run
amafu init --create-links --dry-run
```

On Linux, Amafu checks existing `~/.CloudStorage/` shortcuts first, then accessible
paths in an existing `~/.config/RAIkeep.json5`, then conventional directories under
`/srv/ServerData/`. With no earlier overrides, the setup above should discover
`GoogleDrive` and `OneDrive` at the corresponding `*Data` paths. Other configured
or detected providers may also appear.

For a new configuration, run:

```sh
amafu init --create-links
```

This creates `~/.CloudStorage/GoogleDrive` and `~/.CloudStorage/OneDrive` shortcuts
where needed and uses those clean paths in `~/.config/RAIkeep.json5`.

If a configuration already exists, `init` refuses to overwrite it. Use the
reconciliation preview instead, review its changes, then apply them explicitly:

```sh
amafu reconcile
amafu reconcile --apply
```

Discovery establishes that directories exist. It does not certify that files are
downloaded or that changes have reached another machine. Verify synchronization
separately with a small test file before relying on the setup for shared Pits.

## Troubleshooting

- **Empty or unavailable mount:** check that the correct Windows account and
  drive are available, then retry the mount. An ordinary empty mount-point
  directory is not proof that its drive is mounted.
- **Input/output error:** try reading the file in Windows, ensure it is available
  locally, and retry in WSL. The error alone does not identify a particular cloud
  driver or prove that remounting will fix it.
- **Permission denied:** check Windows access rights and the mount's Linux user
  and group IDs. Do not assume every Ubuntu user has ID `1000`.
- **Paths containing spaces:** quote them as shown above. Stable symlinks simplify
  application configuration but do not change the target filesystem's behavior.
