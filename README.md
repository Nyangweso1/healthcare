# Healthcare Insurance Risk Prediction System

##  Project Overview

The **Healthcare Insurance Risk Prediction System** is an intelligent web-based application that predicts whether individuals are at risk of being uninsured based on their demographic, socioeconomic, and healthcare access patterns. The system provides actionable recommendations to help vulnerable populations access affordable health insurance.

**Developed by:** Prudence  
**Date:** January 3, 2026  
**Institution:** [Your Institution]  
**Target:** Academic Project & Real-world Application

---

##  Problem Statement

In many regions, particularly rural and low-income communities, individuals face significant barriers to accessing health insurance. This leads to:

- **Financial vulnerability** during medical emergencies
- **Delayed healthcare** due to cost concerns
- **Poor health outcomes** from lack of preventive care
- **Economic burden** on families and communities

### The Challenge

How can we identify individuals at highest risk of being uninsured **before** they need medical care, and provide them with targeted interventions to secure coverage?

---

##  Solution

Our system uses **machine learning** to:

1. **Predict insurance risk** based on:
   - Demographic factors (age, gender, marital status)
   - Socioeconomic indicators (income, employment, family size)
   - Healthcare access behaviors (hospital visits, preventive care)

2. **Classify risk levels**:
   - **Low Risk** (< 30% probability of being uninsured)
   - **Medium Risk** (30-60%)
   - **High Risk** (> 60%)

3. **Provide personalized recommendations**:
   - NHIF enrollment guidance
   - Subsidized insurance programs
   - Community-based health insurance
   - Preventive care education

---

##  Dataset Description

### Source
- **Survey Data**: Healthcare access survey from [Region/Country]
- **Sample Size**: [Number] respondents
- **Collection Period**: [Date Range]

### Key Features

#### Target Variable
- **Have you ever had health insurance?**
  - `Yes` → 1 (insured)
  - `No` → 0 (uninsured - HIGH RISK)

#### Input Features

**Demographics:**
- Age
- Gender  
- Marital Status
- Number of Children

**Socioeconomic:**
- Monthly Household Income
- Employment Status

**Healthcare Access:**
- When was the last time you visited a hospital?
- Have you ever had a routine check-up?
- Have you ever had a cancer screening?
- Did you have insurance during your last hospital visit?

#### Engineered Features
- `hospital_visit_gap`: Months since last hospital visit
- `preventive_care_score`: Sum of routine checkups + cancer screening (0-2)
- `age_group`: Categorical age buckets (18-25, 26-35, 36-50, 50+)
- `income_bucket`: Income categories (Low, Medium, High, Very High)
- `num_children`: Numeric count of dependents

---

##  Machine Learning Approach

### Model Selection

We use **interpretable models** suitable for academic and policy applications:

1. **Logistic Regression**
   - Linear model with clear coefficient interpretation
   - Shows which factors increase/decrease risk
   - Best for reporting to stakeholders

2. **Decision Tree (max_depth=5)**
   - Rule-based predictions
   - Easy to visualize decision paths
   - Captures non-linear relationships

### Training Pipeline

```
1. Data Preprocessing
   ├── Load Excel dataset
   ├── Drop metadata columns
   ├── Handle missing values (median/mode imputation)
   ├── Create binary target variable
   ├── Engineer features
   └── One-hot encode categoricals

2. Model Training
   ├── Split data (80% train, 20% test)
   ├── Train Logistic Regression
   ├── Train Decision Tree
   ├── Evaluate both models
   └── Select best based on F1-Score

3. Model Evaluation
   ├── Accuracy
   ├── Precision (avoid false alarms)
   ├── Recall (catch high-risk individuals)
   ├── F1-Score (balance precision & recall)
   └── Confusion Matrix

4. Feature Importance
   ├── Logistic Regression coefficients
   └── Decision Tree feature importance
```

### Key Findings (Example)

Based on model analysis, **strongest predictors** of insurance risk include:

1. **Monthly Household Income** (strongest factor)
2. **Employment Status** (unemployed = higher risk)
3. **Preventive Care Score** (no checkups = higher risk)
4. **Number of Children** (larger families = higher risk)
5. **Hospital Visit Gap** (long time since visit = higher risk)

---

##  System Architecture

### Technology Stack

**Backend:**
- Python 3.11+
- Flask (Web Framework)
- SQLite (User Authentication)
- scikit-learn (ML Models)

**Frontend:**
- HTML5 / CSS3
- Bootstrap 5 (Responsive Design)
- JavaScript (Form Validation)

**Machine Learning:**
- pandas (Data Processing)
- NumPy (Numerical Operations)
- scikit-learn (Model Training & Evaluation)
- joblib (Model Serialization)

### System Flow

```
User Registration/Login
        ↓
Risk Assessment Form
        ↓
User Input Collection
  (Demographics, Income, Healthcare History)
        ↓
Data Preprocessing
  (Feature Engineering, Encoding)
        ↓
ML Model Prediction
  (Probability of Being Uninsured)
        ↓
Risk Classification
  (Low / Medium / High)
        ↓
Risk Factor Identification
        ↓
Recommendation Generation
        ↓
Results Display
  (Risk Level, Probability, Reasons, Actions)
```

### File Structure

```
healthcare_prediction_system/
│
├── app.py                          # Flask web application
├── data_preprocessing.py           # Data cleaning & feature engineering
├── model_training.py               # Train ML models
├── risk_engine.py                  # Risk assessment logic
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── data/
│   ├── Healthcare Dataset.xlsx    # Original survey data
│   └── healthcare_clean.csv       # Processed data for training
│
├── models/
│   ├── insurance_risk_model.pkl   # Trained ML model
│   └── insurance_risk_model_features.pkl  # Feature names
│
├── templates/
│   ├── index.html                 # Landing page
│   ├── home.html                  # Home page
│   ├── register.html              # User registration
│   ├── login.html                 # User login
│   ├── assess.html                # Risk assessment form
│   ├── results.html               # Results display
│   └── [other pages...]
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
└── instance/
    └── users.db                   # SQLite database
```

