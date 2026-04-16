# Copy envfiles to production "safely"

This example shows how to copy envfiles to production through ssh using rsync. It will override the envfiles in production, but it will create a backup of the existing envfiles before copying the new ones.

- Select the envfiles from local envfiles/prod/*
- Ignore files you don't want to copy (*.env.template)
- Before overriding create a backup of the existing envfiles inside the same dir. (e.g., .backups/2024-06-30/15h30m00s/)

Since it uses rsync, you need to have rsync installed on your local machine and on the remote server.

Run `task copy-envfiles-to-prod` to execute the task.

Task definitions in: [Taskfile.yml](./Taskfile.yml)

## Local test target with Docker Compose

There's a `copy-envfiles-to-prod-custom` with less hardcoded values so we can try it using some custom vars, let's see:

You can run an OpenSSH server locally to test this task safely.

1. Start the test target:

```bash
docker compose -f compose.yml up --build
```

2. Run the task against localhost:

```bash
task copy-envfiles-to-prod \
  REMOTE_HOST=root@localhost \
  SSH_PORT=2222
```

3. Optional: inspect copied files inside the container:

```bash
docker compose exec sshd ls -la /username/project-name/envfiles/prod
```

For a simpler 'copy without backup', you could just use scp instead of rsync. 