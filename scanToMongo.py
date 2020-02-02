import json
from pymongo import MongoClient
from networkScanner import scan, scanDict

INTERFACE = "wlan1"

with open('secret.json') as f:
    key = json.load(f)['mongodb']

client = MongoClient(key)
db = client.networkviz

print(db.scans)

s = scanDict(INTERFACE)

#print(s)

#for i in s:
#    print(i)
print(db.scans.insert_many(s))
#print(people.insert_one(me))
#for doc in db.people.find({}):
#    print(doc)
