FROM python:3.8-alpine

RUN apk update \
    && apk add --no-cache ffmpeg ffmpeg-libs \
    && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
    && apk add --no-cache chromaprint-dev

ARG package_version
ENV PACKAGE_VERSION=$package_version

RUN pip3 install "audiomatch==${PACKAGE_VERSION}"

ENTRYPOINT ["audiomatch"]
