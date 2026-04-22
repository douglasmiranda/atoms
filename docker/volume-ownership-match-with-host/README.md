# Docker volume ownership matching with host UID/GID

This snippet shows how to run a container as a non-root user whose UID and GID match the host user.

This is useful when using bind mounts (for example `./data:/data`) and you want files created in the container to be owned by your host user.

## How it works

1. `ARG UID` and `ARG GID` allow passing host IDs at build time.
2. `/data` is created and owned by `${UID}:${GID}`.
3. The container runs as `USER ${UID}:${GID}`.
4. `compose.yml` bind-mounts `./data` to `/data`.

## Files

- `Dockerfile`: receives `UID`/`GID`, sets `/data` ownership, and switches to that user.
- `compose.yml`: passes `UID`/`GID` build args and bind-mounts `./data:/data`.

## Run

From this folder:

```bash
UID=$(id -u) GID=$(id -g) docker compose up -d --build
```

## Verify

```bash
docker compose exec app sh -lc 'id && ls -lah /data'
docker compose exec app sh -lc 'touch /data/testfile && ls -lah /data/testfile'
ls -lah ./data/testfile
```

The file owner on the host and in the container should match your UID/GID.

## Related snippets

- Fixed non-root user with named volume: [docker/volume-ownership-nonroot-user](../volume-ownership-nonroot-user/README.md)
- Runtime ownership fix with `gosu`: [docker/volume-ownership-nonroot-user-gosu](../volume-ownership-nonroot-user-gosu/README.md)
- Bind mount with ACLs for different host/container UIDs: [docker/volume-ownership-fix-with-setfacl](../volume-ownership-fix-with-setfacl/README.md)
- One-shot side container to initialize volume permissions: [docker/volume-permissions-fix-with-one-shot-side-container](../volume-permissions-fix-with-one-shot-side-container/README.md)
