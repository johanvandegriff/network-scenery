from flask import Flask, request, render_template, url_for, jsonify
import os, re, sys
from sense_hat import SenseHat
import json
from pymongo import MongoClient

ROOT = "/home/pi/Nextcloud/NetworkVisualizer/network-scenery/"

with open(ROOT + '/secret.json') as f:
  key = json.load(f)['mongodb']

client = MongoClient(key)
db = client.networkviz


sense = SenseHat()

app = Flask(__name__)

def getMacFromIP(ip):
    device = db.scans.find_one({'IP': ip})
    if device is None:
        return None
    else:
        return device['MAC']


@app.route("/")
def main():


    sense.clear()

    sense.set_pixel(0,0,(197, 8, 255)) #1 puple
    sense.set_pixel(0,1,(197, 8, 255)) #1 puple
    sense.set_pixel(1,0,(197, 8, 255)) #1 puple
    sense.set_pixel(1,1,(197, 8, 255)) #1 puple
    sense.set_pixel(0,2,(255, 243, 8)) #2 yellow
    sense.set_pixel(0,3,(255, 243, 8)) #2 yellow
    sense.set_pixel(1,2,(255, 243, 8)) #2 yellow
    sense.set_pixel(1,3,(255, 243, 8)) #2 yellow
    sense.set_pixel(0,4,(82, 255, 8)) #3 green
    sense.set_pixel(0,5,(82, 255, 8)) #3 green
    sense.set_pixel(1,4,(82, 255, 8)) #3 green
    sense.set_pixel(1,5,(82, 255, 8)) #3 green
    sense.set_pixel(0,6,(3, 45, 255)) #4 blue
    sense.set_pixel(0,7,(3, 45, 255)) #4 blue
    sense.set_pixel(1,6,(3, 45, 255)) #4 blue
    sense.set_pixel(1,7,(3, 45, 255)) #4 blue

    table = ""

    for doc in db.scans.find({}):
        table += "<tr>"
        table += "<td>" + doc["IP"] + "</td>\n"
        table += "<td>" + doc["MAC"] + "</td>\n"
        table += "<td>" + doc["device"] + "</td>\n"
        table+= "</tr>"

    ip = request.remote_addr
    return render_template("index.html", data=table, ip=ip, mac=getMacFromIP(ip))

@app.route("/profile")
def test():
    sense.set_pixel(0,0,(82, 255, 8)) #1 green
    sense.set_pixel(0,1,(82, 255, 8)) #1 green
    sense.set_pixel(1,0,(82, 255, 8)) #1 green
    sense.set_pixel(1,1,(82, 255, 8)) #1 green
    sense.set_pixel(0,2,(3, 45, 255)) #2 blue
    sense.set_pixel(0,3,(3, 45, 255)) #2 blue
    sense.set_pixel(1,2,(3, 45, 255)) #2 blue
    sense.set_pixel(1,3,(3, 45, 255)) #2 blue
    sense.set_pixel(0,4,(197, 8, 255)) #3 puple
    sense.set_pixel(0,5,(197, 8, 255)) #3 puple
    sense.set_pixel(1,4,(197, 8, 255)) #3 puple
    sense.set_pixel(1,5,(197, 8, 255)) #3 puple
    sense.set_pixel(0,6,(255, 243, 8)) #4 yellow
    sense.set_pixel(0,7,(255, 243, 8)) #4 yellow
    sense.set_pixel(1,6,(255, 243, 8)) #4 yellow
    sense.set_pixel(1,7,(255, 243, 8)) #4 yellow

    ip = request.remote_addr
    return render_template("profile.html", ip=ip, mac=getMacFromIP(ip))

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

if __name__ == "__main__":
    # app.run()
    app.run(host= '0.0.0.0') # for local testing
