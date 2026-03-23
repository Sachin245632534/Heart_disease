import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
from tensorflow.keras.models import load_model


# -----------------------------
# FILE PATHS
# -----------------------------


DATA_PATH = "/Users/sachin/digital_twin/new_dataset.csv"
RF_PATH = "/Users/sachin/digital_twin/model/random_forest.pkl"
ANN_PATH = "/Users/sachin/digital_twin/model/ann_model.h5"
SCALER_PATH = "/Users/sachin/digital_twin/model/scaler.pkl"


# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv(DATA_PATH)

X = df.drop("target_binary", axis=1)
y = df["target_binary"]

print("Dataset loaded:", X.shape)


# -----------------------------
# LOAD MODELS
# -----------------------------

rf_model = joblib.load(RF_PATH)
ann_model = load_model(ANN_PATH)
scaler = joblib.load(SCALER_PATH)

print("Models loaded successfully")


# -----------------------------
# RANDOM FOREST PREDICTION
# -----------------------------

rf_probs = rf_model.predict_proba(X)[:,1]
rf_pred = (rf_probs > 0.5).astype(int)

print("\n===== RANDOM FOREST RESULTS =====")

print("Accuracy:", accuracy_score(y, rf_pred))
print("Precision:", precision_score(y, rf_pred))
print("Recall:", recall_score(y, rf_pred))
print("F1 Score:", f1_score(y, rf_pred))
print("ROC-AUC:", roc_auc_score(y, rf_probs))

print("\nConfusion Matrix:")
print(confusion_matrix(y, rf_pred))


# -----------------------------
# ANN PREDICTION
# -----------------------------

X_scaled = scaler.transform(X)

ann_probs = ann_model.predict(X_scaled).flatten()
ann_pred = (ann_probs > 0.5).astype(int)

print("\n===== ANN RESULTS =====")

print("Accuracy:", accuracy_score(y, ann_pred))
print("Precision:", precision_score(y, ann_pred))
print("Recall:", recall_score(y, ann_pred))
print("F1 Score:", f1_score(y, ann_pred))
print("ROC-AUC:", roc_auc_score(y, ann_probs))

print("\nConfusion Matrix:")
print(confusion_matrix(y, ann_pred))











