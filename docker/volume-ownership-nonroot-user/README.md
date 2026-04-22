# Docker volume permissions for a non-root user

This snippet shows how to make a Docker volume writable by a non-root container user.

This is how I prefer most of the time. There are other ways to deal with.

The necessecity of this approach is that when you mount a volume, it is owned by `root:root` by default. (unless you running rootless docker)

The idea is simple:

1. Create the mount point in the image.
2. Set ownership to the numeric UID:GID that the container will run as.
3. Switch to that non-root user.
4. Mount a volume at that same path.

On first run, Docker initializes the empty volume with the directory metadata from the image path, preserving ownership.

## Files

- `Dockerfile`: creates `/data`, sets ownership to `1001:1001`, and runs as that user.
- `compose.yml`: starts one service and mounts a named volume at `/data`.

## Run

From this folder:

```bash
docker compose up -d --build
```

## Verify permissions

```bash
docker compose exec app ls -lah /data
docker compose exec app touch /data/testfile
docker compose exec app ls -lah /data/testfile
```

You should see files owned by UID `1001` and GID `1001`.

## Related snippets

- Match container UID/GID with host for bind mounts: [docker/volume-ownership-match-with-host](../volume-ownership-match-with-host/README.md)
- Runtime ownership fix with `gosu`: [docker/volume-ownership-nonroot-user-gosu](../volume-ownership-nonroot-user-gosu/README.md)
- Bind mount with ACLs for different host/container UIDs: [docker/volume-ownership-fix-with-setfacl](../volume-ownership-fix-with-setfacl/README.md)
- One-shot side container to initialize volume permissions: [docker/volume-permissions-fix-with-one-shot-side-container](../volume-permissions-fix-with-one-shot-side-container/README.md)
