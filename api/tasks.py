from celery import shared_task

from api.cron_job import fetch_and_store_data


@shared_task
def celery_fetch_and_store_data():
    fetch_and_store_data()
