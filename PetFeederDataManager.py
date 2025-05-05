from mqtt_init import connect
import sqlite3
import time

client = connect()

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[MQTT] Topic: {topic} | Message: {payload}")

    conn = sqlite3.connect("pet_feeder.db")
    cursor = conn.cursor()

    if topic == "pet/feeder/feed" or topic == "pet/feeder/empty":
        try:
            amount = int(payload)
            cursor.execute("INSERT INTO feed_log (timestamp, bowl_level) VALUES (?, ?)", (now, amount))
            action = "Emptied" if amount == 0 else "Feeding"
            print(f"[✓] {action} recorded: {amount}% at {now}")
        except ValueError:
            print(f"[⚠] Invalid payload received: {payload}")

    conn.commit()
    conn.close()

client.subscribe("pet/feeder/feed")
client.subscribe("pet/feeder/empty")
client.on_message = on_message

print("[✓] PetFeeder Data Manager is running... Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[!] Stopping...")
    client.loop_stop()
