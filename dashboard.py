from flask import Flask, request, render_template, url_for, jsonify
import os, re, sys, json, datetime
from sense_hat import SenseHat
from pymongo import MongoClient
yellow = (255, 243, 8)
blue = (3, 45, 255)
purple = (197, 8, 255)
green = (82, 255, 8)

ROOT = "/home/pi/Nextcloud/NetworkVisualizer/network-scenery/"

with open(ROOT + '/secret.json') as f:
  key = json.load(f)['mongodb']

client = MongoClient(key)
db = client.networkviz


sense = SenseHat()

app = Flask(__name__)

def convertTimeStampToDate(timestamp):
    value = datetime.datetime.fromtimestamp(timestamp)
    return value.strftime('%Y-%m-%d %H:%M:%S')

def clearLeftHalf():
    for x in range(4):
        for y in range(8):
            sense.set_pixel(x,y,(0,0,0))



def getMacFromIP(ip):
    device = db.arp_scans.find_one({'IP': ip})
    if device is None:
        return None
    else:
        return device['MAC']


def getMostRecentTime():
    times = [x for x in db.arp_scan_times.find({}).sort("time", -1)]
    if len(times) > 0:
        mostRecentTime = times[0]['time']
        timeFilter = {'time': mostRecentTime}
        mostRecentTimeStr = convertTimeStampToDate(mostRecentTime)
    else:
        timeFilter = {}
        mostRecentTimeStr = ""
    return timeFilter, mostRecentTimeStr

@app.route("/")
def main():
    clearLeftHalf()

    sense.set_pixel(0,0,purple) #1 purple
    sense.set_pixel(0,1,purple) #1 purple
    sense.set_pixel(1,0,purple) #1 purple
    sense.set_pixel(1,1,purple) #1 purple
    sense.set_pixel(0,2,yellow) #2 yellow
    sense.set_pixel(0,3,yellow) #2 yellow
    sense.set_pixel(1,2,yellow) #2 yellow
    sense.set_pixel(1,3,yellow) #2 yellow
    sense.set_pixel(0,4,green) #3 green
    sense.set_pixel(0,5,green) #3 green
    sense.set_pixel(1,4,green) #3 green
    sense.set_pixel(1,5,green) #3 green
    sense.set_pixel(0,6,blue) #4 blue
    sense.set_pixel(0,7,blue) #4 blue
    sense.set_pixel(1,6,blue) #4 blue
    sense.set_pixel(1,7,blue) #4 blue
    sense.set_pixel(2,0,blue) #5 blue
    sense.set_pixel(2,1,blue) #5 blue
    sense.set_pixel(3,0,blue) #5 blue
    sense.set_pixel(3,1,blue) #5 blue
    sense.set_pixel(2,2,purple) #6 purple
    sense.set_pixel(2,3,purple) #6 purple
    sense.set_pixel(3,2,purple) #6 purple
    sense.set_pixel(3,3,purple) #6 purple
    sense.set_pixel(2,4,yellow) #7 yellow
    sense.set_pixel(2,5,yellow) #7 yellow
    sense.set_pixel(3,4,yellow) #7 yellow
    sense.set_pixel(3,5,yellow) #7 yellow
    sense.set_pixel(2,6,green) #8 green
    sense.set_pixel(2,7,green) #8 green
    sense.set_pixel(3,6,green) #8 green
    sense.set_pixel(3,7,green) #8 green

    timeFilter, mostRecentTimeStr = getMostRecentTime()

    table = ""
    for doc in db.arp_scans.find(timeFilter):
        table += "<tr>"
        table += "<td>" + doc["network"] + "</td>\n"
        table += "<td>" + doc["IP"] + "</td>\n"
        table += "<td>" + doc["MAC"] + "</td>\n"
        table += "<td>" + doc["device"] + "</td>\n"
        table+= "</tr>"

    ip = request.remote_addr
    return render_template("index.html", data=table, time=mostRecentTimeStr, ip=ip, mac=getMacFromIP(ip))

@app.route("/arp")
def arp():
    timeFilter, mostRecentTimeStr = getMostRecentTime()

    table = []
    for doc in db.arp_scans.find(timeFilter):
        table.append([doc["network"], doc["IP"], doc["MAC"], doc["device"]])
    return json.dumps({"time": mostRecentTimeStr, "arp": table})

@app.route("/users")
def users():
    users = []
    for user in db.users.find():
        del user["_id"]
        users.append(user)
    requests = []
    for request in db.requests.find():
        del request["_id"]
        requests.append(request)
    return json.dumps({"users": users, "requests": requests})

