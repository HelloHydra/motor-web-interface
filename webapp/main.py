#!/usr/bin/env python3

from flask import Flask, request, render_template, redirect, url_for
import datetime

app = Flask(__name__)

input_lines = list()

@app.route('/')
def index():
    return render_template('index.html', input_lines=input_lines)

@app.route('/display', methods=['POST'])
def display():
    input_lines.append(request.form['line'])
    return redirect(url_for('index'))

@app.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return "Quitting..."

if __name__ == '__main__':
    app.run()
