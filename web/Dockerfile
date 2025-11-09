FROM alpine:3

RUN apk add --no-cache apache2 apache2-http2 apache2-proxy

RUN sed -ri \
  -e 's!^(\s*CustomLog)\s+\S+!\1 /proc/self/fd/1!g' \
  -e 's!^(\s*ErrorLog)\s+\S+!\1 /proc/self/fd/2!g' \
  -e 's!^(\s*TransferLog)\s+\S+!\1 /proc/self/fd/1!g' \
  /etc/apache2/httpd.conf

COPY config/* /etc/apache2/conf.d/

# https://httpd.apache.org/docs/2.4/stopping.html#gracefulstop
STOPSIGNAL SIGWINCH

EXPOSE 80

ENTRYPOINT ["httpd", "-DFOREGROUND"]
