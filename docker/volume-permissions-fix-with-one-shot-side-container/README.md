# Docker volume permissions fix with a one-shot side container

This snippet shows a sidecar-style initialization service that fixes ownership and permissions on a named Docker volume before the app starts.

Instead of doing permission fixes in the app container entrypoint, a dedicated one-shot service does the setup and exits successfully. The app service waits for that completion.

## How it works

1. `data_volume_init` mounts the same named volume as the app.
2. It runs as root and executes `chown` + `chmod` on the volume path.
3. It exits with success (`restart: "no"`).
4. `app` runs as non-root (`APP_UID`) and starts only after init completed successfully (`depends_on.condition: service_completed_successfully`).

## Files

- `compose.yml`: defines both the one-shot initializer service and the app service sharing the same named volume.

## Run

From this folder:

```bash
docker compose up -d
```

Optional custom UID:

```bash
APP_UID=$(id -u) docker compose up -d
```

## Verify

```bash
docker compose exec app id
docker compose exec app ls -lah /data_volume
docker compose exec app touch /data_volume/testfile
docker compose exec app ls -lah /data_volume/testfile
```

## When this pattern is useful

- You want startup permission fixes, but do not want root logic in the app container.
- You want a clear separation between initialization tasks and app runtime.
- You want to keep the app container running as non-root only.

## Related snippets

- Match container UID/GID with host for bind mounts: [docker/volume-ownership-match-with-host](../volume-ownership-match-with-host/README.md)
- Fixed non-root user with named volume: [docker/volume-ownership-nonroot-user](../volume-ownership-nonroot-user/README.md)
- Runtime ownership fix with `gosu`: [docker/volume-ownership-nonroot-user-gosu](../volume-ownership-nonroot-user-gosu/README.md)
- Bind mount with ACLs for different host/container UIDs: [docker/volume-ownership-fix-with-setfacl](../volume-ownership-fix-with-setfacl/README.md)
