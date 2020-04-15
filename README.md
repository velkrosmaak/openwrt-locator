# OpenWRT Locator

Snazzy name, right?

This Python 3 script tracks people by checking which wireless access point they are connected to. I have 4 access points in my home, so using this I can see roughly where someone is, and perform actions in Home Assistant accordingly. I can also see when someone isn't connected at all, which assumes they aren't at home. 

I'm using it at home and it works great. It's by no means production ready, so use it at your own risk.

**The script is extremely crude, and needs improvements.**

The script works by connecting to each OpenWRT AP via SSH, and executing `ubus call hostapd.wlan1 get_clients` which lists all the clients connected to a particular interface (the SSID associated with wlan1). The script then checks which AP any of the MAC addresses we care about are connected to. 

Your AP's creds, and home assistant API token are defined in the script in plain text. This is something on my list to improve. It's all a work in progress. 

## Requirements

* Python 3
* paramiko library (`pip install paramiko`)
* Home Assistant
* OpenWRT on your wireless access points
* At least 2 AP's to make this worthwhile.

## Setup
* Clone the repo
* Modify the oh.py script with your credentials and Home Assistant URL and token.
* Run `python oh.py` to test everything is working. You should see new sensors for people created in Home Assistant.
* Create a cron job (`crontab -e`) to run the script every minute (or however frequent you wish).
