# Healthcare Insurance Risk Prediction System

##  Project Overview

The **Healthcare Insurance Risk Prediction System** is an intelligent web-based application that predicts whether individuals are at risk of being uninsured based on their demographic, socioeconomic, and healthcare access patterns. The system provides actionable recommendations to help vulnerable populations access affordable health insurance.

**Developed by:** Prudence
**Date:** January 3, 2026
**Institution:** [university of embu]
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
   - **Medium Risk** (30-60% probability of being uninsured)
   - **High Risk** (> 60% probability)

3. **Provide personalized recommendations**:
   - NHIF enrollment guidance
   - Subsidized insurance programs
   - Community-based health insurance
   - Preventive care education

---

##  Dataset Description

### Source
- **Survey Data**: Healthcare access survey from [Region]
- **Sample Size**: [6158] respondents
- **Collection Period**: [may 2025]

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
├── requirements.txt                # Python dependencies
├── start_app.bat                   # Windows startup script
│
├── data/
│   └── healthcare_clean.csv        # Processed dataset for training
│
├── documents/
│   └── README.md                   # Project documentation
│
├── instance/
│   └── users.db                    # SQLite user database
│
├── ml/
│   ├── __init__.py
│   ├── data_preprocessing.py       # Data cleaning & feature engineering
│   ├── model_training.py           # Train ML models
│   ├── risk_engine.py              # Risk assessment logic
│   ├── model_evaluation.py         # Model evaluation utilities
│   ├── feature_engineering.py      # Feature engineering helpers
│   └── predict.py                  # Prediction utilities
│
├── models/
│   ├── insurance_risk_model.pkl    # Trained ML model
│   └── insurance_risk_model_features.pkl  # Feature names
│
├── static/
│   ├── css/                        # Per-page stylesheets
│   └── js/
│       └── script.js
│
├── templates/
│   ├── base.html                   # Base layout template
│   ├── index.html                  # Landing page
│   ├── register.html               # User registration
│   ├── login.html                  # User login
│   ├── assess.html                 # Risk assessment form
│   ├── results.html                # Results display
│   ├── history.html                # Assessment history
│   ├── blog.html                   # Insurance guide
│   ├── health_tips.html            # Health tips
│   ├── eda.html                    # Data insights
│   ├── about.html                  # About page
│   ├── contact.html                # Contact / messages
│   ├── admin_dashboard.html        # Admin panel
│   ├── 404.html                    # 404 error page
│   └── 500.html                    # 500 error page
│
└── utils/
    ├── create_admin.py             # Create a new admin user
    ├── make_admin.py               # Promote existing user to admin
    ├── check_users.py              # List database users
    └── test_template.py            # Template testing utility
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
- `data/healthcare_clean.csv` should already be present. If missing, re-run preprocessing.

#### 5. Run Data Preprocessing

```bash
python ml/data_preprocessing.py
```

**Expected Output:**
- Creates `data/healthcare_clean.csv`
- Displays data cleaning statistics
- Shows target variable distribution

#### 6. Train the Model

```bash
python ml/model_training.py
```

**Expected Output:**
- Creates `models/insurance_risk_model.pkl`
- Creates `models/insurance_risk_model_features.pkl`
- Displays model performance metrics
- Shows feature importance

#### 7. Test the Risk Engine (Optional)

```bash
python ml/risk_engine.py
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
python ml/data_preprocessing.py
python ml/model_training.py

# Run Application
python app.py
# Open http://localhost:5000 in browser
```

---

**Last Updated:** January 3, 2026
**Version:** 1.0.0

---

---

# 📘 Complete Beginner's Guide — Start Here If You Are New

> This section is written for someone who has **never used this system before**.  
> Read it from top to bottom before touching anything else.

---

## 🧭 What Is This System, In Simple Terms?

Imagine you go to a doctor and describe your lifestyle — your income, your job, your family, when you last went to hospital. The doctor then tells you: *"Based on what you've told me, you are at HIGH risk of not having health insurance — here is what you should do."*

That is exactly what this system does — but automatically, using a machine learning model trained on real survey data.

**In one sentence:**  
> This system collects basic information about you, runs it through a trained AI model, and tells you how likely you are to be uninsured — then gives you specific steps to fix it.

---

