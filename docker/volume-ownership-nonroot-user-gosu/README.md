# Docker volume ownership for a non-root user with gosu

This snippet shows the same idea as the non-root example, but it uses `gosu` in an entrypoint.

Instead of baking one static UID:GID at image build time, this version:

1. Starts as root in the container entrypoint.
2. Ensures `/data` exists and adjusts ownership to `APP_UID:APP_GID`.
3. Drops privileges with `gosu` and runs the final command as non-root.

## Files

- `Dockerfile`: installs `gosu` and sets the entrypoint.
- `entrypoint.sh`: fixes volume ownership and then executes the command as `APP_UID:APP_GID`.
- `compose.yml`: starts one service and mounts a named volume at `/data`.

## Run

From this folder:

```bash
docker compose up -d --build
```

Optional custom IDs:

```bash
APP_UID=$(id -u) APP_GID=$(id -g) docker compose up -d --build
```

## Verify

```bash
docker compose exec app id
docker compose exec app ls -lah /data
docker compose exec app touch /data/testfile
docker compose exec app ls -lah /data/testfile
```

## When gosu is useful

Using `gosu` in an entrypoint is useful when:

- You need root only for startup tasks (for example, `chown` on mounted volumes), but the app must run as non-root.
- UID/GID must be decided at runtime (different hosts, CI runners, or developer machines).
- You run a single image across environments where ownership requirements differ.
- You need a cleaner privilege drop than `su`, without spawning an extra shell process.

## Related snippets

- Fixed non-root user with named volume: [docker/volume-ownership-nonroot-user](../volume-ownership-nonroot-user/README.md)
- Match container UID/GID with host for bind mounts: [docker/volume-ownership-match-with-host](../volume-ownership-match-with-host/README.md)
- Bind mount with ACLs for different host/container UIDs: [docker/volume-ownership-fix-with-setfacl](../volume-ownership-fix-with-setfacl/README.md)
