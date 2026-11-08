# Deploy and rollback project using Docker Compose with git commit hash versioning.

This example shows how to deploy a project to production using Docker Compose, tagging images with the short git commit hash. It also includes a rollback task that starts the previously built image for an older commit.

* This example assumes we are gonna deploy from our machine that have ssh access to the production server.
* The production server is running Docker and Docker Compose.
* The project is NOT gonna use a registry. Meaning that the docker image will be built on the server during deployment, and the version tag will be based on the git commit hash of the code being deployed.


Run `task deploy` to execute the deployment task.

Task definitions in: [Taskfile.yml](./Taskfile.yml)

It will build and tag in the production server using the short git commit hash as the image tag.

Run `task rollback:VERSION` to execute the rollback task, where VERSION is the short git commit hash to rollback to. Rollback does not check out that commit; it starts the image that was built and tagged during that deploy. The image must still exist on the server.
