FROM alpine:3

RUN apk add --no-cache apache2 apache2-http2 apache2-proxy

COPY . /opt/apache2

EXPOSE 80

CMD ["sh", "/opt/apache2/run.sh"]
