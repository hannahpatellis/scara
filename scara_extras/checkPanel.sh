#!/bin/bash
if pgrep "python3" > /dev/null
then
    echo "Running"
else
    DISPLAY=":0" python3 /home/pi/scara_panel/home.py
fi