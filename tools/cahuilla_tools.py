#!/bin/python3

from flask import Flask, render_template, request, flash, redirect, url_for
from orthography.orthography import Orthography
from dictionary.dictionary import Dictionary
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '2647c09074614974e9a936a37e2265ec'

ORTHOGRAPHY_FILE = '../sounds/orthography.json'
DICT_SCHEMA = "dictionary/schema_v2.json"
DICT_WORDS = "../words/dict.json"

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/orthography', methods=['GET', 'POST'])
def orthography():
    ortho = Orthography(ORTHOGRAPHY_FILE)
    text = ""
    if request.method == 'POST':
        text = ortho.convert_orthography(request.form['input'].strip())
        return render_template('orthography.html', text=text)
    elif request.method == 'GET':
        return render_template('orthography.html', text=text)

@app.route('/dictionary', methods=['GET', 'POST'])
def dictionary():
    cahuilla_dict = Dictionary(DICT_SCHEMA, DICT_WORDS)

    cahuilla_dict.load()
    results = []
    if request.method == 'POST':
        results = cahuilla_dict.lookup(request.form['input'].strip())

    return render_template('dictionary.html', results=results)

@app.route('/dictionary/<string:entry_id>/')
def dictionary_entry(entry_id):
    cahuilla_dict = Dictionary(DICT_SCHEMA, DICT_WORDS)

    cahuilla_dict.load()
    entry = cahuilla_dict.get(entry_id)
    return render_template('entry.html', entry=entry, cahuilla_dict=cahuilla_dict)

@app.route('/dictionary/<string:entry_id>/edit', methods=['GET', 'POST'])
def edit_dictionary_entry(entry_id):
    """
    Handles the edit page rendering and dictionary updates 
    """

    cahuilla_dict = Dictionary(DICT_SCHEMA, DICT_WORDS)



    cahuilla_dict.load()
    entry = cahuilla_dict.get(entry_id)

    if request.method == 'POST':
        cahuilla = request.form['cahuilla']
        # entry = request.form['entry']

        if not cahuilla:
            flash("You need to enter a word in the Cahuilla field!")
        else:
            update_items = []         

            entry['cahuilla'] = cahuilla
            entry['english'] = eng_words = request.form.getlist('english')
            entry['pos'] = pos = request.form.getlist('pos')
            entry['origin'] = request.form['origin']
            entry['tags'] = tags = request.form.getlist('tag')
            entry['source'] = request.form['source']

            old_related = entry['related'] #save for cleaning up backlinks
            entry['related'] = request.form.getlist('related')
            entry['notes'] = request.form.getlist('note')

            print (entry)
            update_items.append(entry)

            #update related entries for reciprocal
            if set(old_related) != set(entry['related']):

                #go through related entries to see
                #if there are new entries so that we can
                #set up reciprocals
                for item in entry['related']:
                    if item not in old_related:
                        fixup_entry = cahuilla_dict.get(item)
                        fixup_entry['related'].append(entry['id'])
                        update_items.append(fixup_entry)

                #go through the old related entries to see
                #if a related item was removed. Go fix up
                #the reciprocal reference
                for old_item in old_related:
                    if old_item not in entry['related']:
                        fixup_entry = cahuilla_dict.get(old_item)
                        fixup_entry['related'].remove(entry['id'])
                        update_items.append(fixup_entry)

            for updated_entry in update_items:
                print (updated_entry)
                cahuilla_dict.update(updated_entry)

            #save
            cahuilla_dict.save()
            return redirect(url_for('dictionary_entry', entry_id=entry_id))


    return render_template('edit_entry.html', entry=entry, cahuilla_dict=cahuilla_dict)

@app.route('/dictionary/new_entry/')
def new_entry():
    """
    Set up a new blank entry and redirect to the edit page
    """
    cahuilla_dict = Dictionary(DICT_SCHEMA, DICT_WORDS)

    cahuilla_dict.load()

    new_entry = cahuilla_dict.get_blank()

    cahuilla_dict.add_prefilled(new_entry)
    cahuilla_dict.save()

    return redirect(url_for('edit_dictionary_entry', entry_id=new_entry['id']))

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