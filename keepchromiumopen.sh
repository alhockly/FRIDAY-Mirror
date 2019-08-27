#!/bin/bash
echo "keeping chromium open"
while true
do

        if ! [[ $(pidof /usr/lib/chromium-browser/chromium-browser) ]];
        then
                echo "restarting Mirror due to chrome crash/close"

                ./start.sh
                sleep 10

        fi
done


