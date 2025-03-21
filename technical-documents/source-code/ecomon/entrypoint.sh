#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py crontab add
python manage.py crontab add

gunicorn ecomon.wsgi:application --bind 0.0.0.0:9765