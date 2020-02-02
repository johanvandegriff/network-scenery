import json
from pymongo import MongoClient
from networkScanner import scan, scanDict

INTERFACES = {"wlan1": ""}
ROOT = "/home/pi/Nextcloud/NetworkVisualizer/network-scenery/"

with open(ROOT + '/secret.json') as f:
  key = json.load(f)['mongodb']

client = MongoClient(key)
db = client.networkviz

print(db.arp_scans)

#s = scanDict(INTERFACES)

#print(s)

#print(db.arp_scans.insert_many(s))
#print(people.insert_one(me))
for doc in db.arp_scans.find({}): print(doc)
