FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV N_STATIC_ROOT=/var/opt/nomoney/staticfiles
ENV N_MEDIA_ROOT=/var/opt/nomoney/media

ARG INSTALL_DIR=/opt/nomoney

WORKDIR $INSTALL_DIR

COPY requirements.txt requirements-prod.txt .

RUN apk add --no-cache gettext postgresql-libs && \
    apk add --no-cache --virtual .build-deps \
        gcc linux-headers musl-dev && \
    pip install --no-cache-dir -r requirements-prod.txt && \
    apk del --no-cache --purge .build-deps

COPY . .

RUN django-admin compilemessages

EXPOSE 49152

CMD ["sh", "run.sh"]
