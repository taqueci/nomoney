FROM python:3.9-alpine

ENV INSTALL_DIR /opt/nomoney

WORKDIR $INSTALL_DIR

COPY requirements.txt .

RUN apk add --no-cache gettext postgresql-libs libjpeg && \
    apk add --no-cache --virtual .build-deps gcc \
        linux-headers musl-dev postgresql-dev jpeg-dev zlib-dev && \
    pip install --no-cache-dir -r requirements.txt \
        uwsgi==2.0.20 && \
    apk del --no-cache --purge .build-deps

COPY . $INSTALL_DIR

RUN django-admin compilemessages

EXPOSE 49152

CMD ["sh", "run.sh"]
