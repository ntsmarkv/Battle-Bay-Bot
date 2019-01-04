#!/bin/sh
# launcher.sh
cd /
cd home/pi/bbbot/
sudo python3 1.9.py
# at 6:22 EST, 3:22 PST (we are on PST); 15:22
22 15 * * * /bbbot/launcher.sh >/bbbot/logs/cronlog.log 2>&1
