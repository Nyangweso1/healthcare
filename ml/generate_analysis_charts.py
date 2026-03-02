"""
Project: Healthcare Insurance Risk Prediction System

TASK:
Generate analysis charts for Admin View including:
- Insurance vs. Income distribution
- Risk Score distribution
- Demographics analysis
- Coverage patterns

Author: Prudence
Date: January 5, 2026
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10

# Create output directory
output_dir = 'static/eda'
os.makedirs(output_dir, exist_ok=True)

# Load data
print("Loading healthcare data...")
df = pd.read_csv('data/healthcare_clean.csv')
print(f"✓ Loaded {len(df)} records\n")

# 1. Insurance vs. Income Distribution
print("1. Creating Insurance vs. Income chart...")
plt.figure(figsize=(12, 6))
insured = df[df['Insurance'] == 1]
uninsured = df[df['Insurance'] == 0]

plt.subplot(1, 2, 1)
plt.hist([insured['Monthly Household Income'], uninsured['Monthly Household Income']], 
         bins=30, label=['Insured', 'Uninsured'], color=['#28a745', '#dc3545'], alpha=0.7)
plt.xlabel('Monthly Household Income (KES)')
plt.ylabel('Number of People')
plt.title('Insurance Coverage by Income Level', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
income_bins = [0, 10000, 20000, 30000, 50000, 100000]
income_labels = ['<10K', '10-20K', '20-30K', '30-50K', '>50K']
df['Income_Bracket'] = pd.cut(df['Monthly Household Income'], bins=income_bins, labels=income_labels)
insurance_by_income = df.groupby('Income_Bracket')['Insurance'].apply(lambda x: (x.sum() / len(x)) * 100)
insurance_by_income.plot(kind='bar', color='#667eea', edgecolor='black')
plt.xlabel('Income Bracket (KES)')
plt.ylabel('Insurance Coverage (%)')
plt.title('Insurance Coverage Rate by Income', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f'{output_dir}/insurance_vs_income.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Saved insurance_vs_income.png\n")

# 2. Risk Score Distribution
print("2. Creating Risk Score Distribution...")
plt.figure(figsize=(10, 6))
# Calculate risk scores for all records
from risk_engine import calculate_risk_score

scores = []
categories = []
for _, row in df.iterrows():
    user_data = {
        'Monthly Household Income': row['Monthly Household Income'],
        'Employment Status': row['Employment Status'],
        'routine_check': row.get('Routine check-ups in past year', 0),
        'Age': row['Age']
    }
    score, category = calculate_risk_score(user_data)
    scores.append(score)
    categories.append(category)

df['Risk_Score'] = scores
df['Risk_Category'] = categories

plt.hist(df['Risk_Score'], bins=20, color='#764ba2', edgecolor='black', alpha=0.7)
plt.axvline(df['Risk_Score'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Risk_Score"].mean():.1f}')
plt.xlabel('Risk Score (0-100)')
plt.ylabel('Number of People')
plt.title('Risk Score Distribution Across Population', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(f'{output_dir}/risk_score_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Saved risk_score_distribution.png\n")

# 3. Risk Category Breakdown
print("3. Creating Risk Category Breakdown...")
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
risk_counts = df['Risk_Category'].value_counts()
colors = ['#28a745', '#ffc107', '#dc3545']
plt.pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%', 
        colors=colors, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
plt.title('Population by Risk Category', fontsize=14, fontweight='bold')

plt.subplot(1, 2, 2)
risk_insurance = df.groupby('Risk_Category')['Insurance'].apply(lambda x: (x.sum() / len(x)) * 100)
risk_insurance = risk_insurance.reindex(['Low Risk', 'Medium Risk', 'High Risk'])
risk_insurance.plot(kind='bar', color=colors, edgecolor='black')
plt.xlabel('Risk Category')
plt.ylabel('Insurance Coverage (%)')
plt.title('Insurance Coverage by Risk Category', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f'{output_dir}/risk_category_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Saved risk_category_analysis.png\n")

# 4. Employment vs Insurance
print("4. Creating Employment vs Insurance chart...")
plt.figure(figsize=(10, 6))
employment_insurance = df.groupby('Employment Status')['Insurance'].apply(lambda x: (x.sum() / len(x)) * 100)
employment_insurance.plot(kind='barh', color='#38ef7d', edgecolor='black')
plt.xlabel('Insurance Coverage (%)')
plt.ylabel('Employment Status')
plt.title('Insurance Coverage by Employment Status', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig(f'{output_dir}/employment_vs_insurance.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Saved employment_vs_insurance.png\n")

# 5. Age and Gender Demographics
print("5. Creating Demographics Analysis...")
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
age_bins = [0, 25, 35, 45, 55, 100]
age_labels = ['<25', '25-35', '35-45', '45-55', '55+']
df['Age_Group'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels)
age_insurance = df.groupby('Age_Group')['Insurance'].apply(lambda x: (x.sum() / len(x)) * 100)
age_insurance.plot(kind='bar', color='#f093fb', edgecolor='black')
plt.xlabel('Age Group')
plt.ylabel('Insurance Coverage (%)')
plt.title('Insurance Coverage by Age Group', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')

plt.subplot(1, 2, 2)
gender_insurance = df.groupby('Gender')['Insurance'].apply(lambda x: (x.sum() / len(x)) * 100)
gender_insurance.plot(kind='bar', color='#fa709a', edgecolor='black')
plt.xlabel('Gender')
plt.ylabel('Insurance Coverage (%)')
plt.title('Insurance Coverage by Gender', fontsize=14, fontweight='bold')
plt.xticks(rotation=0)
plt.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{output_dir}/demographics_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Saved demographics_analysis.png\n")

# 6. NHIF Subsidy Eligibility
print("6. Creating NHIF Subsidy Eligibility Analysis...")
plt.figure(figsize=(10, 6))

# High risk = eligible for NHIF subsidy
df['NHIF_Eligible'] = df['Risk_Category'] == 'High Risk'
nhif_eligible_count = df['NHIF_Eligible'].sum()
total_count = len(df)

labels = ['Eligible for\nNHIF Subsidy', 'Standard\nInsurance']
sizes = [nhif_eligible_count, total_count - nhif_eligible_count]
colors = ['#dc3545', '#667eea']
explode = (0.1, 0)

plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', colors=colors,
        startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
plt.title(f'NHIF Subsidy Eligibility Analysis\n({nhif_eligible_count:,} out of {total_count:,} people eligible)', 
          fontsize=14, fontweight='bold')
plt.savefig(f'{output_dir}/nhif_subsidy_eligibility.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Saved nhif_subsidy_eligibility.png\n")

# 7. Summary Statistics
print("7. Generating Summary Statistics...")
stats_text = f"""
HEALTHCARE INSURANCE ANALYSIS SUMMARY
{'='*50}

