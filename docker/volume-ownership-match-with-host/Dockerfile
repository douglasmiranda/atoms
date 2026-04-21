FROM alpine:latest

# Match the UID and GID of the non-root user in the container with
# the host user to ensure proper permissions on mounted volumes
# You can pass the UID and GID as build arguments, or set default values in the Dockerfile
# Example: docker build --build-arg UID=1001 --build-arg GID=1001 -t myapp .
ARG UID=1000
ARG GID=1000
# NOTE: You could create an actual user and group here, but for simplicity we'll just use the numeric IDs

# First you create the directory that will be used as a volume and set permissions
RUN mkdir -p /data && chown ${UID}:${GID} /data

# Then you switch to the non-root user
USER ${UID}:${GID}

VOLUME [ "/data" ]

# The container will just sleep indefinitely, allowing you to exec into it and check permissions
CMD ["sleep", "infinity"]

# Now enter the container and check the permissions of the /data directory
# You should see that it is owned by the non-root user (1001) and group (1001)
# Try to create a file in the /data directory to confirm that the permissions are set correctly

# docker compose up -d
# docker compose exec app ls -lah /data
# docker compose exec app touch /data/testfile
# docker compose exec app ls -lah /data/testfile