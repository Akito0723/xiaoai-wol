FROM alpine:3.21

ARG VERSION

ENV LANG="C.UTF-8" \
    TZ=Asia/Shanghai \
    PUID=1000 \
    PGID=1000 \
    UMASK=022

WORKDIR /app

COPY ./backend/src/requirements.txt .
RUN set -ex && \
    apk add --no-cache \
        bash \
        busybox-suid \
        python3 \
        py3-pip \
        su-exec \
        shadow \
        tini \
        openssl \
        tzdata && \
    python3 -m venv /home/wol/venv && \
    . /home/wol/venv/bin/activate && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    # Add user
    mkdir -p /home/wol && \
    addgroup -S wol -g 911 && \
    adduser -S wol -G wol -h /home/wol -s /sbin/nologin -u 911 && \
    # Clear
    rm -rf \
        /root/.cache \
        /tmp/*

COPY --chmod=755 ./backend/src/. .
COPY --chmod=755 ./entrypoint.sh /entrypoint.sh

RUN if [ -n "$VERSION" ]; then echo "VERSION='$VERSION'" > /app/module/__version__.py; fi

ENTRYPOINT ["tini", "-g", "--", "/entrypoint.sh"]

EXPOSE 5835
VOLUME ["/app/data" ]
