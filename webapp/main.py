#!/usr/bin/env python3

from flask import Flask, request, render_template, redirect, url_for, jsonify
import datetime

app = Flask(__name__)

input_lines = list()

target_position = 0;
current_position = 0;

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/_switch")
def _led():
    state = request.args.get('state')
    if state == 'on':
        print("Led ON")
    else:
        print("Led OFF")
    return ''

@app.route("/_stats")
def _stats():
    return jsonify(
        motorState="Running",
        currentPosition=str(current_position),
        targetPosition=str(target_position),
        uptime=str(datetime.datetime.now())
        )

@app.route('/_setPosition')
def apply_position():
    global target_position
    target_position = int(request.args.get('value'))
    print("New target position", target_position)
    return ''

if __name__ == '__main__':
    app.run()
