from flask import Flask, request, render_template, url_for

import os, re, sys

app = Flask(__name__)

@app.route("/")
def main():
    #return "<h1>hi!</h1>"
    return render_template("index.html", text="some text")

@app.route("/test")
def test():
    return "<h1>test123</h1>"


if __name__ == "__main__":
    # app.run()
    app.run(host= '0.0.0.0') # for local testing
