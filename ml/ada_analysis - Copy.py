# analysis_visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df_prep = pd.read_csv("data/safra_feature_engineered.csv")
df = df_prep  # alias for convenience

# === 1️ Insurance rate by age group ===
if 'Age_Numerical' in df_prep.columns and 'Have you ever had health insurance?_binary' in df_prep.columns:
    age_insurance = df_prep.groupby('Age_Numerical')['Have you ever had health insurance?_binary'].mean()

    print("\nInsurance rate by age group:")
    print(age_insurance)

    # Map numeric codes to readable age labels
    age_labels_map = {
        1.0: '18-30',
        2.0: '31-40',
        3.0: '41-50',
        4.0: '51-60',
        5.0: '61-70',
        6.0: '71+'
    }

    # Keep only the available age groups
    available_indices = [i for i in age_insurance.index if i in age_labels_map]
    available_labels = [age_labels_map[i] for i in available_indices]
    available_rates = [age_insurance[i] for i in available_indices]

    # Plot
    plt.figure(figsize=(8, 6))
    plt.bar(available_labels, available_rates, color='skyblue')
    plt.xlabel('Age Group')
    plt.ylabel('Proportion with Health Insurance')
    plt.title('Health Insurance Coverage by Age Group')
    plt.tight_layout()
    plt.show()
else:
    print(" Age or insurance columns not found — skipping age group analysis.")

# === 2️ Target variable distribution ===
target_variable = 'Have you ever had health insurance?_binary'
if target_variable in df_prep.columns:
    print("\nTarget variable distribution (counts):")
    print(df_prep[target_variable].value_counts())
    print("\nTarget variable distribution (proportion):")
    print(df_prep[target_variable].value_counts(normalize=True))

    plt.figure(figsize=(8, 6))
    sns.countplot(x=target_variable, data=df_prep)
    plt.title('Distribution of Target Variable (Having Health Insurance)')
    plt.xlabel('Has Health Insurance')
    plt.xticks([0, 1], ['No', 'Yes'])
    plt.tight_layout()
    plt.show()
else:
    print(" Target variable not found — skipping distribution plot.")

# === 3️ Correlation analysis ===
corr_columns = [
    'Age_Numerical', 'Income_Numerical',
    'How many children do you have, if any?',
    'Hospital_Visit_Months',
    'Have you ever had health insurance?_binary', 
    'Did you have health insurance during your last hospital visit?_binary',
    'Have you ever had a routine check-up with a doctor or healthcare provider?_binary',
    'Have you ever had a cancer screening (e.g. mammogram, colonoscopy, etc.)?_binary'
]

# Filter only existing columns
existing_corr_columns = [col for col in corr_columns if col in df_prep.columns]

if len(existing_corr_columns) > 1:
    correlation_matrix = df_prep[existing_corr_columns].corr()

    # Make readable labels
    col_labels_map = {
        'Age_Numerical': 'Age',
        'Income_Numerical': 'Income',
        'How many children do you have, if any?': 'Children',
        'Hospital_Visit_Months': 'Hospital Visits',
        'Have you ever had health insurance?_binary': 'Has Insurance',
        'Did you have health insurance during your last hospital visit?_binary': 'Insurance at Last Visit',
        'Have you ever had a routine check-up with a doctor or healthcare provider?_binary': 'Has Routine Checkups',
        'Have you ever had a cancer screening (e.g. mammogram, colonoscopy, etc.)?_binary': 'Had Cancer Screening'
    }

    labels = [col_labels_map.get(col, col) for col in existing_corr_columns]

    plt.figure(figsize=(12, 10))
    sns.heatmap(
        correlation_matrix, 
        annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5,
        xticklabels=labels, yticklabels=labels
    )
    plt.title('Correlation Matrix of Key Features', fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
else:
    print(" Not enough numerical/binary columns for correlation heatmap.")
