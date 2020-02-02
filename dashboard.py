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
    table = ""

#    with open("/home/pi/lastTime.json", 'r') as f:
#        lastTime = json.load(f) #json loads it as a float

    times = [x for x in db.arp_scan_times.find({}).sort("time", -1)]
    if len(times) > 0:
        mostRecentTime = times[0]['time']
        filter = {'time': mostRecentTime}
        mostRecentTimeStr = convertTimeStampToDate(mostRecentTime)
    else:
        filter = {}
        mostRecentTimeStr = ""

    print(filter)

    for doc in db.arp_scans.find(filter):
        table += "<tr>"
        table += "<td>" + doc["network"] + "</td>\n"
        table += "<td>" + doc["IP"] + "</td>\n"
        table += "<td>" + doc["MAC"] + "</td>\n"
        table += "<td>" + doc["device"] + "</td>\n"
        table+= "</tr>"

    ip = request.remote_addr
    return render_template("index.html", data=table, time=mostRecentTimeStr, ip=ip, mac=getMacFromIP(ip))

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
