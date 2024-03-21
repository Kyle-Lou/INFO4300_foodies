import json
import os
from helpers import analysis
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the path to the JSON file relative to the current script
json_file_path = os.path.join(current_directory, 'test.json')

# Assuming your JSON data is stored in a file named 'init.json'
with open(json_file_path, 'r') as file:
    data = json.load(file)

app = Flask(__name__)
CORS(app)


def autocomplete_search(query):
    suggestions = []

    for item in data:
        if query.lower() in item['title'].lower():
            suggestions.append(item)

            if len(suggestions) >= 10:
                break

    return suggestions


def detailed_search(query, allergens=None, preferred_ingredients=None):
    # matched_entry = next((item for item in data if item['title'].lower() == title.lower()), None)
    # if not matched_entry:
    #   return []

    # descriptions = [matched_entry['description']] + [item['description'] for item in data if item['title'].lower() != title.lower()]
    # vectorizer = TfidfVectorizer()
    # tfidf_matrix = vectorizer.fit_transform(descriptions)
    # cos_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    # top_indices = cos_similarities.argsort()[0][-3:][::-1]

    # top_matches = [data[i + 1] for i in top_indices]
    # return top_matches
    top_match_tuples = analysis.get_top_matches(query, data, allergens, preferred_ingredients)
    matches = []
    for jacc_val, data_ind in top_match_tuples:
        matches.append(data[data_ind])
    return matches


@app.route("/")
def home():
    return render_template('base.html', title="sample html")

# @app.route("/snacks")
# def episodes_search():
#     text = request.args.get("title")
#     return json_search(text)


@app.route("/autocomplete")
def autocomplete():
    query = request.args.get("title", "")
    return jsonify(autocomplete_search(query))


@app.route("/search")
def search():
    title = request.args.get("title", "")
    allergies = request.args.getlist('allergies')
    preferred_ingredients = request.args.getlist('preferred_ingredients')
    # print(title, allergies, ingredients)
    allergies = [a.strip().lower() for a in allergies if a.strip()]
    preferred_ingredients = [i.strip().lower() for i in preferred_ingredients if i.strip()]
    print(preferred_ingredients)
    results = detailed_search(title, allergies, preferred_ingredients)

    return jsonify(results)


if 'DB_NAME' not in os.environ:
    app.run(debug=True, host="0.0.0.0", port=5000)