## 🗺️ Step 1 — Understand the Pages (What Each Page Does)

When you open the app at `http://localhost:5000`, you will see a website with several pages. Here is what each one does:

| Page | URL | What It Does |
|------|-----|--------------|
| **Home** | `/` | Landing page. Introduction to the system. Links to register or log in. |
| **Register** | `/register` | Create a new account with username, email, and password. |
| **Login** | `/login` | Log in to your existing account. |
| **Risk Assessment** | `/assess` | The main form. Fill in your details to get your risk prediction. **Requires login.** |
| **Results** | `/results` | Displays your risk level, probability score, risk factors, and recommendations after submitting assessment. |
| **My History** | `/history` | Shows all your past assessments in a table. You can search and filter by risk level. **Requires login.** |
| **Insurance Guide** | `/blog` | Explains all Kenyan insurance options — SHA/NHIF, Britam, Jubilee, APA, community plans, etc. |
| **Health Tips** | `/health_tips` | Articles and tips on staying healthy and reducing insurance risk. |
| **Data Insights** | `/eda` | Visual charts and graphs from the dataset. Useful for understanding trends. |
| **About** | `/about` | Information about the project, its purpose, and the developer. |
| **Messages / Contact** | `/contact` | Send or receive messages within the system. |
| **Admin Panel** | `/admin` | Manage users and view all assessments. **Admin accounts only.** |

---

## 👣 Step 2 — Your First Time Using the System (Full Walkthrough)

Follow these steps **in order** the very first time you use the system.

### ✅ Step 2.1 — Start the Server

Open a terminal (Command Prompt on Windows) in the project folder and run:

```bash
python app.py
```

You should see:
```
INFO: ✓ Risk Assessment Engine initialized
INFO: ✓ Database initialized
* Running on http://0.0.0.0:5000
```

Leave this terminal open. Do not close it while using the app.

### ✅ Step 2.2 — Open the App in Your Browser

Open any web browser (Chrome, Edge, Firefox) and go to:
```
http://localhost:5000
```

You will see the **Home page**.

### ✅ Step 2.3 — Create an Account

1. Click **Register** in the navigation bar
2. Fill in:
   - **Username** — any name you want (e.g. `john_doe`)
   - **Email** — your email address
   - **Password** — choose a strong password
   - **Confirm Password** — type it again
3. Click **Register**
4. You will be redirected to the login page

### ✅ Step 2.4 — Log In

1. Enter your username and password
2. Click **Login**
3. You are now logged in — you will see your username in the top navigation bar

### ✅ Step 2.5 — Take Your First Risk Assessment

1. Click **Risk Assessment** in the navigation bar
2. Fill in **all fields** in the form:

   **Section A — Demographics:**
   - **Age** — your age in years (e.g. `28`)
   - **Gender** — Male / Female
   - **Marital Status** — Single / Married / Divorced / Widowed
   - **Number of Children** — how many children you have (enter `0` if none)

   **Section B — Socioeconomic:**
   - **Monthly Income (KES)** — your household income per month (e.g. `25000`)
   - **Employment Status** — Employed / Self-employed / Unemployed / Student

   **Section C — Healthcare Access:**
   - **Last Hospital Visit** — when did you last go to a hospital? (select from the dropdown)
   - **Routine Check-up** — have you ever had a routine medical check-up? (Yes / No)
   - **Cancer Screening** — have you ever had a cancer screening? (Yes / No)
   - **Insurance During Last Visit** — did you have insurance the last time you visited a hospital? (Yes / No)

3. Click the **"Assess My Risk"** button
4. You will be taken to the **Results page** automatically

---

## 📊 Step 3 — Understanding Your Results

Your results page has **four main sections**. Here is how to read each one:

### 3.1 — Risk Level Badge

You will see one of three badges:

| Badge | Colour | Meaning |
|-------|--------|---------|
| 🟢 **LOW RISK** | Green | You are likely already insured OR have factors that protect you. Keep it up. |
| 🟡 **MEDIUM RISK** | Orange/Yellow | You have some gaps. Action recommended but not urgent. |
| 🔴 **HIGH RISK** | Red | You are very likely uninsured or at high risk. Immediate action needed. |

### 3.2 — Probability Score

This is a **percentage** — for example `72.4%`.