@app.route("/approve")
def approve():
    macFrom = request.args.get("from", "")
    macTo = request.args.get("to", "")
    username = request.args.get("username", "")
    ip = request.remote_addr
    mac = getMacFromIP(ip)
    if mac != macTo:
        return json.dumps({"result": False, "error": "this request is not to you"})
    entry = db.requests.find_one({"from": macFrom, "to": macTo, "username": username})
    if entry is None:
        return json.dumps({"result": False, "error": "the requested request does not exist in requests!"})
    
    db.requests.delete_many({"from": macFrom, "to": macTo, "username": username})

    entry = db.users.find_one({"MAC": macFrom})
    if entry is not None:
        print("MAC address already in database, username updated")
        db.users.update_one({"MAC": macFrom}, { "$set": { "username": username } })
    else:
        db.users.insert_one({"MAC": macFrom, "username": username})
    return json.dumps({"result": True})

@app.route("/deny")
def deny():
    macFrom = request.args.get("from", "")
    macTo = request.args.get("to", "")
    username = request.args.get("username", "")
    ip = request.remote_addr
    mac = getMacFromIP(ip)
    if mac != macTo and mac != macFrom:
        return json.dumps({"result": False, "error": "this request is not to you or from you"})
    entry = db.requests.find_one({"from": macFrom, "to": macTo, "username": username})
    if entry is None:
        return json.dumps({"result": False, "error": "the requested request does not exist in requests!"})
    
    db.requests.delete_many({"from": macFrom, "to": macTo, "username": username})

    return json.dumps({"result": True})

@app.route("/usersOverTime")
def usersOverTime():
    data = db.arp_scan_times.find()
    data = [x for x in data]
    for item in data:
        del item["_id"]
        item["timeStr"] = convertTimeStampToDate(item["time"])
    return json.dumps({"usersOverTime": data})

@app.route("/setUsername")
def setUsername():
    username = request.args.get("username", "")
    if username is None or username == "":
        return json.dumps({"result": False, "error": "missing username"})
    ip = request.remote_addr
    mac = getMacFromIP(ip)
    if mac is None:
        return json.dumps({"result": False, "error": "MAC address not found in database"})
    entry = db.users.find_one({"username": username})
    if entry is not None:
        if entry["MAC"] == mac: #don't need permission for this device itself
            return json.dumps({"result": True})
        #the username is already associated with another device. need to send a request
        db.requests.insert_one({"from": mac, "to": entry["MAC"], "username": username})
        return json.dumps({"result": False, "error": "username already in database"})

    entry = db.users.find_one({"MAC": mac})
    if entry is not None:
        print("MAC address already in database, username updated")
        db.users.update_one({"MAC": mac}, { "$set": { "username": username } })
    else:
        db.users.insert_one({"MAC": mac, "username": username})
    return json.dumps({"result": True})

    

@app.route("/profile")
def test():
    clearLeftHalf()

    sense.set_pixel(0,0,yellow) #1
    sense.set_pixel(0,1,yellow) #1
    sense.set_pixel(1,0,yellow) #1
    sense.set_pixel(1,1,yellow) #1
    sense.set_pixel(0,2,blue) #2 blue
    sense.set_pixel(0,3,blue) #2 blue
    sense.set_pixel(1,2,blue) #2 blue
    sense.set_pixel(1,3,blue) #2 blue
    sense.set_pixel(0,4,green) #3 green
    sense.set_pixel(0,5,green) #3 green
    sense.set_pixel(1,4,green) #3 green
    sense.set_pixel(1,5,green) #3 green
    sense.set_pixel(0,6,purple) #4 purple
    sense.set_pixel(0,7,purple) #4 purple
    sense.set_pixel(1,6,purple) #4 purple
    sense.set_pixel(1,7,purple) #4 purple
    sense.set_pixel(2,0,purple) #5 purple
    sense.set_pixel(2,1,purple) #5 purple
    sense.set_pixel(3,0,purple) #5 purple
    sense.set_pixel(3,1,purple) #5 purple
    sense.set_pixel(2,2,green) #6 green
    sense.set_pixel(2,3,green) #6 green
    sense.set_pixel(3,2,green) #6 green
    sense.set_pixel(3,3,green) #6 green
    sense.set_pixel(2,4,blue) #7 blue
    sense.set_pixel(2,5,blue) #7 blue
    sense.set_pixel(3,4,blue) #7 blue
    sense.set_pixel(3,5,blue) #7 blue
    sense.set_pixel(2,6,yellow) #8 yellow
    sense.set_pixel(2,7,yellow) #8 yellow
    sense.set_pixel(3,6,yellow) #8 yellow
    sense.set_pixel(3,7,yellow) #8 yellow

    ip = request.remote_addr
    return render_template("profile.html", ip=ip, mac=getMacFromIP(ip))

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

if __name__ == "__main__":
    # app.run()
    app.run(host= '0.0.0.0') # for local testing
