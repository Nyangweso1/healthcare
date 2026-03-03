# Healthcare Insurance Risk Prediction System

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-F7931E?logo=scikit-learn&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

## Project Overview

The **Healthcare Insurance Risk Prediction System** is an intelligent web-based application that predicts whether individuals are at risk of being uninsured, based on their demographic, socioeconomic, and healthcare access patterns. The system provides actionable, personalised recommendations to help vulnerable populations secure affordable health insurance.

**Developer:** Prudence
**Institution:** University of Embu
**Version:** 1.0.0
**Last Updated:** March 3, 2026

## Problem Statement

In many regions, particularly rural and low-income communities, individuals face significant barriers to accessing health insurance. This leads to:

- **Financial vulnerability** during medical emergencies
- **Delayed healthcare** due to cost concerns
- **Poor health outcomes** from lack of preventive care
- **Economic burden** on families and communities

### The Challenge

How can we identify individuals at highest risk of being uninsured before they need medical care, and provide targeted interventions to secure coverage?

---

## Solution

The system uses machine learning to:

1. **Predict insurance risk** using:
   - Demographic factors (age, gender, marital status)
   - Socioeconomic indicators (income, employment, education, family size)
   - Healthcare access behaviours (hospital visits, preventive care, screenings)

2. **Classify risk levels:**
   - **Low Risk** — < 30% probability of being uninsured
   - **Medium Risk** — 30–60% probability
   - **High Risk** — > 60% probability

3. **Provide personalised recommendations:**
   - SHA/NHIF enrolment guidance
   - Subsidised insurance programmes
   - Community-based health insurance
   - Preventive care education

---

## Features

| Feature | Description |
| ------- | ----------- |
| User Authentication | Secure registration and login with hashed passwords |
| Risk Assessment Form | Guided 4-section questionnaire (demographics, finances, health, access) |
| ML-Powered Prediction | Instant insurance risk classification: Low, Medium, or High |
| Personalised Results | Probability score, top risk factors, and tailored action steps |
| Assessment History | Review all your past assessments with date, score, and risk level |
| Health Tips | Curated articles on preventive care and staying healthy |
| Data Insights (EDA) | Interactive charts and statistics from the training dataset |
| Insurance Guide | Plain-language explanations of insurance types and benefits |
| Admin Dashboard | Manage users, view all assessments, send messages to users |
| Contact & Messaging | Users can send messages to the support team |

---

## Dataset

| Attribute | Details |
| --------- | ------- |
| Source | Healthcare access survey |
| Sample size | 6,158 respondents |
| Collection period | May 2025 |
| Region | Kenya |

### Target Variable

**Have you ever had health insurance?**

- `Yes` → Insured
- `No` → Uninsured (High Risk)

### Input Features

| Category | Features |
| -------- | -------- |
| Demographics | Age, Gender, Marital Status, Number of Children |
| Socioeconomic | Monthly Household Income, Employment Status, Education Level, Residence Type, Family Size |
| Health Status | Chronic Illness, Healthcare Knowledge |
| Healthcare Access | Hospital Visit Gap, Routine Checkups, Cancer Screening, Dental Checkup, Mental Health Support |

### Engineered Features

| Feature | Description |
| ------- | ----------- |
| `hospital_visit_gap` | Months since last hospital visit |
| `preventive_care_score` | Sum of all preventive care activities |
| `age_group` | Categorical age buckets (18-25, 26-35, 36-50, 50+) |
| `income_bucket` | Income category (Low, Medium, High, Very High) |

---

## Machine Learning Approach

### Models

| Model | Description |
| --- | --- |
| Logistic Regression | Linear model with interpretable coefficients. Best for stakeholder reporting. |
| Decision Tree (max_depth=5) | Rule-based predictions. Captures non-linear patterns. |

### Training Pipeline

```text
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

### Key Findings

Strongest predictors of insurance risk:

1. **Monthly Household Income** (strongest factor)
2. **Employment Status** (unemployed = higher risk)
3. **Preventive Care Score** (no checkups = higher risk)
4. **Number of Children** (larger families = higher risk)
5. **Hospital Visit Gap** (long time since visit = higher risk)

---

## System Architecture

### Technology Stack

| Layer | Technologies |
| --- | --- |
| Backend | Python 3.11+, Flask 3.0.0, SQLite |
| Frontend | HTML5, CSS3, Bootstrap 5.3, JavaScript |
| Machine Learning | scikit-learn, pandas, NumPy, joblib |
| Visualisation | matplotlib, seaborn |

### System Flow

```text
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

