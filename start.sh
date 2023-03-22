#!/bin/sh

python manage.py runserver 0.0.0.0:8000

# python manage.py makemigrate --settings=core.settings.production
# python manage.py collectstatic --noinput --settings=core.settings.production
# gunicorn core.wsgi:application --bind 0.0.0.0:8000