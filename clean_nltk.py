# this file will remove the languages in nltk_data

import os

# Paths to corpora/tokenizers
stopwords_path = "./nltk_data/corpora/stopwords"
punkt_path = "./nltk_data/tokenizers/punkt"
punkt_tab_path = "./NLP/nltk_data/tokenizers/punkt_tab"

# Keep only English
keep_stopwords = {"english"}
keep_punkt = {"english.pickle"}
keep_punkt_tab = {"english"}

# Remove non-English stopwords
for fname in os.listdir(stopwords_path):
    if fname not in keep_stopwords:
        os.remove(os.path.join(stopwords_path, fname))
        print(f"Removed stopwords: {fname}")

# Remove non-English punkt models
for fname in os.listdir(punkt_path):
    if fname not in keep_punkt:
        os.remove(os.path.join(punkt_path, fname))
        print(f"Removed punkt model: {fname}")


# Remove non-English punkt-tab
for fname in os.listdir(punkt_tab_path):
    if fname not in keep_punkt_tab:
        os.remove(os.path.join(punkt_tab_path, fname))
        print(f"Removed punkt model: {fname}")

