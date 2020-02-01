from flask import Flask, request, render_template, url_for
from networkScanner import scan
import os, re, sys

app = Flask(__name__)

@app.route("/")
def main():

    data =[['10.128.128.1', '00:2f:5c:03:61:50', '(Unknown)'],
     ['10.128.128.50', 'b8:7b:c5:07:69:89', '(Unknown)'],
     ['10.128.128.50', 'b8:7b:c5:07:69:89', '(Unknown) (DUP: 2)']]

    #data = scan("wlan0")




    table = ""
    for line in data:
        table += "<tr>"
        for info in line:
            table += "<td>" + info + "</td>\n"
        table+= "</tr>"
    return render_template("index.html", data=table)

@app.route("/profile")
def test():
    return "<h1>test123</h1>"


if __name__ == "__main__":
    # app.run()
    app.run(host= '0.0.0.0') # for local testing
