from mqtt_init import connect
import time

client = connect()
feed_topic = "pet/feeder/feed"

def send_feed_request():
    client.publish(feed_topic, "feed")
    print("[✓] Manual feeding request sent.")

if __name__ == "__main__":
    print("🐾 Manual Feed Button")
    print("Press ENTER to send a feeding request (or Ctrl+C to exit)")
    try:
        while True:
            input()
            send_feed_request()
    except KeyboardInterrupt:
        print("\n[!] Exiting...")
        client.loop_stop()