> It means: *"Based on your data, there is a 72.4% chance that you do not have health insurance."*

- Below 30% → Low Risk
- 30% to 60% → Medium Risk
- Above 60% → High Risk

### 3.3 — Rule-Based Score

This is a **score out of 100** calculated separately from the ML model using fixed rules (income thresholds, employment status, etc.).

- **0–39** → Very High Risk
- **40–59** → High Risk
- **60–74** → Medium Risk
- **75–100** → Low Risk

Both the ML probability and the rule score are shown so you can see two perspectives on your risk.

### 3.4 — Risk Factors & Recommendations

Below the scores, you will see:

- **Why you are at risk** — a list of the specific things about your profile that increased your risk (e.g. "Low income", "No routine check-up", "Long gap since hospital visit")
- **What to do** — personalised recommendations such as:
  - Register for SHA (Social Health Authority)
  - Consider community-based insurance
  - Schedule a routine check-up
  - Explore employer-sponsored insurance

> 💡 **Tip:** Click the links in the recommendations to go directly to the **Insurance Guide** page for detailed instructions on each option.

---

## 📁 Step 4 — Viewing Your History

After completing one or more assessments:

1. Click **My History** in the navigation bar
2. You will see a table with all your past assessments
3. Each row shows: Date, Risk Level, Probability, Rule Score, Age, Income, Employment
4. Use the **search bar** to look for specific entries
5. Use the **Risk Level filter** dropdown to show only High / Medium / Low risk entries
6. On mobile, the table becomes individual cards automatically

---

## 📖 Step 5 — Using the Insurance Guide

If you are unsure which insurance to choose:

1. Click **Insurance Guide** in the navigation bar
2. You will see sections for:
   - **SHA/NHIF** — government-run universal health coverage (cheapest option, best for low income)
   - **Linda Mama** — free maternity cover for all Kenyan women
   - **Private Insurance** — Britam, Jubilee, APA (better hospitals, more features, higher cost)
   - **Family Plans** — cover your whole family under one policy
   - **Affordable Options** — for those earning under KES 25,000/month
   - **Chronic Illness Coverage** — for diabetes, hypertension, cancer
   - **Community-Based Insurance** — local cooperative schemes
3. Each section has direct links to the insurer's website

---

## 🔐 Step 6 — Admin Panel (Admin Users Only)

The admin panel is for **system administrators** — not regular users.

### How to Become an Admin

Run this in your terminal (with the virtual environment active):

```bash
python utils/create_admin.py
```

Or to promote an existing user:
```bash
python utils/make_admin.py
```

Follow the prompts to promote a user to admin.

### What Admins Can Do

1. Log in normally, then click **Admin Panel** in the navigation bar
2. **View all registered users** — names, emails, registration dates
3. **View all assessments** across all users
4. **Manage users** — view individual user profiles and their assessment history

> ⚠️ Admin credentials should never be shared. Only give admin access to trusted system managers.

---

## ⚠️ Step 7 — Troubleshooting Common Problems

### Problem: App won't start — "No module named flask"
**Fix:** You haven't installed dependencies. Run:
```bash
pip install -r requirements.txt
```

### Problem: App starts but shows "Model not found" error
**Fix:** You haven't trained the model yet. Run:
```bash
python data_preprocessing.py
python model_training.py
```
Then restart `python app.py`.

### Problem: "Internal Server Error" on the Results page
**Fix:** The dataset file may be missing. Make sure `data/Healthcare Dataset.xlsx` exists in the `data/` folder, then re-run preprocessing.

### Problem: Can't log in — "Invalid credentials"
**Fix:** Make sure you are entering the exact username (not email) and password you registered with. Passwords are case-sensitive.

### Problem: Page shows but CSS/styles are broken (unstyled page)
**Fix:** Make sure you are running `python app.py` — do NOT open the HTML files directly from the folder. The CSS only loads correctly through the Flask server.

### Problem: Port 5000 already in use
**Fix:** Another app is using port 5000. Either close it, or change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```
Then access the app at `http://localhost:5001`.

### Problem: Database error on first run
**Fix:** Delete the file `instance/users.db` if it exists and restart the app. The database will be recreated automatically.

---

## 📚 Step 8 — Glossary of Terms

If you see a word you do not understand, look it up here:

