#!/usr/bin/env bash


if [ ! -f locale/en/LC_MESSAGES/django.po ]; then
  python3 manage.py makemessages --ignore="static-site" --ignore=".env" -l en -v 3
  python3 manage.py makemessages --ignore="static-site" --ignore=".env" -l en -d djangojs -v 3
fi

if [ ! -f locale/cn/LC_MESSAGES/django.po ]; then
  python3 manage.py makemessages --ignore="static-site" --ignore=".env" -l cn -v 3
  python3 manage.py makemessages --ignore="static-site" --ignore=".env" -l cn -d djangojs -v 3
fi

python3 manage.py makemessages --ignore="static-site" --ignore=".env" -a -d djangojs -v 3
python3 manage.py makemessages --ignore="static-site" --ignore=".env" -a -v 3

python3 manage.py compilemessages -v 3