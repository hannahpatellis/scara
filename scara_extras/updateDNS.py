## Gets your public IP address and updates a DNS server, this one being the name servers on Digital Ocean
## Handy if you do not have a static public IP, like most residential plans
## Written by Hannah A. Patellis - hannahap.com - @hannahpatellis

import urllib.request
import json
import requests

data = urllib.request.urlopen("http://ip.jsontest.com/").read().decode('utf-8')
data = json.loads(data)
ip = data["ip"]

url = "https://api.digitalocean.com/v2/domains/DOMAIN/records/RECORDNUMBER"
headers = {"Content-Type": "application/json", "Authorization": "Bearer YOUR API KEY"}
data = '{"data": "'+ip+'"}'

r = requests.request('PUT', url, data=data, headers=headers)
