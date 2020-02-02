from pymongo import MongoClient
import json

with open('secret.json') as f:
  key = json.load(f)['mongodb']

#key += "&ssl=true&ssl_cert_reqs=CERT_NONE"
print(key)

client = MongoClient(key) #, connect=False)
db = client.test
people = db.people

print(people)

me={"name": "Johan", "age": 21, "coolnessFactor": 9001, "gamerPoints": 350}
#print(people.insert_one(me))
for doc in db.people.find({}):
    print(doc)
