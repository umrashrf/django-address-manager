from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.conf import settings

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'address_manager.settings')

app = Celery('address_manager')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)
