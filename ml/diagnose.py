
import os
import sys

print("=" * 60)
print("HEALTHCARE SYSTEM DIAGNOSTIC CHECK")
print("=" * 60)

# Check 1: Virtual Environment
print("\n[1] Virtual Environment:")
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("    ✓ Virtual environment is active")
else:
    print("    ✗ Virtual environment NOT active")
    print("    → Run: venv\\Scripts\\activate")

# Check 2: Python Version
print("\n[2] Python Version:")
print(f"    Python {sys.version}")
if sys.version_info >= (3, 11):
    print("    ✓ Python version is compatible")
else:
    print("    ⚠ Python 3.11+ recommended")

# Check 3: Required Files
print("\n[3] Required Files:")
files = {
    'data/Healthcare Dataset.xlsx': 'Source data',
    'data/healthcare_clean.csv': 'Processed data',
    'models/insurance_risk_model.pkl': 'Trained model',
    'models/insurance_risk_model_features.pkl': 'Feature names',
    'app.py': 'Flask application',
    'risk_engine.py': 'Risk engine',
    'data_preprocessing.py': 'Preprocessing script',
    'model_training.py': 'Training script',
    'requirements.txt': 'Dependencies list'
}

missing_files = []
for filepath, description in files.items():
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"    ✓ {description}: {filepath} ({size:,} bytes)")
    else:
        print(f"    ✗ MISSING {description}: {filepath}")
        missing_files.append(filepath)

# Check 4: Python Packages
print("\n[4] Required Packages:")
packages = {
    'flask': 'Flask',
    'pandas': 'pandas',
    'numpy': 'numpy', 
    'sklearn': 'scikit-learn',
    'joblib': 'joblib',
    'werkzeug': 'werkzeug',
    'openpyxl': 'openpyxl'
}

missing_packages = []
for module, name in packages.items():
    try:
        pkg = __import__(module)
        version = getattr(pkg, '__version__', 'unknown')
        print(f"    ✓ {name}: {version}")
    except ImportError:
        print(f"    ✗ {name} NOT installed")
        missing_packages.append(name)

# Check 5: Import Tests
print("\n[5] Component Import Tests:")
try:
    from risk_engine import RiskAssessmentEngine
    print("    ✓ risk_engine imports successfully")
    
    # Try to initialize
    try:
        engine = RiskAssessmentEngine()
        print("    ✓ RiskAssessmentEngine initializes successfully")
    except Exception as e:
        print(f"    ⚠ RiskAssessmentEngine initialization warning: {e}")
        
except Exception as e:
    print(f"    ✗ risk_engine import failed: {e}")

try:
    import app
    print("    ✓ app module imports successfully")
except Exception as e:
    print(f"    ✗ app import failed: {e}")

# Check 6: Database
print("\n[6] Database Check:")
if os.path.exists('instance/users.db'):
    size = os.path.getsize('instance/users.db')
    print(f"    ✓ Database exists: instance/users.db ({size:,} bytes)")
else:
    print("    ⚠ Database not found (will be created on first run)")

# Check 7: Templates
print("\n[7] Template Files:")
required_templates = ['index.html', 'home.html', 'login.html', 'register.html', 
                      'assess.html', 'results.html', '404.html', '500.html']
if os.path.exists('templates'):
    templates = os.listdir('templates')
    for template in required_templates:
        if template in templates:
            print(f"    ✓ {template}")
        else:
            print(f"    ✗ MISSING: {template}")
else:
    print("    ✗ templates/ folder not found!")

# Summary
print("\n" + "=" * 60)
print("DIAGNOSTIC SUMMARY")
print("=" * 60)

issues = []
if missing_files:
    issues.append(f"Missing files: {', '.join(missing_files)}")
if missing_packages:
    issues.append(f"Missing packages: {', '.join(missing_packages)}")

if not issues:
    print("✓ ALL CHECKS PASSED - System is ready!")
    print("\nTo start the application:")
    print("  python app.py")
    print("\nThen open: http://localhost:5000")
else:
    print("✗ ISSUES FOUND:")
    for issue in issues:
        print(f"  - {issue}")
    print("\nRecommended Actions:")
    if missing_packages:
        print("  1. pip install -r requirements.txt")
    if 'data/healthcare_clean.csv' in missing_files:
        print("  2. python data_preprocessing.py")
    if 'models/insurance_risk_model.pkl' in missing_files:
        print("  3. python model_training.py")

print("=" * 60)
