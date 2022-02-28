import os

import django


def setup():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'probe_fab.settings')
    django.setup()
