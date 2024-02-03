from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zelf_challenge_rest_api.settings")

app = Celery("zelf_challenge_rest_api")


app.conf.beat_schedule = {
    "fetch-and-store-data-every-minute": {
        "task": "api.tasks.celery_fetch_and_store_data",
        "schedule": crontab(minute="*/1"),  # Run every 1 minutes
    },
}

# Include tasks from other files
app.autodiscover_tasks()

# Load task modules from all registered Django app configs.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps.
app.autodiscover_tasks()
