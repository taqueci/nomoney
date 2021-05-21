FROM alpine:3.12.0

RUN apk add --no-cache apache2 apache2-http2 apache2-proxy

ARG N_URL_PREFIX="/n"
ARG N_STATIC_URL="/n/static/"
ARG N_MEDIA_URL="/n/media/"
ARG N_URL_APP="http://localhost:49152/n/"

COPY n.conf.in /tmp/n.conf.in

RUN sed \
    -e "s!@N_URL_PREFIX@!$N_URL_PREFIX!g" \
    -e "s!@N_STATIC_URL@!$N_STATIC_URL!g" \
    -e "s!@N_MEDIA_URL@!$N_MEDIA_URL!g" \
    -e "s!@N_URL_APP@!$N_URL_APP!g" \
    /tmp/n.conf.in > /etc/apache2/conf.d/n.conf

EXPOSE 80

CMD ["httpd", "-DFOREGROUND"]