Total Population Analyzed: {len(df):,}
Insurance Coverage Rate: {(df['Insurance'].sum() / len(df) * 100):.1f}%

Risk Distribution:
- Low Risk: {(df['Risk_Category'] == 'Low Risk').sum():,} ({(df['Risk_Category'] == 'Low Risk').sum() / len(df) * 100:.1f}%)
- Medium Risk: {(df['Risk_Category'] == 'Medium Risk').sum():,} ({(df['Risk_Category'] == 'Medium Risk').sum() / len(df) * 100:.1f}%)
- High Risk: {(df['Risk_Category'] == 'High Risk').sum():,} ({(df['Risk_Category'] == 'High Risk').sum() / len(df) * 100:.1f}%)

NHIF Subsidy Eligibility: {nhif_eligible_count:,} people ({nhif_eligible_count / len(df) * 100:.1f}%)

Average Monthly Income: KES {df['Monthly Household Income'].mean():,.0f}
Median Monthly Income: KES {df['Monthly Household Income'].median():,.0f}

Insurance Coverage by Income:
- Income < 10K: {df[df['Monthly Household Income'] < 10000]['Insurance'].mean() * 100:.1f}%
- Income 10-20K: {df[(df['Monthly Household Income'] >= 10000) & (df['Monthly Household Income'] < 20000)]['Insurance'].mean() * 100:.1f}%
- Income 20-30K: {df[(df['Monthly Household Income'] >= 20000) & (df['Monthly Household Income'] < 30000)]['Insurance'].mean() * 100:.1f}%
- Income > 30K: {df[df['Monthly Household Income'] >= 30000]['Insurance'].mean() * 100:.1f}%
"""

with open(f'{output_dir}/analysis_summary.txt', 'w') as f:
    f.write(stats_text)
print("✓ Saved analysis_summary.txt\n")

print("="*50)
print(" All analysis charts generated successfully!")
print(f" Charts saved to: {output_dir}/")
print("="*50)
