export DISPLAY=:0.0
killall chromium-browser
sudo killall python3

sudo rm -rf ~/.cache/chromium
sudo nohup python3 FRIDAY-Mirror.py &
sleep 10
./keepchromiumopen.sh &
