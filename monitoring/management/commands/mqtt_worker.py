from django.core.management.base import BaseCommand
from monitoring.mqtt_client import run_mqtt

class Command(BaseCommand):
    help = "Démarre le worker MQTT pour les capteurs IoT"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(" IoT MQTT Worker démarré !"),
            ending='\n'
        )
        self.stdout.write("Attente des mesures (temp, humidité, lumière)...")
        run_mqtt()
