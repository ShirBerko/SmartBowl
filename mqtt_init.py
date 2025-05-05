import paho.mqtt.client as mqtt
import random

broker = "mqtt.eclipseprojects.io"
port = 1883
client_name = f"IOT_PetFeeder_{random.randint(1000, 9999)}"

client = mqtt.Client(client_name)

def connect():
    client.connect(broker, port)
    client.loop_start()
    print(f"[✓] Connected to MQTT Broker as {client_name}")
    return client
