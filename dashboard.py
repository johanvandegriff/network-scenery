from flask import Flask, request, render_template, url_for, jsonify
import os, re, sys
from sense_hat import SenseHat
import json
from pymongo import MongoClient

with open('secret.json') as f:
  key = json.load(f)['mongodb']

client = MongoClient(key)
db = client.networkviz


sense = SenseHat()

app = Flask(__name__)

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

    table = ""

    for doc in db.scans.find({}):
        table += "<tr>"
        table += "<td>" + doc["IP"] + "</td>\n"
        table += "<td>" + doc["MAC"] + "</td>\n"
        table += "<td>" + doc["device"] + "</td>\n"
        table+= "</tr>"

    return render_template("index.html", data=table, ip=request.remote_addr)

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

    return render_template ("profile.html", ip=request.remote_addr)

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

if __name__ == "__main__":
    # app.run()
    app.run(host= '0.0.0.0') # for local testing
