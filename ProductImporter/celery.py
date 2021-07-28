from __future__ import absolute_import, unicode_literals
import os
import environ

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

# celery_app = Celery('blowhorn')

RABBIT_HOSTNAME = os.environ.get('RABBIT_PORT_5672_TCP', 'rabbit')
if RABBIT_HOSTNAME.startswith('tcp://'):
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]


broker_url = os.environ.get('CELERY_BROKER_URL', '')
if not broker_url:
    broker_url = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
        user=os.environ.get('RABBIT_ENV_USER', 'guest'),
        password=os.environ.get('RABBIT_ENV_RABBITMQ_PASS', 'guest'),
        hostname=RABBIT_HOSTNAME,
        vhost=os.environ.get('RABBIT_ENV_VHOST', ''))


celery_app = Celery('ProductImporter', broker=broker_url,
             include=['ProductImporter.product.tasks'])

celery_app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
env = environ.Env()
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    settingsModule = 'config.settings.production'
else:
    settingsModule = 'config.settings.local'

celery_app.config_from_object(settingsModule, namespace='CELERY')
celery_app.conf.broker_transport_options = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,

}



# Load task modules from all registered Django app configs.
#app.autodiscover_tasks()
celery_app.autodiscover_tasks(settings.INSTALLED_APPS)

@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
