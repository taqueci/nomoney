FROM alpine:3

RUN apk add --no-cache apache2 apache2-http2 apache2-proxy

COPY config/* /etc/apache2/conf.d/

EXPOSE 80

ENTRYPOINT ["httpd", "-DFOREGROUND"]
