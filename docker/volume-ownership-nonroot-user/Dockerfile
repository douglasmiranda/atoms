FROM alpine:latest

# NOTE: You could create an actual user and group here, but for simplicity we'll just use the numeric IDs

# First you create the directory that will be used as a volume and set permissions
RUN mkdir -p /data && chown 1001:1001 /data

# Then you switch to the non-root user
USER 1001:1001

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