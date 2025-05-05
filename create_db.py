import sqlite3

conn = sqlite3.connect("pet_feeder.db")
cursor = conn.cursor()

# טבלת לוגים – אם עוד לא קיימת
cursor.execute('''
    CREATE TABLE IF NOT EXISTS feed_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        bowl_level INTEGER
    )
''')

# טבלה חדשה לזמני האכלה
cursor.execute('''
    CREATE TABLE IF NOT EXISTS feeding_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        label TEXT,
        time TEXT
    )
''')

conn.commit()
conn.close()
print("[✓] Database and tables created.")
