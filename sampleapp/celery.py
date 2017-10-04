from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sampleapp.settings')

app = Celery('sampleapp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from celery.schedules import crontab
app.conf.beat_schedule = {
    'task_users': {
        'task': 'uploader.tasks.sync_users',
        'schedule': crontab(minute='*/10')
    },
    'task_candidates': {
        'task': 'uploader.tasks.sync_candidates',
        'schedule': crontab(minute='*/15')
    }
}
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))