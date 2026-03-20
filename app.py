
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re


# 🔥 Load model + vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

app = Flask(__name__)
CORS(app) # 🔥 allows React to connect

# 🔧 Clean text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

# 🔧 Keyword logic
def keyword_score(text):
    fake_keywords = ["breaking", "shocking", "secret", "exposed", "viral", "leaked"]
    real_keywords = ["official", "confirmed", "announced", "report"]

    text = text.lower()

    fake_score = sum(1 for w in fake_keywords if w in text)
    real_score = sum(1 for w in real_keywords if w in text)

    return fake_score, real_score

# 🔥 Prediction logic
def predict_news(text):

    clean = clean_text(text)

    vector = vectorizer.transform([clean])
    pred = model.predict(vector)[0]

    fake_score, real_score = keyword_score(text)

    word_len = len(text.split())

    if word_len < 20:
        if fake_score >= 2:
            return "Fake News"
        elif real_score >= 2:
            return "Real News"
        else:
            return "Uncertain News"

    return "Real News" if pred == 1 else "Fake News"

# 🚀 API route
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No input provided"}), 400

    result = predict_news(text)

    return jsonify({
        "prediction": result
    })

# # 🟢 Run server
# if __name__ == "__main__":
#     app.run(debug=True)

#making the backend live
from pyngrok import ngrok
ngrok.set_auth_token("3BDxsBdE6fOlWPhbp0UNyV8uWS9_2Na3YbeYyhQZAbJt7qtCS")
if __name__ == "__main__":
    public_url = ngrok.connect(5000)
    print("Public URL:", public_url)

    app.run(port=5000, debug=False)