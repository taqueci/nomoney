#!/bin/sh

exec uwsgi \
    --http-socket :49152 \
    --wsgi-file config/wsgi.py \
    --touch-chain-reload uwsgi-reload \
    --master \
    --processes 4 --threads 1 --thunder-lock \
    --max-requests 6000
