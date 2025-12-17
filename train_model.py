import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import re

# --- Preprocessing ---
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# --- Load datasets ---
fake = pd.read_csv("fake.csv")
true = pd.read_csv("true.csv")

fake["label"] = 0  # Fake
true["label"] = 1  # Real

data = pd.concat([fake, true])
data["text"] = data["text"].apply(clean_text)

X = data["text"]
y = data["label"]

# --- TF-IDF ---
vectorizer = TfidfVectorizer(stop_words="english", max_features=20000, ngram_range=(1,3))
X_vec = vectorizer.fit_transform(X)

# --- Train Naive Bayes ---
model = MultinomialNB()
model.fit(X_vec, y)

# --- Save vectorizer + model ---
with open("model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)

print("Model trained and saved as model.pkl")
