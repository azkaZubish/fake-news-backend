
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
from db import predictions_collection


model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

app = Flask(__name__)
CORS(app,origins=[
    "http://localhost:5173",
    "https://fake-news-detection-rosy-seven.vercel.app"
])

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def keyword_analysis(text):
    fake_keywords = ["breaking", "shocking", "secret", "exposed", "viral", "leaked"]
    real_keywords = ["official", "confirmed", "announced", "report"]

    text_lower = text.lower()

    fake_matches = [w for w in fake_keywords if w in text_lower]
    real_matches = [w for w in real_keywords if w in text_lower]

    return {
        "fake_score": len(fake_matches),
        "real_score": len(real_matches),
        "fake_keywords": fake_matches,
        "real_keywords": real_matches
    }

def predict_news(text):
    clean = clean_text(text)
    vector = vectorizer.transform([clean])

    pred = model.predict(vector)[0]

    # confidence (basic simulation if model doesn't provide prob)
    try:
        prob = model.predict_proba(vector)[0]
        confidence = max(prob)
    except:
        confidence = 0.75  # fallback

    keyword_data = keyword_analysis(text)

    word_len = len(text.split())

    # Rule-based override
    if word_len < 20:
        if keyword_data["fake_score"] >= 2:
            prediction = "Fake News"
        elif keyword_data["real_score"] >= 2:
            prediction = "Real News"
        else:
            prediction = "Uncertain News"
    else:
        prediction = "Real News" if pred == 1 else "Fake News"

    return {
        "prediction": prediction,
        "confidence": round(confidence * 100, 2),
        "word_count": word_len,
        "analysis": keyword_data
    }

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No input provided"}), 400

        result = predict_news(text)
        print(result)

        try:
            predictions_collection.insert_one({
            "news_text": text,
            "prediction": result["prediction"],
            "confidence": float(result["confidence"])
            })
        except Exception as e:
            print("MongoDB insert failed:", e)

        return jsonify(result)
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/history')
def history():
    predictions = list(predictions_collection.find({}, {"_id" : 0}))

    return jsonify(predictions)


@app.route('/')
def home():
    return "Backend is running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # app.run(debug=True)


#making the backend live
# from pyngrok import ngrok
# ngrok.set_auth_token("3BDxsBdE6fOlWPhbp0UNyV8uWS9_2Na3YbeYyhQZAbJt7qtCS")
# if __name__ == "__main__":
    # public_url = ngrok.connect(5000)
    # print("Public URL:", public_url)

    # app.run(port=5000, debug=False)