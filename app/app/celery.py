from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
logger = logging.getLogger("Celery")
app = Celery('app')
app.conf.broker_url = 'redis://localhost:6379/0'
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


