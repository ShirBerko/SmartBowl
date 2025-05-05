import sqlite3

conn = sqlite3.connect("pet_feeder.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM feeding_schedule")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
