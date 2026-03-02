# predict.py
import os
import pandas as pd
import joblib

def main():
    model_path = "models/insurance_model.pkl"
    data_path = "data/safra_feature_engineered.csv"

    # --- Check files ---
    if not os.path.exists(model_path):
        print(f" Model file not found: {model_path}")
        return
    if not os.path.exists(data_path):
        print(f" Data file not found: {data_path}")
        return

    # --- Load model ---
    print(" Loading trained model...")
    model = joblib.load(model_path)

    # --- Load new data ---
    print(" Loading new data for prediction...")
    df = pd.read_csv(data_path)
    print(f"Data loaded successfully with shape: {df.shape}")

    # --- Clean columns ---
    # Drop target column if it exists
    if 'Have you ever had health insurance?_binary' in df.columns:
        df = df.drop(columns=['Have you ever had health insurance?_binary'])
        print("🧹 Dropped target column from new data.")

    # --- Align columns with model ---
    if hasattr(model, "feature_names_in_"):
        expected_features = model.feature_names_in_
        # Add missing columns with 0
        for col in expected_features:
            if col not in df.columns:
                df[col] = 0
        # Drop any extra columns not used in training
        df = df[expected_features]
        print(f" Data aligned to model features: {len(expected_features)} columns.")
    else:
        print(" Model does not store feature names. Proceeding with current columns...")

    # --- Make predictions ---
    print(" Making predictions...")
    predictions = model.predict(df)

    # --- Save results ---
    df['Predicted_Has_Insurance'] = predictions
    output_path = "data/predictions_output.csv"
    df.to_csv(output_path, index=False)

    print(f" Predictions completed and saved to: {output_path}")
    print(df.head())

if __name__ == "__main__":
    main()
