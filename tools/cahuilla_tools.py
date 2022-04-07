#!/bin/python3

from flask import Flask, render_template, request
from orthography.orthography import Orthography

app = Flask(__name__)
app.config['SECRET_KEY'] = '2647c09074614974e9a936a37e2265ec'


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/orthography', methods=['GET', 'POST'])
def orthography():
    ortho = Orthography('../sounds/orthography.json')
    text = ""
    if request.method == 'POST':
        text = ortho.convert_orthography(request.form['input'].strip())
        return render_template('orthography.html', text=text)
    elif request.method == 'GET':
        return render_template('orthography.html', text=text)

@app.route('/dictionary', methods=['GET', 'POST'])
def dictionary():
    
    # if request.method == 'POST':
    #     text = ortho.convert_orthography(request.form['input'].strip())
    #     return render_template('orthography.html', text=text)
    # elif request.method == 'GET':
    #     return render_template('orthography.html', text=text)

    return render_template('dictionary.html')
