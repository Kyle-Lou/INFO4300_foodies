import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the path to the JSON file relative to the current script
json_file_path = os.path.join(current_directory, 'test.json')

# Assuming your JSON data is stored in a file named 'init.json'
with open(json_file_path, 'r') as file:
    data = json.load(file)

app = Flask(__name__)
CORS(app)

# Sample search using json with pandas
def json_search(query):
    # Initialize matched_entry as None
    matched_entry = None

    # Loop through each item in data to find a match by title
    for item in data:
        if item['title'].lower() == query.lower():
            matched_entry = item
            break
    if matched_entry is None:
        print("The input in the search bar can't match an exact title in the existing dataset")
        return []
    descriptions = [matched_entry['description']]
    for item in data:
        if item['title'].lower() != query.lower():
            descriptions.append(item['description'])
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(descriptions)
    cos_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    top_indices = cos_similarities.argsort()[0][-3:][::-1]
    top_matches = []
    for i in top_indices:
        top_matches.append(data[i+1])
    return top_matches
    
@app.route("/")
def home():
    return render_template('base.html',title="sample html")

@app.route("/snacks")
def episodes_search():
    text = request.args.get("title")
    return json_search(text)


if 'DB_NAME' not in os.environ:
    app.run(debug=True,host="0.0.0.0",port=5000)