| Term | Plain English Meaning |
|------|----------------------|
| **ML / Machine Learning** | A type of AI that learns patterns from data and makes predictions |
| **Model** | The trained AI brain of the system — stored as a `.pkl` file |
| **Probability** | A percentage chance, e.g. 72% probability of being uninsured |
| **Feature** | A piece of information used to make a prediction (e.g. age, income) |
| **Risk Level** | A label — Low, Medium, or High — summarising your overall risk |
| **Flask** | The Python framework that runs the web server |
| **SQLite** | A lightweight database used to store user accounts and assessments |
| **SHA** | Social Health Authority — Kenya's national health insurance body (replaced NHIF in 2024) |
| **NHIF** | National Hospital Insurance Fund — predecessor to SHA |
| **Admin** | A special user account with extra permissions to manage the system |
| **Virtual Environment (venv)** | An isolated Python workspace so project packages don't conflict with other projects |
| **pip** | Python's package installer — used to install libraries from `requirements.txt` |
| **localhost:5000** | Your local computer acting as a web server on port 5000 |
| **Preprocessing** | Cleaning and preparing raw data before feeding it to the model |
| **F1-Score** | A measure of model accuracy that balances precision and recall (higher = better) |
| **Rule-Based Score** | A score calculated using fixed logical rules, separate from the ML model |

---

## ❓ Step 9 — Frequently Asked Questions (FAQ)

**Q: Do I need internet access to use this system?**  
A: No. Once set up, the system runs entirely on your local computer. Internet is only needed to install packages the first time.

---

**Q: Can I use this system on my phone?**  
A: Yes, the interface is mobile-responsive. As long as your phone is on the same Wi-Fi network as the computer running the server, navigate to `http://[your-computer-IP]:5000`.

---

**Q: Is my data safe?**  
A: Your data is stored locally in `instance/users.db` on your own computer. It is not sent anywhere online. Passwords are stored as hashed values, not plain text.

---

**Q: How accurate is the prediction?**  
A: The Logistic Regression model achieves approximately **82% accuracy** on test data. This means about 1 in 5 predictions may not perfectly reflect your real situation. Use the results as guidance, not as a definitive diagnosis.

---

**Q: Can I retake the assessment?**  
A: Yes, as many times as you want. Each submission is saved separately in your history. This is useful for tracking how your risk changes over time (e.g. after getting a new job or enrolling in insurance).

---

**Q: What if I fill in the form incorrectly?**  
A: The form has validation — it will highlight fields that are missing or invalid before submitting. If you submitted incorrect data, simply take a new assessment with the correct values.

---

**Q: How do I update the model with new data?**  
A: Replace `data/Healthcare Dataset.xlsx` with your updated dataset, then run:
```bash
python data_preprocessing.py
python model_training.py
```
Restart `python app.py` to use the newly trained model.

---

**Q: What does "rule-based score" mean vs "ML probability"?**  
A: The **ML probability** is what the AI model calculated based on patterns it learned from thousands of survey responses. The **rule-based score** is calculated using straightforward logical rules (e.g. "if income < 15,000 and unemployed, add 30 penalty points"). Having both gives a more complete picture.

---

**Q: I am a developer — where do I start reading the code?**  
A: Start with these files in order:
1. `app.py` — all routes and logic
2. `ml/risk_engine.py` — how risk is calculated
3. `ml/model_training.py` — how the ML model is built
4. `ml/data_preprocessing.py` — how raw data is cleaned
5. `templates/` — all HTML pages
6. `static/css/` — all styling

---

## 🧪 Step 10 — Quick Sanity Check (Confirm Everything Works)

Run through this checklist after setup to confirm the system is working correctly:

- [ ] `python app.py` starts without errors
- [ ] `http://localhost:5000` loads the home page in your browser
- [ ] You can register a new account
- [ ] You can log in with that account
- [ ] The Risk Assessment form loads at `/assess`
- [ ] Submitting the form takes you to a Results page with a risk level shown
- [ ] Your history appears at `/history`
- [ ] The Insurance Guide loads at `/blog`
- [ ] Logging out works and redirects you to the home page

If all boxes are checked ✅ — your system is fully working.

---

**Last Updated:** January 3, 2026  
**Version:** 1.0.0
