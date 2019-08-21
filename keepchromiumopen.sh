#!/bin/bash
echo "keeping chromium open"
while true
do

        if ! [[ $(pidof /usr/lib/chromium-browser/chromium-browser) ]];
        then
                echo "opening chrome"

                chromium-browser --kiosk --incognito http://localhost:8000/main$
                sleep 10

        fi
done


