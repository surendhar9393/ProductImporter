#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

su -m celeryuser -c "celery -A ProductImporter worker -Q high -l INFO -n high_worker --concurrency=5 --pidfile="
