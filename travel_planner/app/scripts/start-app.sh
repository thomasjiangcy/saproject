#!/bin/bash
python3 /app/scripts/wait_for_db.py
python3 /app/manage.py makemigrations
python3 /app/manage.py migrate

python3 /app/manage.py collectstatic --noinput

gunicorn -w 4 -b 0.0.0.0:8000 --reload app.wsgi:application --timeout 90