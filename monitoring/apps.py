
"""
from django.apps import AppConfig
from .mqtt_client import start_mqtt

class MonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoring'

    def ready(self):
        start_mqtt()
"""

from django.apps import AppConfig
import os

class MonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoring'

    def ready(self):
        # Désactiver MQTT si demandé
        if os.environ.get("DISABLE_MQTT") == "true":
            print("MQTT désactivé via DISABLE_MQTT")
            return

        # Ne pas lancer MQTT pendant les migrations ou le reloader
        if os.environ.get("RUN_MAIN") != "true":
            return

        from .mqtt_client import start_mqtt
        start_mqtt()

