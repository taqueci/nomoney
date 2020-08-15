FROM alpine:3.12.0

RUN apk add --no-cache apache2 apache2-http2 apache2-proxy

COPY peta.conf /etc/apache2/conf.d/peta.conf

EXPOSE 80 8080

CMD ["httpd", "-DFOREGROUND"]
