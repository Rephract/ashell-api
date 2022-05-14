import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.task_routes = {
#     "migrator.tasks.store_process_data": {"queue": "medium-priority"},
# }

app.conf.task_routes = {
    'launcher.tasks.medium_tasks.*': {"queue": "medium-priority"}}
