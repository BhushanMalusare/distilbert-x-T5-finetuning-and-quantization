import config
from flask import Flask, jsonify, request
import os 
from model import get_class_names, predict_intent, summarize_text

app = Flask(__name__)

# Endpoint to inference for intent recognition
@app.route("/predict-intent", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text")
    if text:
        predicted_class = predict_intent(text)
        if predicted_class:
            return jsonify({"class": predicted_class}), 200
        else:
            return jsonify({"class": "Transformer is unsure about the intent."}), 200
    else:
        return jsonify({"error": "No text provided"}), 400

# End point to return classes of distilbert model
@app.route("/classes", methods=["GET"])
def classes():
    class_names = get_class_names()
    return jsonify({"classes": class_names}), 200

# End point to generate summary of input text
@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text")
    if text:
        summary = summarize_text(text)
        return jsonify({"summary": summary}), 200
    else:
        return jsonify({"error": "No text provided"}), 400

if __name__ == "__main__":
    app.run(debug=True)
