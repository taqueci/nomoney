#!/bin/sh

ADMIN_USER=admin
ADMIN_MAIL=admin@example.com
ADMIN_PASSWD=password

python3 manage.py compilemessages
python3 manage.py migrate
python3 manage.py collectstatic --no-input --clear

# Create super user
cat <<EOF | python3 manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='$ADMIN_USER').exists():
    User.objects.create_superuser('$ADMIN_USER', '$ADMIN_MAIL', '$ADMIN_PASSWD')
EOF