---

##  Installation & Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Installation

#### 1. Clone or Download the Project

```bash
cd healthcare_prediction_system
```

#### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Prepare the Data

**Ensure you have the dataset:**
- Place `Healthcare Dataset.xlsx` in the `data/` folder

#### 5. Run Data Preprocessing

```bash
python data_preprocessing.py
```

**Expected Output:**
- Creates `data/healthcare_clean.csv`
- Displays data cleaning statistics
- Shows target variable distribution

#### 6. Train the Model

```bash
python model_training.py
```

**Expected Output:**
- Creates `models/insurance_risk_model.pkl`
- Creates `models/insurance_risk_model_features.pkl`
- Displays model performance metrics
- Shows feature importance

#### 7. Test the Risk Engine (Optional)

```bash
python risk_engine.py
```

This runs a test prediction with sample data.

---

##  Running the System

### Start the Web Application

```bash
python app.py
```

**Expected Output:**
```
INFO: Starting Healthcare Insurance Risk Prediction System
INFO: ✓ Risk Assessment Engine initialized
INFO: ✓ Database initialized
* Running on http://0.0.0.0:5000
```

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

### Using the System

1. **Register** a new account (or use existing)
2. **Login** with your credentials
3. Navigate to **Risk Assessment**
4. Fill in the assessment form:
   - Demographics (age, gender, marital status)
   - Socioeconomic info (employment, income, children)
   - Healthcare access (last visit, checkups, screenings)
5. Click **"Assess My Risk"**
6. View your results:
   - Risk level (Low/Medium/High)
   - Probability of being uninsured
   - Key risk factors
   - Personalized recommendations

---

##  Model Performance

### Evaluation Metrics (Example)

| Model                | Accuracy | Precision | Recall | F1-Score |
|---------------------|----------|-----------|--------|----------|
| Logistic Regression | 0.8234   | 0.7891    | 0.8456 | 0.8163   |
| Decision Tree       | 0.7956   | 0.7634    | 0.8123 | 0.7871   |

**Best Model:** Logistic Regression (F1-Score: 0.8163)

### Confusion Matrix

```
                  Predicted
                  0     1
Actual  0       [TN]  [FP]
        1       [FN]  [TP]
```

Where:
- **TN** (True Negative): Correctly predicted insured
- **FP** (False Positive): Predicted uninsured but actually insured
- **FN** (False Negative): Predicted insured but actually uninsured ⚠️ *Most critical to minimize*
- **TP** (True Positive): Correctly predicted uninsured

---

##  Ethical Considerations

### Data Privacy
- User data is stored securely in SQLite database
- Passwords are hashed using industry-standard algorithms
- No sensitive health data is permanently stored
- Complies with data protection regulations

### Bias Mitigation
- Model trained on diverse demographic groups
- Regular audits for fairness across age, gender, income
- Transparent feature importance reporting
- Clear explanation of predictions

### Responsible Use
- **This system is a decision-support tool, not a diagnostic system**
- Predictions should be used to identify at-risk individuals for outreach
- Should not be used to deny services or discriminate
- Human oversight and expert judgment remain essential

### Limitations
- Model accuracy depends on training data quality
- May not generalize to significantly different populations
- Requires periodic retraining with updated data
- Cannot account for all individual circumstances

---

##  Future Improvements

### Short-term (3-6 months)
- [ ] Add data visualization dashboard
- [ ] Implement assessment history tracking
- [ ] Export results to PDF
- [ ] Multi-language support (Swahili, local languages)
- [ ] Mobile-responsive enhancements

### Medium-term (6-12 months)
- [ ] Integration with NHIF database (API)
- [ ] SMS/email notifications for high-risk individuals
- [ ] Geographic heat maps of insurance risk
- [ ] Batch assessment for community health workers
- [ ] Advanced models (Random Forest, XGBoost)

### Long-term (1-2 years)
- [ ] Real-time model retraining pipeline
- [ ] Integration with hospital management systems
- [ ] Predictive analytics for policy makers
- [ ] Mobile application (Android/iOS)
- [ ] AI chatbot for insurance guidance

---

##  Contributing

This is an academic project, but contributions are welcome!

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

##  Contact & Support

**Developer:** Prudence  
**Email:** [Your Email]  
**Institution:** [Your Institution]  
**Project Repository:** [GitHub/GitLab URL]

For questions, issues, or collaboration inquiries, please contact via email or open an issue in the repository.

---

##  License

This project is developed for academic purposes.

---

##  Acknowledgments

- Healthcare survey data contributors
- Open-source community (scikit-learn, Flask, Bootstrap)
- Academic advisors and reviewers
- All individuals working toward universal health coverage

---

##  References

1. World Health Organization. (2023). Universal Health Coverage.
2. Scikit-learn Documentation. (2024). Machine Learning in Python.
3. Flask Documentation. (2024). Web Development with Python.
4. Kenya National Bureau of Statistics. (2023). Healthcare Access Survey.

---

**Built with  for improving healthcare access**

---

## Quick Start Commands

```bash
# Setup
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Data & Model Preparation
python data_preprocessing.py
python model_training.py

# Run Application
python app.py
# Open http://localhost:5000 in browser
```

---

**Last Updated:** January 3, 2026  
**Version:** 1.0.0
# healthcare
# healthcare
