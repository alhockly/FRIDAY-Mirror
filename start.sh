export DISPLAY=:0.0
killall chromium-browser
killall keepchromiumopen.sh
sudo killall python3

sudo rm -rf ~/.cache/chromium
sudo nohup python3 FRIDAY-Mirror.py &
sleep 10
chromium-browser --kiosk --incognito http://localhost:8000/main.html &
sleep 5
./keepchromiumopen.sh &
