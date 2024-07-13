# jobfeed_project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobfeed_project.settings')

app = Celery('jobfeed_project')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from celery.schedules import crontab

app.conf.beat_schedule = {
    'periodic-scraping-task': {
        'task': 'jobfeed.tasks.periodic_scraping',
        'schedule': crontab(minute=0, hour='*/1'),  # Run every hour
    },
    'generate-xml-task': {
        'task': 'jobfeed.tasks.generate_xml',
        'schedule': crontab(minute=30, hour='*/1'),  # Generate XML every half hour
    },
}

if __name__ == '__main__':
    app.start()
