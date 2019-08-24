#!/bin/bash
echo "keeping chromium open"
while true
do

        if ! [[ $(pidof /usr/lib/chromium-browser/chromium-browser) ]];
        then
                echo "opening chrome"

                ./start.sh
                sleep 10

        fi
done


