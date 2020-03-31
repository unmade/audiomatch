FROM python:3.8-alpine

RUN apk update \
    && apk add --no-cache ffmpeg ffmpeg-libs \
    && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
    && apk add --no-cache chromaprint-dev

CMD ["/bin/sh"]
