#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

try:
    from ml.risk_engine import RiskAssessmentEngine
    
    # Create engine
    engine = RiskAssessmentEngine(model_path="models/insurance_risk_model.pkl")
    print('✓ Engine initialized')
    
    # Test with sample user data
    user_data = {
        'Age': 35,
        'Gender': 'Male',
        'Marital Status': 'Married',
        'Employment Status': 'Employed',
        'Monthly Household Income': 50000,
        'num_children': 2,
        'education_level': 'Tertiary',
        'residence_type': 'Urban',
        'chronic_illness': 'No',
        'family_size': 4,
        'healthcare_knowledge': 'Moderate',
        'hospital_visit_gap': 12,
        'routine_check': 1,
        'cancer_screening': 0,
        'dental_checkup': 0,
        'mental_health_support': 0,
        'preventive_care_score': 1
    }
    
    print('✓ User data prepared')
    
    # Test prepare_input
    input_df = engine.prepare_input(user_data)
    if input_df is None:
        print('✗ prepare_input returned None')
    else:
        print(f'✓ Input prepared, shape: {input_df.shape}')
        print(f'Number of non-zero values: {(input_df != 0).sum().sum()}')
    
    # Test predict_risk
    print('\nTesting predict_risk...')
    result = engine.predict_risk(user_data)
    print('✓ Prediction completed')
    print(f'Result keys: {result.keys()}')
    print(f'insurance_likelihood: {result.get("insurance_likelihood")}')
    print(f'risk_level: {result.get("risk_level")}')
    if result.get('error'):
        print(f'Error: {result.get("error")}')
    
except Exception as e:
    print(f'✗ Error: {e}')
    import traceback
    traceback.print_exc()
