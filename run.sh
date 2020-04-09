#!/bin/sh

pip install -r requirements.txt

test -f config/local_settings.py ||
    cp config/local_settings.py.tmpl config/local_settings.py

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear

# Create super user
cat <<EOF | python manage.py shell
from django.contrib.auth import get_user_model
from config.settings import ADMIN_USER, ADMIN_MAIL, ADMIN_PASSWORD

User = get_user_model()

if not User.objects.filter(username=ADMIN_USER).exists():
    User.objects.create_superuser(ADMIN_USER, ADMIN_MAIL, ADMIN_PASSWORD)
EOF

django-admin compilemessages

test -d logs || mkdir logs

exec uwsgi \
    --http-socket :49152 \
    --wsgi-file config/wsgi.py \
    --logto logs/uwsgi.log \
    --touch-chain-reload uwsgi-reload \
    --master \
    --processes 4 --threads 1 --thunder-lock \
    --max-requests 6000
