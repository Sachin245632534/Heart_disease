from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import os
import joblib
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

# -----------------------------
# MODEL PATHS
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RF_PATH = os.path.join(BASE_DIR, "model", "random_forest.pkl")
ANN_PATH = os.path.join(BASE_DIR, "model", "ann_model.h5")
SCALER_PATH = os.path.join(BASE_DIR, "model", "scaler.pkl")

rf_model = None
ann_model = None
scaler = None


# -----------------------------
# LOAD MODELS
# -----------------------------

try:
    if os.path.exists(RF_PATH):
        rf_model = joblib.load(RF_PATH)
        print("Random Forest loaded")
except Exception as e:
    print("RF load error:", e)

try:
    if os.path.exists(ANN_PATH):
        ann_model = load_model(ANN_PATH)
        print("ANN model loaded")
except Exception as e:
    print("ANN load error:", e)

try:
    if os.path.exists(SCALER_PATH):
        scaler = joblib.load(SCALER_PATH)
        print("Scaler loaded")
except Exception as e:
    print("Scaler load error:", e)


# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# PREDICTION ROUTE
# -----------------------------

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    try:
        features = np.array([[
            data["age"],
            data["sex"],
            data["cp"],
            data["trestbps"],
            data["chol"],
            data["fbs"],
            data["thalach"],
            data["exang"],
            data["oldpeak"],
            data["slope"],
            data["ca"],
            data["thal"]
        ]], dtype=float)

        model_name = "Unknown"
        prob = 0.0

        # Random Forest
        if data["model"] == "rf" and rf_model is not None:
            prob = rf_model.predict_proba(features)[0][1]
            model_name = "Random Forest"

        # ANN
        elif data["model"] == "ann" and ann_model is not None:
            if scaler is not None:
                features = scaler.transform(features)

            prob = float(ann_model.predict(features)[0][0])
            model_name = "Artificial Neural Network"

        else:
            return jsonify({"error": "Model not available"}), 500

        prediction = 1 if prob > 0.5 else 0

        return jsonify({
            "risk": float(prob),
            "target_binary": prediction,
            "model": model_name
        })

    except Exception as e:
        print("Prediction error:", e)
        return jsonify({"error": "Prediction failed"}), 500


# -----------------------------
# RUN SERVER
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)