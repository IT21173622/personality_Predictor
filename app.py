"""
Personality Predictor API
Predicts Introvert / Extrovert based on behavioral characteristics.
"""

from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load model once at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), "personality_model.pkl")
model = joblib.load(MODEL_PATH)

REQUIRED_FIELDS = [
    "Time_spent_Alone",
    "Stage_fear",
    "Social_event_attendance",
    "Going_outside",
    "Drained_after_socializing",
    "Friends_circle_size",
    "Post_frequency",
]


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Personality Predictor API",
        "version": "1.0",
        "endpoints": {
            "POST /predict": "Predict introvert or extrovert",
            "GET /health": "Health check",
        },
        "example_request": {
            "Time_spent_Alone": 8,
            "Stage_fear": "Yes",
            "Social_event_attendance": 1,
            "Going_outside": 2,
            "Drained_after_socializing": "Yes",
            "Friends_circle_size": 3,
            "Post_frequency": 2,
        },
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model_loaded": model is not None})


@app.route("/predict", methods=["POST"])
def predict():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON (Content-Type: application/json)"}), 400

    data = request.get_json()

    # Validate required fields (allow missing values — model handles imputation)
    unknown = [k for k in data if k not in REQUIRED_FIELDS]
    if unknown:
        return jsonify({"error": f"Unknown fields: {unknown}. Accepted: {REQUIRED_FIELDS}"}), 400

    try:
        input_df = pd.DataFrame([{field: data.get(field) for field in REQUIRED_FIELDS}])

        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]

        label = "Extrovert" if prediction == 1 else "Introvert"
        confidence = float(max(probabilities))

        return jsonify({
            "personality": label,
            "confidence": round(confidence, 4),
            "probabilities": {
                "Introvert": round(float(probabilities[0]), 4),
                "Extrovert": round(float(probabilities[1]), 4),
            },
        })

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
