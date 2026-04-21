FROM alpine:latest

ARG APP_UID=1001
ARG APP_GID=1001

RUN apk add --no-cache gosu ca-certificates

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENV APP_UID=${APP_UID}
ENV APP_GID=${APP_GID}

VOLUME [ "/data" ]

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["sleep", "infinity"]
