#!/bin/bash
if pgrep "node" > /dev/null
then
    echo "Running"
else
    node /home/pi/scara_server/server.js
fi
