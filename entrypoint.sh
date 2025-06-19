#!/bin/bash
# shellcheck shell=bash
# for test
tail -f /dev/null

umask ${UMASK}

groupmod -o -g "${PGID}" wol
usermod -o -u "${PUID}" wol

chown wol:wol -R /app /home/wol
. /home/wol/venv/bin/activate
exec su-exec "${PUID}:${PGID}" python3 main.py