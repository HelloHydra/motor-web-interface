#!/usr/bin/env python3

from flask import Flask, request, render_template, redirect, url_for, jsonify
import datetime

app = Flask(__name__)

input_lines = list()

@app.route('/')
def index():
    return render_template('index.html', uptime="5 days" )

@app.route("/_led")
def _led():
    state = request.args.get('state')
    if state == 'on':
        print("Led ON")
    else:
        print("Led OFF")
    return ''

@app.route("/_button")
def _button():
    state = "not pressed"
    return jsonify(buttonState=state)

@app.route("/_stats")
def _stats():
    uptime = str(datetime.datetime.time(datetime.datetime.now()))
    return jsonify(stats=uptime)


@app.route('/display', methods=['POST'])
def display():
    input_lines.append(request.form['line'])
    print("received")
    return redirect(url_for('index'))

@app.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return "Quitting..."

if __name__ == '__main__':
    app.run()
