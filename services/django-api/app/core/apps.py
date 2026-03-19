import os

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from .mqtt_client import start_mqtt_listener

        start_mqtt_listener()
