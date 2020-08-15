#!/bin/sh

if type python3 > /dev/null 2>&1; then
    alias python=python3
    alias pip=pip3
fi

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear

# Create super user
cat <<EOF | python manage.py shell
from django.contrib.auth import get_user_model

ADMIN_USER = 'admin'
ADMIN_MAIL = 'admin@example.com'
ADMIN_PASSWORD = 'password'

User = get_user_model()

if not User.objects.filter(username=ADMIN_USER).exists():
    User.objects.create_superuser(ADMIN_USER, ADMIN_MAIL, ADMIN_PASSWORD)
EOF

python manage.py compilemessages

exec uwsgi \
    --http-socket :49152 \
    --wsgi-file config/wsgi.py \
    --logto logs/uwsgi.log \
    --touch-chain-reload uwsgi-reload \
    --master \
    --processes 4 --threads 1 --thunder-lock \
    --max-requests 6000
