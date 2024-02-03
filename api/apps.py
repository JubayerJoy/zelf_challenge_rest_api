from django.apps import AppConfig

from api.cron_job import fetch_and_store_data


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
