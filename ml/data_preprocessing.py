
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def preprocess_data(input_path="data/Healthcare Dataset.xlsx", output_path="data/healthcare_clean.csv"):
    """
    Comprehensive data preprocessing for healthcare insurance risk prediction.
    
    Steps:
    1. Load dataset
    2. Drop irrelevant metadata columns
    3. Handle missing values
    4. Encode categorical variables
    5. Engineer features
    6. Create binary target variable
    7. Save cleaned dataset
    """
    
    logger.info("=" * 60)
    logger.info("HEALTHCARE INSURANCE RISK PREDICTION - DATA PREPROCESSING")
    logger.info("=" * 60)

    def _impute_columns(dataframe, columns, strategy):
        """Impute a set of columns with a given strategy."""
        if not columns:
            return
        imputer = SimpleImputer(strategy=strategy)
        dataframe[columns] = imputer.fit_transform(dataframe[columns])
    
    # ========== STEP 1: LOAD DATASET ==========
    logger.info("\n[1/7] Loading dataset...")
    try:
        df = pd.read_excel(input_path)
        logger.info(f"✓ Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
    except FileNotFoundError:
        logger.error(f"✗ File not found: {input_path}")
        return
    except Exception as e:
        logger.error(f"✗ Error loading file: {e}")
        return
    
    # ========== STEP 2: DROP IRRELEVANT METADATA COLUMNS ==========
    logger.info("\n[2/7] Dropping metadata and irrelevant columns...")
    
    # Define columns to drop
    metadata_cols = ['_id', '_uuid', '_submission_time', '_status', '_submitted_by', 
                     '__version__', '_index', '_validation_status', '_notes', '_tags']
    location_cols = ['_Location_latitude', '_Location_longitude', '_Location_altitude', 
                     '_Location_precision', 'Location']
    datetime_cols = ['Date and Time']
    image_cols = ['Your Picture', 'Your Picture_URL']
    
    # Combine all columns to drop
    cols_to_drop = [col for col in (metadata_cols + location_cols + datetime_cols + image_cols) 
                    if col in df.columns]
    
    df = df.drop(columns=cols_to_drop, errors='ignore')
    logger.info(f"✓ Dropped {len(cols_to_drop)} columns")
    
    # Drop completely empty columns
    empty_cols = df.columns[df.isna().all()].tolist()
    if empty_cols:
        df = df.drop(columns=empty_cols)
        logger.info(f"✓ Dropped {len(empty_cols)} empty columns")
    
    # Drop rows where ALL values are missing
    df = df.dropna(how='all')
    logger.info(f"✓ Current shape: {df.shape}")
    
    # ========== STEP 3: CREATE TARGET VARIABLE (VERY IMPORTANT!) ==========
    logger.info("\n[3/7] Creating binary target variable 'insured'...")
    
    target_col = 'Have you ever had health insurance?'
    if target_col not in df.columns:
        logger.error(f"✗ Target column '{target_col}' not found!")
        logger.info(f"Available columns: {df.columns.tolist()}")
        return
    
    # Create binary target: 1 = insured, 0 = uninsured
    df['insured'] = df[target_col].map({'Yes': 1, 'No': 0})
    
    # Handle missing values in target
    if df['insured'].isnull().sum() > 0:
        logger.warning(f"⚠ {df['insured'].isnull().sum()} missing values in target - dropping these rows")
        df = df.dropna(subset=['insured'])
    
    logger.info("✓ Target variable created:")
    logger.info(f"  - Insured (1): {(df['insured'] == 1).sum()} ({(df['insured'] == 1).sum()/len(df)*100:.1f}%)")
    logger.info(f"  - Uninsured (0): {(df['insured'] == 0).sum()} ({(df['insured'] == 0).sum()/len(df)*100:.1f}%)")
    
    # Drop original target column (we now have 'insured')
    df = df.drop(columns=[target_col])
    
    # ========== STEP 4: HANDLE MISSING VALUES ==========
    logger.info("\n[4/7] Handling missing values...")
    
    # Separate numerical and categorical columns
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Remove 'insured' from numerical columns (it's our target)
    if 'insured' in numerical_cols:
        numerical_cols.remove('insured')
    
    logger.info(f"✓ Numerical columns: {len(numerical_cols)}")
    logger.info(f"✓ Categorical columns: {len(categorical_cols)}")
    
    # Impute numerical columns with median
    _impute_columns(df, numerical_cols, 'median')
    if numerical_cols:
        logger.info(f"✓ Imputed {len(numerical_cols)} numerical columns with median")
    
    # Impute categorical columns with most frequent value
    _impute_columns(df, categorical_cols, 'most_frequent')
    if categorical_cols:
        logger.info(f"✓ Imputed {len(categorical_cols)} categorical columns with most_frequent")
    
    # ========== STEP 5: FEATURE ENGINEERING ==========
    logger.info("\n[5/7] Engineering features...")
    
    # Feature 1: hospital_visit_gap (months since last hospital visit)
    if 'When was the last time you visited a hospital' in df.columns:
        visit_col = 'When was the last time you visited a hospital'
        visit_mapping = {
            'Within the last month': 0.5,
            'Within the last 3 months': 2,
            'Within the last 6 months': 4.5,
            'Within the last year': 9,
            'More than a year ago': 18,
            'Never': 24,
            'I don\'t know': 12
        }
        df['hospital_visit_gap'] = df[visit_col].map(visit_mapping).fillna(12)
        logger.info("✓ Created feature: hospital_visit_gap")
    
    # Feature 2: preventive_care_score
    preventive_score = 0
    if 'Have you ever had a routine check-up?' in df.columns:
        df['routine_check'] = df['Have you ever had a routine check-up?'].map({'Yes': 1, 'No': 0}).fillna(0)
        preventive_score += 1
    
    if 'Have you ever had a cancer screening?' in df.columns:
        df['cancer_screening'] = df['Have you ever had a cancer screening?'].map({'Yes': 1, 'No': 0}).fillna(0)
        preventive_score += 1
    
    if preventive_score > 0:
        score_cols = [c for c in ['routine_check', 'cancer_screening'] if c in df.columns]
        df['preventive_care_score'] = df[score_cols].sum(axis=1)
        logger.info(f"✓ Created feature: preventive_care_score (from {len(score_cols)} indicators)")
    
    # Feature 3: Age groups (convert to numeric first)
    if 'Age' in df.columns:
        # Convert Age to numeric (handle any string values)
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        # Fill any NaN values with median age
        df['Age'] = df['Age'].fillna(df['Age'].median())
        
        df['age_group'] = pd.cut(df['Age'], bins=[0, 25, 35, 50, 100], 
                                  labels=['18-25', '26-35', '36-50', '50+'])
        logger.info("✓ Created feature: age_group")
    
    # Feature 4: Income buckets (convert to numeric first)
    if 'Monthly Household Income' in df.columns:
        # Convert Income to numeric (handle any string values)
        df['Monthly Household Income'] = pd.to_numeric(df['Monthly Household Income'], errors='coerce')
        # Fill any NaN values with median income
        df['Monthly Household Income'] = df['Monthly Household Income'].fillna(df['Monthly Household Income'].median())
        
        df['income_bucket'] = pd.cut(df['Monthly Household Income'], 
                                      bins=[0, 20000, 50000, 100000, float('inf')],
                                      labels=['Low', 'Medium', 'High', 'Very High'])
        logger.info("✓ Created feature: income_bucket")
    
    # Feature 5: Number of children as numeric
    if 'How many children do you have' in df.columns:
        df['num_children'] = pd.to_numeric(df['How many children do you have'], errors='coerce').fillna(0)
        logger.info("✓ Created feature: num_children")
    
    # ========== STEP 6: ENCODE CATEGORICAL VARIABLES ==========
    logger.info("\n[6/7] Encoding categorical variables...")
    
    # Get current categorical columns (after feature engineering)
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if categorical_cols:
        # Convert all categorical columns to strings to handle mixed types
        for col in categorical_cols:
            df[col] = df[col].astype(str)
        
        # Use OneHotEncoder
        encoder = OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore')
        encoded_array = encoder.fit_transform(df[categorical_cols])
        encoded_cols = encoder.get_feature_names_out(categorical_cols)
        
        # Create DataFrame with encoded columns
        encoded_df = pd.DataFrame(encoded_array, columns=encoded_cols, index=df.index)
        
        # Drop original categorical columns and concatenate encoded ones
        df = df.drop(columns=categorical_cols)
        df = pd.concat([df, encoded_df], axis=1)
        
        logger.info(f"✓ Encoded {len(categorical_cols)} categorical columns into {len(encoded_cols)} features")
    
    # ========== STEP 7: FINAL CLEANUP AND SAVE ==========
    logger.info("\n[7/7] Final cleanup and saving dataset...")
    
    # Fill any remaining NaN values
    # For numerical columns, fill with 0
    numerical_final = df.select_dtypes(include=['number']).columns.tolist()
    if 'insured' in numerical_final:
        numerical_final.remove('insured')
    
    for col in numerical_final:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(0)
            logger.info(f"  Filled remaining NaN in {col} with 0")
    
    # Verify no NaN values remain
    total_nan = df.isnull().sum().sum()
    if total_nan > 0:
        logger.warning(f"⚠ {total_nan} NaN values remain - dropping rows")
        df = df.dropna()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    logger.info(f"✓ Dataset saved to: {output_path}")
    logger.info(f"✓ Final shape: {df.shape}")
    logger.info(f"✓ Features (X): {df.shape[1] - 1} columns")
    logger.info("✓ Target (y): insured (binary: 0=uninsured, 1=insured)")
    
    # Display feature summary
    logger.info("\n" + "=" * 60)
    logger.info("PREPROCESSING COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Total samples: {len(df)}")
    logger.info(f"Total features: {df.shape[1] - 1}")
    logger.info("Target distribution:")
    logger.info(f"  Insured: {(df['insured']==1).sum()}")
    logger.info(f"  Uninsured: {(df['insured']==0).sum()}")
    
    return df


# --- Run preprocessing if this file is executed directly ---
if __name__ == "__main__":
    preprocess_data()
