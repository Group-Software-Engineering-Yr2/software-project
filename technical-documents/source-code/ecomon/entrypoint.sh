#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn ecomon.wsgi:application --bind 0.0.0.0:9765