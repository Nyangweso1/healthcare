#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

try:
    import joblib
    import pandas as pd
    
    # Load model and features
    model = joblib.load('models/insurance_risk_model.pkl')
    features = joblib.load('models/insurance_risk_model_features.pkl')
    
    print('✓ Model loaded successfully')
    print('✓ Features loaded successfully')
    print(f'Number of features: {len(features)}')
    print(f'Model type: {type(model).__name__}')
    print(f'Model classes: {getattr(model, "classes_", "N/A")}')
    
    # Create a sample input
    input_df = pd.DataFrame(0, index=[0], columns=features)
    print('✓ Input DataFrame created')
    
    # Try to make a prediction
    proba = model.predict_proba(input_df)
    print('✓ Prediction successful!')
    print(f'Prediction shape: {proba.shape}')
    print(f'Prediction values: {proba}')
    
except Exception as e:
    print(f'✗ Error: {e}')
    import traceback
    traceback.print_exc()
