FROM python:3.8-alpine

ENV INSTALL_DIR /opt/nomoney

WORKDIR $INSTALL_DIR

COPY requirements.txt .

RUN apk add --no-cache gettext postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc \
        linux-headers musl-dev postgresql-dev && \
    pip install --no-cache-dir uwsgi psycopg2 -r requirements.txt && \
    apk del --no-cache --purge .build-deps

COPY . $INSTALL_DIR

RUN django-admin compilemessages

EXPOSE 49152

CMD ["sh", "run.sh"]
