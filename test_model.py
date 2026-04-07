#!/usr/bin/env python3
"""
Simple test script to verify the model loads correctly.
Run this to diagnose why assessments return 0.0 values.

Usage: python test_model.py
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_model_initialization():
    """Test if the model initializes correctly."""
    print("=" * 60)
    print("MODEL DIAGNOSTIC TEST")
    print("=" * 60)
    print()
    
    # Check if files exist
    base_dir = project_root
    model_path = os.path.join(base_dir, "models", "insurance_risk_model.pkl")
    features_path = os.path.join(base_dir, "models", "insurance_risk_model_features.pkl")
    
    print(f"Base directory: {base_dir}")
    print(f"Model path: {model_path}")
    print(f"  - Exists: {os.path.exists(model_path)}")
    print(f"  - Size: {os.path.getsize(model_path) / 1024 / 1024:.2f} MB" if os.path.exists(model_path) else "  - N/A")
    print()
    print(f"Features path: {features_path}")
    print(f"  - Exists: {os.path.exists(features_path)}")
    print(f"  - Size: {os.path.getsize(features_path) / 1024:.2f} KB" if os.path.exists(features_path) else "  - N/A")
    print()
    
    # List models directory
    models_dir = os.path.join(base_dir, "models")
    print(f"Files in {models_dir}/:")
    if os.path.exists(models_dir):
        for file in os.listdir(models_dir):
            file_path = os.path.join(models_dir, file)
            size = os.path.getsize(file_path)
            size_str = f"{size / 1024 / 1024:.2f} MB" if size > 1024 * 1024 else f"{size / 1024:.2f} KB"
            print(f"  - {file} ({size_str})")
    else:
        print("  [Directory not found]")
    print()
    
    # Try to initialize the risk engine
    print("Attempting to initialize RiskAssessmentEngine...")
    try:
        from ml.risk_engine import RiskAssessmentEngine
        
        engine = RiskAssessmentEngine(model_path=model_path)
        print("✓ Model initialized successfully!")
        print()
        
        # Test with sample data
        print("Testing with sample user data...")
        sample_data = {
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
        
        result = engine.predict_risk(sample_data)
        
        print(f"Risk Level: {result.get('risk_level')}")
        print(f"Probability (uninsured): {result.get('probability')}%")
        print(f"Insurance Likelihood: {result.get('insurance_likelihood')}%")
        print()
        
        if result.get('probability') == 0.0 and result.get('insurance_likelihood') == 0.0:
            print("⚠ WARNING: Model returned 0% for both metrics!")
            print("This indicates the model prediction failed.")
            if 'error' in result:
                print(f"Error: {result.get('error')}")
        else:
            print("✓ Model appears to be working correctly!")
        
    except ImportError as e:
        print(f"✗ Failed to import RiskAssessmentEngine: {e}")
    except FileNotFoundError as e:
        print(f"✗ Model file not found: {e}")
    except Exception as e:
        print(f"✗ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)

if __name__ == '__main__':
    test_model_initialization()
