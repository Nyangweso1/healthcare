from ml.risk_engine import RiskAssessmentEngine
import os

model_path = os.path.join(os.getcwd(), 'models', 'insurance_risk_model.pkl')
engine = RiskAssessmentEngine(model_path=model_path)

# Test with sample data
test_data = {
    'Age': 35,
    'Gender': 'Male',
    'Marital Status': 'Married',
    'Employment Status': 'Employed',
    'Monthly Household Income': 45000,
    'num_children': 2,
    'education_level': 'Secondary',
    'residence_type': 'Urban',
    'chronic_illness': 'None',
    'family_size': 4,
    'healthcare_knowledge': 'Good',
    'hospital_visit_gap': 6,
    'routine_check': 1,
    'cancer_screening': 0,
    'dental_checkup': 1,
    'mental_health_support': 0
}

result = engine.predict_risk(test_data)
print(f'Risk Level: {result.get("risk_level")}')
print(f'Probability (uninsured): {result.get("probability")}%')
print(f'Insurance Likelihood: {result.get("insurance_likelihood")}%')
print(f'Rule Based Score: {result.get("rule_based_score")}')
if result.get("probability") == 0.0:
    print("WARNING: Result is 0%!")
