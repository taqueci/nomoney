FROM python:3.12-alpine

ARG INSTALL_DIR=/opt/nomoney

WORKDIR $INSTALL_DIR

COPY requirements.txt .

RUN apk add --no-cache gettext postgresql-libs libjpeg && \
    apk add --no-cache --virtual .build-deps gcc \
        linux-headers musl-dev postgresql-dev jpeg-dev zlib-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del --no-cache --purge .build-deps

COPY . .

RUN django-admin compilemessages

EXPOSE 49152

CMD ["sh", "run.sh"]
