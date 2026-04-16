# Deploy and rollback project using Docker Compose with git tag-based versioning.

This example shows how to deploy a project to production using Docker Compose with git tag-based versioning. It also includes a rollback task that allows you to rollback to a previous version in case of issues.

* This example assumes we are gonna deploy from our machine that have ssh access to the production server.
* The production server is running Docker and Docker Compose.
* The project is NOT gonna use a registry. Meaning that the docker image will be built on the server during deployment, and the version tag will be based on the git commit hash of the code being deployed.


Run `task deploy` to execute the deployment task.

Task definitions in: [Taskfile.yml](./Taskfile.yml)

It will build and tag in the production server using the short git commit hash as version tag.

Run `task rollback:VERSION` to execute the rollback task, where VERSION is the short git commit hash to rollback to.