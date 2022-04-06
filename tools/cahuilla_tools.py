#!/bin/python3

from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = '2647c09074614974e9a936a37e2265ec'


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/orthography', methods=['GET', 'POST'])
def orthography():
    return render_template('orthography.html')