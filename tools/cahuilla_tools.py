#!/bin/python3

from flask import Flask, render_template, request, flash, redirect, url_for
from orthography.orthography import Orthography
from dictionary.dictionary import Dictionary
import json

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
    cahuilla_dict = Dictionary("dictionary/schema_v2.json", "../words/dict.json")

    cahuilla_dict.load()
    results = []
    if request.method == 'POST':
        results = cahuilla_dict.lookup(request.form['input'].strip())

    return render_template('dictionary.html', results=results)

@app.route('/dictionary/<string:entry_id>/')
def dictionary_entry(entry_id):
    cahuilla_dict = Dictionary("dictionary/schema_v2.json", "../words/dict.json")

    cahuilla_dict.load()
    entry = cahuilla_dict.get(entry_id)
    return render_template('entry.html', entry=entry)

@app.route('/dictionary/<string:entry_id>/edit', methods=['GET', 'POST'])
def edit_dictionary_entry(entry_id):
    cahuilla_dict = Dictionary("dictionary/schema_v2.json", "../words/dict.json")



    cahuilla_dict.load()
    entry = cahuilla_dict.get(entry_id)

    if request.method == 'POST':
        cahuilla = request.form['cahuilla']
        # entry = request.form['entry']

        if not cahuilla:
            flash("You need to enter a word in the Cahuilla field!")
        else:
            eng_words = request.form.getlist('english')
            if 0 == len(eng_words[-1]):
                eng_words.pop() #remove empty entry at end

            print (eng_words)

            pos = request.form.getlist('pos')
            if 0 == len(pos[-1]):
                pos.pop() #remove empty entry at end
            print (pos)

            # cahuilla_dict.update(entry)

            # #save
            # cahuilla_dict.save()
            # return redirect(url_for('dictionary_entry'))


    return render_template('edit_entry.html', entry=entry)

@app.context_processor
def get_resources():
    #read in index for sources
    #read in tags file
    src = []
    tag_set = []
    with open("../resources/index.json") as file:
        src = json.load(file)
    with open ("../resources/tags.json") as file:
        tag_set = json.load(file)
    return dict(sources=src, tag_set=tag_set)