#!/usr/bin/env python
# coding: utf-8

import numpy as np 
import pandas as pd

import string
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.cluster import BisectingKMeans

from sklearn.pipeline import Pipeline

import pickle

import nltk
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer

nltk.download('punkt') 
nltk.download('stopwords') 
nltk.download('wordnet')

news_df = pd.read_json("./dataset/small_dataset_articles.json", lines=True)
# Define the pipeline

# tokenization
def preprocess_text(text, use_lemmatization=True):
    text = str(text) 
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)

# stopwords removal
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]

# case conversion
    tokens = [token.lower() for token in tokens]

# lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return tokens


# tokenization

headlines_text = news_df['headline'].apply(lambda x: preprocess_text(x, use_lemmatization=True))
description_text = news_df['short_description']. apply(lambda x: preprocess_text(x, use_lemmatization=True))

headlines_tokens = headlines_text.tolist()
description_tokens = description_text.tolist()


def combine(headlines_tokens, description_tokens):
    articles = []
    for headline_tokens, desc_tokens in zip(headlines_tokens, description_tokens):
        headline = " ".join(headline_tokens)      
        description = " ".join(desc_tokens)      
        articles.append(headline + " " + description)
    return articles


articles = combine(headlines_tokens, description_tokens)


pipeline_bisecting = Pipeline([
    ('tfidf', TfidfVectorizer(max_df=0.02, min_df=20, stop_words='english')),
    ('svd', TruncatedSVD(n_components=100)),
    ('scaler', StandardScaler()),
    ('kmeans', BisectingKMeans(n_clusters=27, random_state=22))
])


pipeline_bisecting.fit(articles)


with open("pipeline_bisecting.pkl", "wb") as f:
    pickle.dump(pipeline_bisecting, f)

print("Pipeline saved as pipeline_bisecting.pkl")
