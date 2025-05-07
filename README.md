# 🐶 SmartBowl – Smart Pet Feeder

**SmartBowl** is an IoT-based smart feeding system for pets that combines automation, sensors, and user interfaces to ensure pets are fed on time, every time.

## 📌 Features

- 🕹️ **Manual feeding** via button press  
- ⏰ **Scheduled automatic feeding** (set times for morning, noon, and evening)  
- 🧠 **Adaptive feeding** – learns eating habits and adjusts quantity accordingly  
- 🎙️ **Sound-based feeding trigger** – detects barking when bowl is empty and fills it  
- 📊 **GUI dashboard** showing last feeding time and settings  
- 🧪 **Bowl fullness sensor** to avoid overfeeding  

## 🧰 Technologies Used

- `Python 3`
- `PyQt5` for GUI
- `MQTT` protocol (`paho-mqtt`)
- SQLite database (`pet_feeder.db`)
- Simple image/audio files for user interaction

## 🗂️ Main Files

| File                     | Description                                    |
|--------------------------|------------------------------------------------|
| `PetFeederGui.py`        | Main graphical interface                      |
| `FeedingSchedulerGui.py` | Schedule feeding times                        |
| `ManualFeedButton.py`    | Manual feed button interface                  |
| `autoFeeder.py`          | Handles automated feeding logic               |
| `FeederRelay.py`         | Controls the physical relay for feeding       |
| `BowlFullSensor.py`      | Simulates bowl fullness sensor                |
| `PetFeederDataManager.py`| Manages feeding history and stats             |
| `create_db.py`           | Initializes SQLite database                   |
| `mqtt_init.py`           | MQTT setup and configuration                  |
| `view_schedule.py`       | View and manage existing feed schedule        |

## ▶️ How to Run

1. Make sure you have Python 3 installed.
2. Install requirements:
```
pip install PyQt5 paho-mqtt
```
3.Initialize the database:
```
python create_db.py
```
4.Run the main GUI:
```
python PetFeederGui.py
```

