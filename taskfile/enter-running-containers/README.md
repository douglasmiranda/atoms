# Enter Running Containers

Examples of tasks that enter running containers using `docker compose exec`.

Run the sample containers with:

```bash
docker compose up -d
```

Task definitions in: [Taskfile.yaml](./Taskfile.yaml)

`enter-simple-1` - Enter the `postgres` container and run `psql` command.

```
task enter-simple-1 -- postgres psql -U postgres
task: [enter-simple-1] docker compose exec postgres psql -U postgres
psql (18.3 (Debian 18.3-1.pgdg13+1))
Type "help" for help.

postgres=# WE ARE INSIDE THE PSQL SHELL OF THE POSTGRES CONTAINER!
```

`enter-with-cmd` - Enter a container and run a command selected from a list. The task will prompt you to select a service and a command to run.

```
task enter-with-cmd
? Select value for SERVICE:
  app
  postgres
❯ postgres2
  (↑/↓ to move, enter to select, esc to cancel)

? Select value for CMD:
  sh
  bash
❯ psql -U postgres
  (↑/↓ to move, enter to select, esc to cancel)

psql (18.3)
Type "help" for help.

postgres=# WE ARE INSIDE THE PSQL SHELL OF THE POSTGRES2 CONTAINER!
```



`enter-with-default-cmd` - Enter the `app` container and run `sh` command by default. The task will prompt you to select a service, and if you select `postgres2`, it will run `psql` command instead.

```
task enter-with-default-cmd
? Select value for SERVICE:
❯ app
  postgres
  postgres2
  (↑/↓ to move, enter to select, esc to cancel)


task: [enter-with-default-cmd] docker compose exec app sh
/ # WE ARE INSIDE THE APP CONTAINER!
```


```
task enter-with-default-cmd
? Select value for SERVICE:
  app
  postgres
❯ postgres2
  (↑/↓ to move, enter to select, esc to cancel)


task: [enter-with-default-cmd] docker compose exec postgres2 psql -U postgres
psql (18.3)
Type "help" for help.

postgres=# WE ARE INSIDE THE PSQL SHELL OF THE POSTGRES2 CONTAINER!
```