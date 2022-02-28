import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'probe_fab.settings')

app = Celery('probe_fab.tasks.send')

app.config_from_object(settings, namespace='CELERY')

app.conf.timezone = 'Europe/Moscow'

app.autodiscover_tasks()
