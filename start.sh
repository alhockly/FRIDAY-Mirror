killall chromium-browser
sudo killall python3

sudo python3 FRIDAY-Mirror.py &
sleep 5
chromium-browser http://localhost:8000/web/main.html --kiosk &