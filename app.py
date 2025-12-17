from flask import Flask, render_template, request, jsonify
import pickle
import re
import spacy

app = Flask(__name__)

# --- Load trained model ---
with open("model.pkl", "rb") as f:
    vectorizer, model = pickle.load(f)

# --- Load spaCy NER model ---
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        text = data.get("news", "")
        if not text.strip():
            return jsonify({"error": "No news text provided"}), 400

        # Clean and vectorize
        cleaned_text = clean_text(text)
        X_vec = vectorizer.transform([cleaned_text])

        # Predict fake or real
        pred = model.predict(X_vec)[0]
        label = "REAL" if pred == 1 else "FAKE"

        # Named Entity Recognition
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        return jsonify({"prediction": label, "entities": entities})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Prediction failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

