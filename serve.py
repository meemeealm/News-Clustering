#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, jsonify
import pickle

# Load the trained pipeline
with open("pipeline_bisecting.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

# Home route with HTML form
@app.route("/", methods=["GET"])
def home():
    return """
    <form action="/predict" method="post">
        <input name="headline" placeholder="Headline">
        <input name="short_description" placeholder="Description">
        <button type="submit">Predict</button>
    </form>
    """

def combine_text(headline, description):
    return f"{headline} {description}"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
    except:
        data = None

    articles = []

    if isinstance(data, dict):
        articles = [combine_text(data.get("headline", ""), data.get("short_description", ""))]
    elif isinstance(data, list):
        articles = [combine_text(item.get("headline", ""), item.get("short_description", "")) for item in data]
    else:
        headline = request.form.get("headline", "")
        description = request.form.get("short_description", "")
        articles = [combine_text(headline, description)]

    preds = model.predict(articles)

    results = []
    for article, label in zip(articles, preds):
        results.append({"text": article, "cluster": int(label)})

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
