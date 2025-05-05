@echo off
echo [✓] Running SmartBowl System...

start "" python PetFeederDataManager.py
timeout /t 2 >nul

start "" python PetFeederGui.py
timeout /t 1 >nul

start "" python FeedingSchedulerGui.py

echo [✓] All components launched.
pause
