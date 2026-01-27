import json
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "iot/measurements"

def on_connect(client, userdata, flags, rc):
    print("MQTT connecté avec le code :", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    from .models import Sensor, Measurement  

    try:
        payload = json.loads(msg.payload.decode())
        print("Message reçu :", payload)

        sensor_id = payload.get("sensor_id")
        value = payload.get("value")
        unit = payload.get("unit")

        if not sensor_id or value is None or not unit:
            print("Payload invalide :", payload)
            return

        sensor = Sensor.objects.get(id=sensor_id)

        Measurement.objects.create(
            sensor=sensor,
            value=value,
            unit=unit
        )

        print("Mesure enregistrée")

    except Exception as e:
        print("Erreur MQTT :", e)


def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_start()
