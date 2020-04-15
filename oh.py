import paramiko
import json
import requests

# Access points to use. Assumes same credentials on each AP.
access_points = ["ap2", "ap3", "ap4"]
ap_username = "root"
ap_password = "ap_password"

# WiFi MAC addresses of phones to track
person_a = "AA:BB:CC:DD:EE:FF"
person_a_present = False
person_b = "AA:BB:CC:DD:EE:FF"
person_bpresent = False

# home assistant config
hass_url = "https://my.hass-url.org:8123"
hass_api_token = "HASS API TOKEN"


def send2hass(person, apname):
    '''
    Updates the person_nearest_ap sensor in HASS with the person and AP name.
    '''
    
    url = hass_url + "/api/states/sensor." + person + "_nearest_ap"
    
    payload = "{\"state\": \"" + apname + "\"}"
    headers = {
    'Authorization': 'Bearer ' + hass_api_token,
    'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data = payload)

    return(response.text.encode('utf8'))

# set up the ssh client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for ap in access_points:    
    # connect to ssh
    ssh.connect(ap, username=ap_username, password=ap_password)

    #run the ssh command for the bt homehubs
    ssh_stdin, ssh_stdout, ssh_stderr  = ssh.exec_command("ubus call hostapd.wlan1 get_clients")
    #run the ssh command for the tp link
    ssh_stdin2, ssh_stdout2, ssh_stderr2  = ssh.exec_command("ubus call hostapd.wlan0 get_clients")

    # load the output of the ssh command as a json dict
    dct = (json.loads(ssh_stdout.read().decode('utf-8'))["clients"].keys())
    # load the output for thr wlan1 command
    dct2 = (json.loads(ssh_stdout2.read().decode('utf-8'))["clients"].keys())
    
    if person_a in dct or person_a in dct2:
        print("person_a is on " + ap)
        print(send2hass("person_a", ap))
        person_a_present = True
        
    if person_b in dct or person_b in dct2:
        print("person_b is on " + ap)
        print(send2hass("person_b", ap))
        person_b_present = True
        
# check if we are associated with any aps at all        
if person_a_present == False:
    print("person_a is away")
    print(send2hass("person_a", "away"))

if person_b_present == False:
    print("person_b is away")
    print(send2hass("person_b", "away"))