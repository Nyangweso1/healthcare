#!/usr/bin/env python
"""
Comprehensive test to simulate form submission and prediction
"""
import sys
sys.path.insert(0, '.')

try:
    from ml.risk_engine import RiskAssessmentEngine
    
    # Simulate form data - as if submitted from the assess form
    form_data = {
        'age': '35',  # Form data is always strings
        'gender': 'Male',
        'marital_status': 'Married',
        'employment_status': 'Employed',
        'income': '50000',
        'children': '2',
        'education_level': 'College/University',
        'residence_type': 'Urban',
        'chronic_illness': 'No',
        'family_size': '4',
        'healthcare_knowledge': 'Moderate',
        'hospital_visit_gap': '6',
        'routine_check': '1',
        'cancer_screening': '0',
        'dental_checkup': '0',
        'mental_health_support': '0'
    }
    
    # Convert to the format app.py uses
    user_data = {
        'Age': int(form_data['age']),
        'Gender': form_data['gender'],
        'Marital Status': form_data['marital_status'],
        'Employment Status': form_data['employment_status'],
        'Monthly Household Income': float(form_data['income']),
        'num_children': int(form_data['children']),
        'education_level': form_data['education_level'],
        'residence_type': form_data['residence_type'],
        'chronic_illness': form_data['chronic_illness'],
        'family_size': int(form_data['family_size']),
        'healthcare_knowledge': form_data['healthcare_knowledge'],
        'hospital_visit_gap': float(form_data['hospital_visit_gap']),
        'routine_check': int(form_data['routine_check']),
        'cancer_screening': int(form_data['cancer_screening']),
        'dental_checkup': int(form_data['dental_checkup']),
        'mental_health_support': int(form_data['mental_health_support'])
    }
    
    # Calculate preventive care score (as app.py does)
    user_data['preventive_care_score'] = (
        user_data['routine_check'] + 
        user_data['cancer_screening'] + 
        user_data['dental_checkup'] + 
        user_data['mental_health_support']
    )
    
    print('✓ Form data converted successfully')
    print(f'User data: {user_data}')
    
    # Initialize engine
    engine = RiskAssessmentEngine(model_path="models/insurance_risk_model.pkl")
    print('✓ Engine initialized')
    
    # Make prediction
    result = engine.predict_risk(user_data)
    print('✓ Prediction completed')
    
    # Check result
    print('\n=== RESULTS ===')
    print(f'Insurance Likelihood: {result.get("insurance_likelihood")}%')
    print(f'Risk Level: {result.get("risk_level")}')
    print(f'Probability: {result.get("probability")}%')
    print(f'Interpretation: {result.get("interpretation")}')
    print(f'Rule-based Score: {result.get("rule_based_score")}/100')
    print(f'Rule-based Category: {result.get("rule_based_category")}')
    
    if result.get('error'):
        print(f'ERROR: {result.get("error")}')
    
    # Verify all required keys exist
    required_keys = ['insurance_likelihood', 'risk_level', 'probability', 'interpretation', 
                     'eligible_insurance', 'recommendations', 'reasons', 'rule_based_score', 'rule_based_category']
    missing_keys = [k for k in required_keys if k not in result]
    if missing_keys:
        print(f'\n⚠ Missing keys: {missing_keys}')
    else:
        print('\n✓ All required keys present')
    
except Exception as e:
    print(f'✗ Test failed: {e}')
    import traceback
    traceback.print_exc()
