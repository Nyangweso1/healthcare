#!/usr/bin/env python
import joblib
import pandas as pd
import numpy as np

# Load model and features
model = joblib.load('models/insurance_risk_model.pkl')
features = joblib.load('models/insurance_risk_model_features.pkl')

# Create a sample input
input_df = pd.DataFrame(0, index=[0], columns=features)

# Try to make a prediction
print('Model type:', type(model))
print('Number of features:', len(features))
print('Model classes:', getattr(model, 'classes_', 'No classes attr'))

try:
    proba = model.predict_proba(input_df)
    print('Prediction successful!')
    print('Proba shape:', proba.shape)
    print('Proba:', proba)
except Exception as e:
    print('Error:', e)
    import traceback
    traceback.print_exc()
