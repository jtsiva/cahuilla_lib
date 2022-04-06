#!/bin/python3

from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = '2647c09074614974e9a936a37e2265ec'


@app.route('/')
def index():
    return render_template('index.html')