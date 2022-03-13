#!/bin/sh

tmpl=/opt/apache2/config/app.conf.in
conf=/etc/apache2/conf.d/app.conf

sed \
    -e "s!@APP_PATH@!$APP_PATH!g" \
    -e "s!@APP_STATIC_PATH@!$APP_STATIC_PATH!g" \
    -e "s!@APP_MEDIA_PATH@!$APP_MEDIA_PATH!g" \
    -e "s!@APP_URL@!$APP_URL!g" \
    $tmpl > $conf

exec httpd -DFOREGROUND
