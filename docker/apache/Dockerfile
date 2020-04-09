FROM httpd:2.4-alpine

COPY httpd.conf.extra /tmp/httpd.conf.extra

RUN cat /tmp/httpd.conf.extra >> /usr/local/apache2/conf/httpd.conf
