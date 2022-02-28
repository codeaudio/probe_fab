import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'probe_fab.settings')

app = Celery('probe_fab.tasks.send')

app.conf.timezone = 'Europe/Moscow'

app.autodiscover_tasks()