```text
healthcare_prediction_system/
│
├── app.py                              # Flask web application (all routes)
├── requirements.txt                    # Python dependencies
├── start_app.bat                       # Windows one-click startup
├── .python-version                     # Python version pin
│
├── data/
│   └── healthcare_clean.csv            # Processed dataset for training
│
├── documents/
│   └── README.md                       # This file
│
├── instance/
│   └── users.db                        # SQLite database (users, assessments)
│
├── ml/
│   ├── __init__.py
│   ├── risk_engine.py                  # Core risk assessment & prediction logic
│   ├── model_training.py               # Train and save ML models
│   ├── data_preprocessing.py           # Data cleaning & feature engineering
│   ├── feature_engineering.py          # Feature engineering helpers
│   ├── model_evaluation.py             # Model evaluation utilities
│   ├── predict.py                      # Standalone prediction utility
│   ├── ada_analysis.py                 # AdaBoost model analysis
│   ├── generate_analysis_charts.py     # EDA chart generation
│   └── diagnose.py                     # Model diagnostics
│
├── models/
│   ├── insurance_risk_model.pkl        # Primary trained model (used by web app)
│   ├── insurance_risk_model_features.pkl  # Feature names companion file
│   └── insurance_model.pkl             # Standalone scripts only (predict.py, model_evaluation.py)
│
├── static/
│   ├── css/
│   │   ├── base.css   assess.css   results.css  history.css
│   │   ├── auth.css   home.css     blog.css      health_tips.css
│   │   ├── eda.css    about.css    contact.css   admin.css
│   │   ├── messaging.css  errors.css   style.css
│   └── js/
│       └── script.js
│
├── templates/
│   ├── base.html                   # Master layout (navbar, footer)
│   ├── index.html                  # Landing page
│   ├── register.html / login.html  # Authentication
│   ├── assess.html                 # Risk assessment form
│   ├── results.html                # Prediction results
│   ├── history.html                # Assessment history
│   ├── blog.html                   # Insurance guide
│   ├── health_tips.html            # Health tips list
│   ├── health_tip_detail.html      # Individual health tip
│   ├── eda.html                    # Data insights
│   ├── about.html / contact.html   # Info & messaging
│   ├── admin_dashboard.html        # Admin panel
│   ├── admin_user_view.html        # Admin: user detail
│   ├── 404.html / 500.html         # Error pages
│
└── utils/
    ├── create_admin.py             # Create admin account
    ├── make_admin.py               # Promote user to admin
    ├── check_users.py              # List database users
    └── test_template.py            # Template testing
```

---

## Pages & Routes

| Page | Route | Login Required |
| ---- | ----- | :------------: |
| Home | `/` | No |
| Register | `/register` | No |
| Login | `/login` | No |
| Risk Assessment | `/assess` | Yes |
| Results | `/results` | Yes |
| My History | `/history` | Yes |
| Insurance Guide | `/blog` | No |
| Health Tips | `/health_tips` | No |
| Data Insights | `/eda` | No |
| About | `/about` | No |
| Contact | `/contact` | Yes |
| Admin Panel | `/admin` | Admin only |

---

## Installation & Setup

### Prerequisites

Make sure the following are installed on your machine before you begin:

