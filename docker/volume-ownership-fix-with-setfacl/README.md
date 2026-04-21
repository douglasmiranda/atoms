# Docker bind mount ownership fix with setfacl

This snippet shows how to keep a bind-mounted directory writable from both sides when host and container use different UIDs.

Typical case:

- Host user is UID 1000.
- Container process runs as UID 1001.
- Both need read and write access to `./data` (host) and `/data` (container).

This snippet uses POSIX ACLs to grant both users access, including defaults for future files.

## Why this exists

For bind mounts (`./data:/data`), file ownership and permissions come from the host filesystem.

If host UID and container UID differ, plain `chown` or `chmod` is often not enough for true bidirectional access. ACLs allow granting permissions to multiple users at the same time.

## How it works

1. `Dockerfile` builds an image that runs as a non-root numeric user (`UID:GID`, default `1001:1001`).
2. `compose.yml` bind-mounts `./data` to `/data`.
3. `Makefile` target `fix-data-volume-permissions` applies ACLs so both host user and app user can read/write existing files and future files.

## Files in this snippet

- `Dockerfile`: defines container user and `/data` mount point.
- `compose.yml`: bind mount configuration and build args for UID/GID.
- `Makefile`: helper target that applies ACLs in a safe order.

## Requirements

- Docker and Docker Compose.
- Host filesystem with ACL support.
- `setfacl` available on host.

On Debian/Ubuntu:

```bash
sudo apt-get update && sudo apt-get install -y acl
```

On Fedora:

```bash
sudo dnf install -y acl
```

On Alpine:

```bash
sudo apk add acl
```

## Run

From this folder:

```bash
docker compose up -d --build
```

Then apply ACLs:

```bash
make fix-data-volume-permissions
```

Optional custom app UID/GID (if container user is not the default):

```bash
make fix-data-volume-permissions APP_UID=1001 APP_GID=1001
```

## Verify bidirectional behavior

Create from host, read/write from container:

```bash
touch data/from-host
docker compose exec app sh -lc 'echo container >> /data/from-host && ls -lah /data/from-host'
```

Create from container, read/write from host:

```bash
docker compose exec app sh -lc 'echo container > /data/from-container && ls -lah /data/from-container'
echo host >> data/from-container
ls -lah data/from-container
```

Check ACLs:

```bash
getfacl data
getfacl data/from-container
```

## About the touch behavior

You might observe:

```bash
touch data/a
# touch: setting times of 'data/a': Permission denied
```

while editing the same file from an editor still appears to work.

This can happen because:

- `touch` updates timestamps on the existing inode and needs write permission on that file (or ownership/capability).
- Many editors do not modify the same inode in place. They write a temporary file and rename it, which depends mostly on directory write/execute permissions.

That is why "save works" but `touch` may fail when file-level ACLs are missing or stale.

The `fix-data-volume-permissions` target applies ACLs recursively to existing files and sets default ACLs for future files to reduce this inconsistency.

If you still see this behavior, re-run:

```bash
make fix-data-volume-permissions
```

and inspect:

```bash
id -u
docker compose exec app id
ls -ln data/a
getfacl data data/a
```

## Notes and caveats

- A file can have only one owner UID, but ACL lets multiple users access it.
- If your goal is identical ownership on both sides, prefer matching host/container UID/GID directly.
- ACL support depends on filesystem and mount options.

## setfacl flags

Annotations for `setfacl` flags. Basically to remind myself when to use which:

`-m, --modify=acl`

Purpose: Add or update ACL entries on target objects.
Use when: You want to grant/change rights without replacing the whole ACL.
Example idea: add user 1001 rwx on a directory.

`-M, --modify-file=file`

Purpose: Same as `-m`, but read many entries from a file.
Use when: Applying a prepared ACL snippet repeatedly.

`-x, --remove=acl`

Purpose: Remove specific ACL entries.
Use when: Revoking one user/group entry but leaving others.

`-X, --remove-file=file`

Purpose: Remove entries listed in a file.
Use when: Bulk cleanup of selected ACL entries.

`-b, --remove-all`

Purpose: Remove all extended ACL entries (named users/groups and mask), keeping base owner/group/other.
Use when: Resetting object ACLs to simple mode quickly.

`-k, --remove-default`

Purpose: Remove default ACL from a directory.
Use when: Stop inheritance behavior for newly created children.

`--set=acl`

Purpose: Replace the entire ACL with exactly what you provide.
Use when: You want a strict, known ACL state.
Caution: Destructive to existing extended entries.

`--set-file=file`

Purpose: Same as `--set`, but ACL definition comes from file.
Use when: Reproducible ACL deployments from saved templates.

`--mask`

Purpose: Recalculate/update mask entry from ACL contents.
Use when: You want effective rights recomputed explicitly.
Note: Mask limits effective permissions of named users/groups (and group class).

`-n, --no-mask`

Purpose: Do not recalculate mask.
Use when: You intentionally manage mask yourself and do not want `setfacl` to adjust it.

`-d, --default`

Purpose: Apply operation to default ACL (directory inheritance ACL), not normal access ACL.
Use when: You need future files/subdirs to inherit ACL entries.
Important: Only meaningful on directories.

`-R, --recursive`

Purpose: Apply operation recursively through directory tree.
Use when: You need to update many existing files/subdirs at once.
Note: Recursive affects existing objects; default ACL still governs future ones.

`-L, --logical`

Purpose: During recursive walk, follow symlinked directories.
Use when: You want traversal to include targets behind symlinks.

`-P, --physical`

Purpose: During recursive walk, do not follow symlinks (operate on links as links).
Use when: You want safer, non-following behavior.

`--restore=file`

Purpose: Restore ACLs from a backup file produced by `getfacl -R`.
Use when: Recovering ACL state after migrations/incidents.


## Related snippets

- Match container UID/GID with host for simpler ownership: [docker/volume-ownership-match-with-host](../volume-ownership-match-with-host/README.md)
- Fixed non-root user with named volume: [docker/volume-ownership-nonroot-user](../volume-ownership-nonroot-user/README.md)
- Runtime ownership fix with `gosu`: [docker/volume-ownership-nonroot-user-gosu](../volume-ownership-nonroot-user-gosu/README.md)
