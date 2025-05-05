from mqtt_init import connect

client = connect()
bowl_topic = "pet/feeder/bowl"

def send_bowl_status(is_full):
    value = "1" if is_full else "0"
    client.publish(bowl_topic, value)
    print(f"[✓] Bowl status sent: {'Full' if is_full else 'Empty'}")

if __name__ == "__main__":
    print("🐾 Bowl Full Sensor")
    print("Choose bowl status:")
    print("1. Full")
    print("0. Empty")

    try:
        choice = input("Enter 0 or 1: ").strip()
        if choice in ["0", "1"]:
            send_bowl_status(choice == "1")
        else:
            print("⚠ Invalid choice.")
    except KeyboardInterrupt:
        print("\n[!] Exiting...")
        client.loop_stop()
