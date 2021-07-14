from ___future__ import absolute_import, unicode_literals
import os
from celery import celery

os.eviron.setdefault('DJANGO_SETTINGS_MODULE', 'python_tips.settings')

app = Celery('python_tips')

app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_task()