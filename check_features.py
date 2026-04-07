from ml.risk_engine import RiskAssessmentEngine
import os

model_path = os.path.join(os.getcwd(), 'models', 'insurance_risk_model.pkl')
engine = RiskAssessmentEngine(model_path=model_path)

# Show all employment status features
employment_features = [f for f in engine.feature_names if 'Employment' in f]
print('Employment Status features in model:')
for f in employment_features:
    print(f'  - {f}')

# Show gender features
print('\nGender features in model:')
gender_features = [f for f in engine.feature_names if 'Gender' in f]
for f in gender_features:
    print(f'  - {f}')

# Show marital status features
print('\nMarital Status features in model:')
marital_features = [f for f in engine.feature_names if 'Marital' in f]
for f in marital_features:
    print(f'  - {f}')
