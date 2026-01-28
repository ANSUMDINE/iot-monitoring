import json
import paho.mqtt.client as mqtt
from monitoring.models import Sensor, Measurement
import logging

MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/measurements"

def on_connect(client, userdata, flags, rc):
    print(" MQTT connecté avec succès ! (rc = {})".format(rc))
    print(f" Abonné au topic : {MQTT_TOPIC}")
    client.subscribe(MQTT_TOPIC)
    print(" Prêt à recevoir les données IoT !")

def on_message(client, userdata, msg):
    print(f" NOUVEAU MESSAGE MQTT reçu sur {msg.topic}")
    
    try:
        payload = msg.payload.decode("utf-8")
        print(f" Payload brut: {payload}")
    except UnicodeDecodeError as e:
        print(f" Erreur décodage: {e}")
        return

    try:
        data = json.loads(payload)
        print(f" Données parsées: {data}")
    except json.JSONDecodeError as e:
        print(f" JSON invalide: {e}")
        return

    if not all(k in data for k in ("sensor_id", "type", "value", "unit")):
        print(f"  Clés manquantes. Attendu: sensor_id,type,value,unit. Reçu: {data}")
        return

    try:
        sensor, created = Sensor.objects.get_or_create(
            sensor_id=data["sensor_id"],
            defaults={
                "name": f"Sensor {data['sensor_id']}",
                "sensor_type": data["type"],
            }
        )
        if created:
            print(f" Nouveau capteur créé: {sensor.name} (type: {sensor.sensor_type})")

        measurement = Measurement.objects.create(
            sensor=sensor,
            value=data["value"],
            unit=data["unit"]
        )
        print(f" MESURE ENREGISTRÉE: {data['value']} {data['unit']} | Capteur: {sensor.name} | ID: {measurement.id}")
        print("-" * 50)
        
    except Exception as e:
        print(f" ERREUR DB: {e}")
        import traceback
        traceback.print_exc()

def run_mqtt():
    print(" Connexion au broker MQTT...")
    print(f" Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f" Topic d'écoute: {MQTT_TOPIC}")
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print(" Boucle MQTT lancée ! Attente des messages...")
        print("=" * 60)
        client.loop_forever()
    except Exception as e:
        print(f" Erreur critique MQTT: {e}")
