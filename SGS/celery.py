
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from datetime import timedelta
# from base.tasks import escalate_complaint
from celery.schedules import crontab



# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SGS.settings')

app = Celery('SGS')
app.conf.enable_utc = False 
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.beat_schedule = {
    'check-complaint-escalation': {
        'task': 'base.tasks.escalate_complaint',
        'schedule': timedelta(minutes=2),  # Run the task every 15 minutes
    },
}

# app.conf.beat_schedule = {
#     'check-complaint-escalation': {
#         'task': 'base.tasks.escalate_complaint',
#         'schedule': crontab(minute='*/2'),  # Run every 2 minutes
#     },
# }

# app.conf.beat_schedule = {
#     'run-every-hour': {
#         'task': 'base.tasks.check_complaint_status',
#         'schedule': crontab(minute=0, hour='*/1'),  # check every hour
#     },
# }
# app.conf.timezone = 'UTC'



# app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

# Celery beat Settings 
# Load task modules from all registered Django app configs

