#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd


with open("pipeline_bisecting.pkl", "rb") as f:
    model = pickle.load(f)


news_df = pd.read_json("./dataset/test.json", lines=True)
articles = (news_df['headline'] + " " + news_df['short_description']).tolist()

preds = model.predict(articles)

news_df['cluster'] = preds

print(news_df[['headline', 'short_description', 'cluster']].head())
