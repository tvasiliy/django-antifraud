import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_antifraud.settings')

app = Celery('django_antifraud')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'load-torlist': {
        'task': 'app_device.tasks.hello',
        'schedule': crontab(),
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
