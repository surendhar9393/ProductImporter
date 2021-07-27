#!/bin/sh
python /app/manage.py collectstatic --noinput
# Set the number of workers = 2n + 1 (n is number of CPU cores)
/usr/local/bin/gunicorn config.wsgi -t 60 -w 17 -b 0.0.0.0:5000 --chdir=/app --max-requests 1000 --max-requests-jitter 500
