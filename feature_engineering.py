# feature_engineering.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def feature_engineering(file_path="data/safra_cleaned.csv", save_path="data/safra_feature_engineered.csv"):
    # Load cleaned dataset
    df_prep = pd.read_csv(file_path)

    # --- Feature Engineering ---

    # Create binary features for yes/no questions
    binary_cols = [
        'Have you ever had health insurance?',
        'Did you have health insurance during your last hospital visit?',
        'Have you ever had a routine check-up with a doctor or healthcare provider?',
        'Have you ever had a cancer screening (e.g. mammogram, colonoscopy, etc.)?'
    ]
    for col in binary_cols:
        if col in df_prep.columns:
            df_prep[f'{col}_binary'] = df_prep[col].map({'Yes': 1, 'No': 0})

    # Encode income as numerical
    income_mapping = {
        'Less than 10000': 1,
        '10001-20000': 2,
        '20001-30000': 3,
        '30001-40000': 4,
        '40001-50000': 5,
        'More than 50000': 6
    }
    if 'Monthly Household Income' in df_prep.columns:
        df_prep['Income_Numerical'] = df_prep['Monthly Household Income'].map(income_mapping)

    # Encode age as numerical
    age_mapping = {
        '18-30': 1,
        '31-40': 2,
        '41-50': 3,
        '51-60': 4,
        '61-70': 5,
        '71+': 6
    }
    if 'Age' in df_prep.columns:
        df_prep['Age_Numerical'] = df_prep['Age'].map(age_mapping)

    # One-hot encode categorical variables
    categorical_to_encode = ['Gender', 'Marital Status', 'Employment Status', 'Insurance_Category']
    for col in categorical_to_encode:
        if col in df_prep.columns:
            dummies = pd.get_dummies(df_prep[col], prefix=col, drop_first=False)
            df_prep = pd.concat([df_prep, dummies], axis=1)

    # --- NEW SECTION: Label encode any leftover non-numeric columns ---
    cat_cols_left = df_prep.select_dtypes(include=['object']).columns
    if len(cat_cols_left) > 0:
        print(f"\n Encoding remaining categorical columns: {list(cat_cols_left)}")
        le = LabelEncoder()
        for col in cat_cols_left:
            df_prep[col] = le.fit_transform(df_prep[col].astype(str))

    # --- Save feature engineered version ---
    df_prep.to_csv(save_path, index=False)
    print(f"\n Feature engineered dataset saved to {save_path}")
    print("Shape after feature engineering:", df_prep.shape)
    print(df_prep.head())

    return save_path

if __name__ == "__main__":
    feature_engineering()
