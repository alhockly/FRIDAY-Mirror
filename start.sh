killall chromium-browser
sudo killall python3

sudo python3 FRIDAY-Mirror.py &
sleep 10
chromium-browser http://localhost:8000/main.html --kiosk &