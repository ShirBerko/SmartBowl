import sounddevice as sd
import numpy as np
import sqlite3
import time
from mqtt_init import connect

# התחברות ל-MQTT
client = connect()

# הגדרות קבועות
NOISE_THRESHOLD = 0.0005          # סף רעש (אפשר להתאים)
BOWL_LEVEL_THRESHOLD = 20       # אחוז מינימום בקערה שמפעיל מילוי
AUTO_FEED_AMOUNT = 40           # הכמות שימולא כשמתגלה רעש (ניתן לשנות)

# פונקציה לזיהוי רעש מהסביבה
def detect_noise(threshold=NOISE_THRESHOLD, duration=1.0):
    try:
        audio = sd.rec(int(duration * 44100), samplerate=44100, channels=1)
        sd.wait()
        volume_norm = np.linalg.norm(audio) / len(audio)
        print(f"[🎙] Noise Level: {volume_norm:.4f}")
        return volume_norm > threshold
    except Exception as e:
        print(f"[⚠] Error detecting noise: {e}")
        return False

# פונקציה לבדוק מה מצב הקערה לפי בסיס הנתונים
def get_bowl_level():
    try:
        conn = sqlite3.connect("pet_feeder.db")
        cursor = conn.cursor()
        cursor.execute("SELECT bowl_level FROM feed_log ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 100  # אם אין נתונים – מניח שהיא מלאה
    except Exception as e:
        print(f"[⚠] DB Error: {e}")
        return 100

# לולאה ראשית – האזנה לרעש ובדיקה
print("[🔁] AutoFeeder is running...")
try:
    while True:
        if detect_noise():
            level = get_bowl_level()
            print(f"[📊] Bowl level: {level}%")
            if level < BOWL_LEVEL_THRESHOLD:
                print(f"[🤖] Auto-feeding: {AUTO_FEED_AMOUNT}%")
                client.publish("pet/feeder/feed", str(AUTO_FEED_AMOUNT))
            else:
                print("[✅] Bowl level is sufficient. No action taken.")
        time.sleep(5)
except KeyboardInterrupt:
    print("\n[!] AutoFeeder stopped.")
    client.loop_stop()
