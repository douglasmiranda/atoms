FROM alpine:latest

# You can pass the UID and GID as build arguments, or set default values in the Dockerfile
# Example: docker build --build-arg UID=1002 --build-arg GID=1002 -t myapp .
ARG UID=1001
ARG GID=1001

# NOTE: You could create an actual user and group here, but for simplicity we'll just use the numeric IDs

# First you create the directory that will be used as a volume and set permissions
RUN mkdir -p /data && chown -R ${UID}:${GID} /data

# Then you switch to the non-root user
USER ${UID}:${GID}

VOLUME [ "/data" ]

# The container will just sleep indefinitely, allowing you to exec into it and check permissions
CMD ["sleep", "infinity"]