| Tool | Version | Download |
| ---- | ------- | -------- |
| Python | 3.11 or higher | [python.org/downloads](https://www.python.org/downloads/) |
| Git | Any recent version | [git-scm.com](https://git-scm.com/) |
| pip | Comes with Python | — |

> **Check your Python version:**
>
> ```bash
> python --version
> ```
>
> You should see `Python 3.11.x` or higher.

---

### Step 0 — Clone the Repository

```bash
git clone https://github.com/Nyangweso1/healthcare.git
cd healthcare
```

> If you downloaded the project as a ZIP, unzip it and open a terminal inside the project folder instead.

### Step 1 — Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Train the Model

`data/healthcare_clean.csv` is included. Run:

#### Run Data Preprocessing

```bash
python ml/data_preprocessing.py
```

#### Train the Model

```bash
python ml/model_training.py
```

### Step 4 — Run the Application

```bash
python app.py
```

Or double-click **start_app.bat** on Windows.

Expected output:

```text
INFO: ✓ Risk Assessment Engine initialized
INFO: ✓ Database initialized
* Running on http://0.0.0.0:5000
```

### Step 5 — Open in Browser

```text
http://localhost:5000
```

---

## Quick Start

> For full step-by-step instructions see [Installation & Setup](#installation--setup).

```bash
# 1. Clone the project
git clone https://github.com/Nyangweso1/healthcare.git
cd healthcare

# 2. Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Prepare data and train the model
python ml/data_preprocessing.py
python ml/model_training.py

# 5. Start the app
python app.py
```

Open your browser and go to: **<http://localhost:5000>**

---

## Using the System

### First-Time Setup

1. Open **<http://localhost:5000>** in your browser.
2. Click **Register** to create a new account (username, email, password).
3. Log in with the username and password you just created.

> ⚠️ **Note:** Login uses your **username**, not your email address. Passwords are case-sensitive.

### Running a Risk Assessment

1. Click **"Risk Assessment"** in the navigation bar (or go to `/assess`).
2. Complete all four sections of the form:

   | Section | Fields |
   | ------- | ------ |
   | Demographics | Age, Gender, Marital Status, Number of Children |
   | Socioeconomic | Employment, Monthly Income, Education, Residence, Family Size |
   | Health Status | Chronic Illness, Healthcare Knowledge Level |
   | Healthcare Access | Last Hospital Visit, Routine Checkups, Screenings |

3. Click **"Assess My Risk"** to submit.
4. Your results page will show:
   - **Risk Level** — Low, Medium, or High
   - **Probability Score** — percentage chance of being uninsured
   - **Top Risk Factors** — the specific inputs driving your risk
   - **Recommendations** — personalised action steps (e.g. NHIF registration, subsidised programmes)

### Exploring Other Pages

| Page | What it does |
| ---- | ------------ |
| **My History** (`/history`) | View all your previous assessments with dates and risk levels |
| **Insurance Guide** (`/blog`) | Read articles explaining health insurance types and benefits |
| **Health Tips** (`/health_tips`) | Browse preventive care tips and healthy lifestyle articles |
| **Data Insights** (`/eda`) | Explore charts and statistics from the underlying dataset |
| **About** (`/about`) | Learn about the project, its goals, and the team |
| **Contact** (`/contact`) | Send a message to the support team |

---

## Model Performance

### Evaluation Metrics (Example)

| Model               | Accuracy | Precision | Recall | F1-Score |
| ------------------- | -------- | --------- | ------ | -------- |
| Logistic Regression | 0.8234   | 0.7891    | 0.8456 | 0.8163   |
| Decision Tree       | 0.7956   | 0.7634    | 0.8123 | 0.7871   |

**Best Model:** Logistic Regression (F1-Score: 0.8163)

### Confusion Matrix

```text
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

## Ethical Considerations

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

## Future Improvements

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

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).

You are free to use, copy, modify, and distribute this software for personal, academic, or commercial purposes, provided you include the original copyright notice.

---

## Contributing

This is an academic project, but contributions are welcome!

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## Admin Panel

```bash
# Create a new admin account
python utils/create_admin.py

# Promote an existing user to admin
python utils/make_admin.py
```

Admins can: view all users, view all assessments, inspect individual user profiles, and send messages to users.

---

## Troubleshooting

| Problem | Fix |
| ------- | --- |
| `No module named flask` | `pip install -r requirements.txt` |
| Model not found error | `python ml/model_training.py` then restart `app.py` |
| CSS not loading | Open via `python app.py`, not by opening HTML files directly |
| Invalid credentials | Use your **username** (not email). Case-sensitive. |
| Port 5000 already in use | Set `app.run(port=5001)` in `app.py`, access `localhost:5001` |
| Database error on first run | Delete `instance/users.db` and restart — recreated automatically |

---

## Contact & Support

**Developer:** Prudence  
**Institution:** University of Embu  
**Project Repository:** [https://github.com/Nyangweso1/healthcare](https://github.com/Nyangweso1/healthcare)

---

## Acknowledgements

- Healthcare survey data contributors
- Open-source community (scikit-learn, Flask, Bootstrap)
- Academic advisors and reviewers
- All individuals working toward universal health coverage

---

## References

1. World Health Organization. (2023). Universal Health Coverage.
2. Scikit-learn Documentation. (2024). Machine Learning in Python.
3. Flask Documentation. (2024). Web Development with Python.
4. Kenya National Bureau of Statistics. (2023). Healthcare Access Survey.
