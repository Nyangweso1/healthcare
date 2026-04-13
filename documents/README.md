# Kenya Healthcare Insurance Prediction

This project uses survey data from 6,139 respondents to build a machine learning model that predicts whether an individual in Kenya has health insurance based on socioeconomic and demographic factors.

---

## 1. Project Description

The **Healthcare Insurance Risk Prediction System** is a web-based application that predicts insurance risk using machine learning. It helps identify individuals at risk of being uninsured and provides personalized recommendations for accessing affordable health insurance.

**Key Capability:** The system uses Logistic Regression (91.94% accuracy) with an automatic fallback to rule-based scoring when ML fails, ensuring users always receive valid results even during system failures.

---

## 2. Dataset Overview

| Attribute | Details |
| --------- | ------- |
| **Source** | Healthcare Access Survey (Safra Data School) |
| **Size** | 6,139 respondents |
| **Collection Period** | May 2025 |
| **Region** | Kenya |
| **Target Variable** | Insurance Status (Binary: 1=Insured, 0=Uninsured) |

### Key Features

- **Demographics:** Age, Gender, Marital Status, Number of Children
- **Socioeconomic:** Monthly Income, Employment Status, Education, Family Size
- **Health Status:** Chronic Illness, Healthcare Knowledge
- **Healthcare Access:** Hospital Visit Gap, Routine Checkups, Screenings

### Engineered Features

- **Total Features:** 279 (from 19 input fields)
- **Feature Types:** 4 numerical + 115 one-hot encoded categorical + 160 engineered features
- **Class Distribution:** 58% Insured, 42% Uninsured

---

## 3. Installation & Requirements

### Prerequisites

| Tool | Version |
| ---- | ------- |
| Python | 3.11+ |
| pip | Latest |

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Key Libraries

- **Web Framework:** Flask 3.0.0
- **Machine Learning:** scikit-learn 1.5.1, pandas 2.2.2, numpy 1.26.4
- **Database:** SQLite
- **Model Serialization:** joblib 1.4.2

---

## 4. Methodology

### Step 1: Data Cleaning

- Handled missing values using median/mode imputation
- Removed outliers
- Encoded categorical variables

### Step 2: Exploratory Data Analysis (EDA)

- Analyzed relationship between income and insurance
- Identified key risk factors
- Visualized feature distributions

### Step 3: Feature Engineering

- Expanded 19 input fields to 279 features
- Applied one-hot encoding for categorical variables
- Created employment status mapping (6 form categories → 2 training categories)

### Step 4: Model Training

- Split data: 80% training, 20% testing (stratified)
- Trained **Logistic Regression** and Decision Tree
- Selected Logistic Regression as best model

### Step 5: Model Evaluation

**Logistic Regression Performance:**

| Metric | Value |
| ------ | ------- |
| Accuracy | 91.94% |
| Precision | 96.23% |
| Recall | 89.61% |
| F1-Score | 0.9280 |

**Confusion Matrix:**

- True Negatives (TN): 491
- False Positives (FP): 25
- True Positives (TP): 638
- False Negatives (FN): 74

### Step 6: Dual-System Architecture

The system implements **ML + Rule-Based Fallback:**

- **Primary Path:** Logistic Regression (91.94% accuracy)
- **Fallback Path:** Weighted rule-based algorithm (~75% accuracy)
- **Benefit:** Always produces valid results even when ML fails

---

## 5. How to Use

### Run the Web Application

```bash
python app.py
```

Visit: `http://localhost:5000`

### Train Models Locally

First, prepare the data:

```bash
python ml/data_preprocessing.py
```

Then train the model:

```bash
python ml/model_training.py
```

Output:

- Trained model: `models/insurance_risk_model.pkl`
- Feature names: `models/insurance_risk_model_features.pkl`

### Make Predictions Programmatically

```python
from ml.risk_engine import RiskAssessmentEngine

engine = RiskAssessmentEngine()
result = engine.predict_risk(user_data)
print(result)  # Returns: risk_level, probability, factors, recommendations
```

---

## 6. Key Findings

1. **Monthly Household Income** is the strongest predictor of insurance status
2. **Employment Status** significantly affects insurance risk (unemployed = higher risk)
3. **Preventive Care History** is critical (no checkups = higher risk)
4. **Family Size** impacts risk (larger families = higher risk among low-income groups)
5. **Hospital Visit Gap** indicates healthcare engagement (>12 months gap = higher risk)

### Model Comparison

| Dimension | Logistic Regression | Decision Tree |
| ---------- | ------------------- | ------------- |
| **Accuracy** | 91.94% | 91.53% |
| **Precision** | 96.23% | 95.51% |
| **Recall** | 89.61% | 89.61% |
| **TN Correctly Identified** | 491 | 486 |
| **Best For** | Probability calibration | Rule extraction |

---

## 7. Credits & License

**Data Source:** Safra Data School (May 2025)

**Project Author:** Nyangweso

**Repository:** [Nyangweso1/healthcare](https://github.com/Nyangweso1/healthcare)

**License:** MIT

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
