#!/bin/sh
set -eu

APP_UID="${APP_UID:-1001}"
APP_GID="${APP_GID:-1001}"

mkdir -p /data
chown -R "${APP_UID}:${APP_GID}" /data

exec gosu "${APP_UID}:${APP_GID}" "$@"
