from celery import Celery

celery_app = Celery(
    'tc_gen',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
)

celery_app.autodiscover_tasks(['file_manager.tasks'])
