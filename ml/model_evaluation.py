# model_evaluation.py

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    RocCurveDisplay
)

def main():
    # --- File paths ---
    model_path = "models/insurance_model.pkl"
    test_data_path = "data/safra_feature_engineered.csv"

    # --- Check files exist ---
    if not os.path.exists(model_path):
        print(f"Model file not found: {model_path}")
        return
    if not os.path.exists(test_data_path):
        print(f"Test data file not found: {test_data_path}")
        return

    # --- Load model and data ---
    print(" Loading model and test dataset...")
    model = joblib.load(model_path)
    df = pd.read_csv(test_data_path)

    # --- Ensure target column exists ---
    target_col = "Have you ever had health insurance?_binary"
    if target_col not in df.columns:
        print(f" Target column '{target_col}' not found in dataset.")
        return

    # --- Drop rows with missing values ---
    print("🧹 Dropping rows with missing values...")
    df = df.dropna(subset=[target_col])
    df = df.dropna()  # removes any remaining NaNs in features

    # --- Separate features and target ---
    X = df.drop(columns=[target_col])
    y_true = df[target_col]

    # --- Align features with model ---
    if hasattr(model, "feature_names_in_"):
        expected_features = model.feature_names_in_
        for col in expected_features:
            if col not in X.columns:
                X[col] = 0
        X = X[expected_features]
    else:
        print(" Model does not store feature names; using available columns.")

    # --- Make predictions ---
    print(" Evaluating model...")
    y_pred = model.predict(X)

    # --- Metrics ---
    acc = accuracy_score(y_true, y_pred)
    print(f"\n Model Accuracy: {acc:.4f}")

    print("\n Classification Report:")
    print(classification_report(y_true, y_pred))

    # --- Confusion Matrix ---
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.show()

    # --- ROC Curve ---
    if len(set(y_true)) == 2:
        try:
            RocCurveDisplay.from_estimator(model, X, y_true)
            plt.title("ROC Curve")
            plt.show()
            auc = roc_auc_score(y_true, model.predict_proba(X)[:, 1])
            print(f" ROC-AUC Score: {auc:.4f}")
        except Exception as e:
            print(f" Skipped ROC curve: {e}")

    print("\n Evaluation completed successfully.")

if __name__ == "__main__":
    main()
