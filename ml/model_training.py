

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Get absolute paths based on script location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA_PATH = os.path.join(BASE_DIR, "data", "healthcare_clean.csv")
DEFAULT_MODEL_PATH = os.path.join(BASE_DIR, "models", "insurance_risk_model.pkl")


def _train_and_log(model, name, x_train, y_train):
    logger.info(f"\n  → Training {name}...")
    model.fit(x_train, y_train)
    logger.info(f"  ✓ {name} trained")
    return model


def train_models(data_path=None, model_output_path=None):
    """
    Train and evaluate machine learning models for insurance risk prediction.
    
    Args:
        data_path: Path to cleaned CSV data (default: data/healthcare_clean.csv)
        model_output_path: Where to save the model (default: models/insurance_risk_model.pkl)
    """
    # Use defaults if not provided
    if data_path is None:
        data_path = DEFAULT_DATA_PATH
    if model_output_path is None:
        model_output_path = DEFAULT_MODEL_PATH
    
    logger.info("=" * 70)
    logger.info("HEALTHCARE INSURANCE RISK PREDICTION - MODEL TRAINING")
    logger.info("=" * 70)
    
    # ========== STEP 1: LOAD CLEANED DATASET ==========
    logger.info("\n[1/7] Loading cleaned dataset...")
    try:
        df = pd.read_csv(data_path)
        logger.info(f"✓ Dataset loaded: {df.shape}")
    except FileNotFoundError:
        logger.error(f"✗ File not found: {data_path}")
        logger.error("Please run data_preprocessing.py first!")
        return
    
    # ========== STEP 2: SEPARATE FEATURES AND TARGET ==========
    logger.info("\n[2/7] Separating features (X) and target (y)...")
    
    if 'insured' not in df.columns:
        logger.error("✗ Target column 'insured' not found in dataset!")
        logger.error("Please run data_preprocessing.py first!")
        return
    
    # Target variable
    y = df['insured']
    
    # Features (all columns except 'insured')
    X = df.drop(columns=['insured'])
    
    logger.info(f"✓ Features shape: {X.shape}")
    logger.info(f"✓ Target shape: {y.shape}")
    logger.info(f"✓ Number of features: {X.shape[1]}")
    
    # Display class distribution
    class_counts = y.value_counts()
    logger.info(f"\n✓ Target distribution:")
    logger.info(f"  - Insured (1): {class_counts.get(1, 0)} ({class_counts.get(1, 0)/len(y)*100:.1f}%)")
    logger.info(f"  - Uninsured (0): {class_counts.get(0, 0)} ({class_counts.get(0, 0)/len(y)*100:.1f}%)")
    
    # ========== STEP 3: SPLIT DATA ==========
    logger.info("\n[3/7] Splitting data into train and test sets (80/20)...")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    logger.info(f"✓ Training set: {X_train.shape[0]} samples")
    logger.info(f"✓ Test set: {X_test.shape[0]} samples")
    
    # ========== STEP 4: TRAIN MODELS ==========
    logger.info("\n[4/7] Training machine learning models...")
    
    # Model 1: Logistic Regression (interpretable, best for reports)
    lr_model = _train_and_log(
        LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
        "Logistic Regression",
        X_train,
        y_train,
    )

    # Model 2: Decision Tree (interpretable, limited depth)
    dt_model = _train_and_log(
        DecisionTreeClassifier(max_depth=5, random_state=42, class_weight='balanced'),
        "Decision Tree",
        X_train,
        y_train,
    )

    models = {
        "Logistic Regression": lr_model,
        "Decision Tree": dt_model,
    }
    
    # ========== STEP 5: EVALUATE MODELS ==========
    logger.info("\n[5/7] Evaluating models...")
    
    results = []
    
    for model_name, model in models.items():
        logger.info(f"\n  → Evaluating {model_name}...")
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        results.append({
            'Model': model_name,
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1
        })
        
        logger.info(f"  ✓ Accuracy: {accuracy:.4f}")
        logger.info(f"  ✓ Precision: {precision:.4f}")
        logger.info(f"  ✓ Recall: {recall:.4f}")
        logger.info(f"  ✓ F1-Score: {f1:.4f}")
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        logger.info("  ✓ Confusion Matrix:")
        logger.info(f"     [[TN={cm[0][0]}, FP={cm[0][1]}],")
        logger.info(f"      [FN={cm[1][0]}, TP={cm[1][1]}]]")
    
    # ========== STEP 6: COMPARISON TABLE ==========
    logger.info("\n[6/7] Model Performance Comparison:")
    logger.info("=" * 70)
    
    results_df = pd.DataFrame(results)
    logger.info("\n" + results_df.to_string(index=False))
    
    # Select best model based on F1-Score
    best_model_idx = results_df['F1-Score'].idxmax()
    best_model_name = results_df.loc[best_model_idx, 'Model']
    best_model = models[best_model_name]
    
    logger.info(f"\n✓ Best model: {best_model_name}")
    logger.info(f"✓ F1-Score: {results_df.loc[best_model_idx, 'F1-Score']:.4f}")
    
    # ========== STEP 7: SAVE BEST MODEL ==========
    logger.info("\n[7/7] Saving best model...")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    
    # Save model
    joblib.dump(best_model, model_output_path)
    logger.info(f"✓ Model saved to: {model_output_path}")
    
    # Save feature names for later use
    feature_names_path = model_output_path.replace('.pkl', '_features.pkl')
    joblib.dump(X.columns.tolist(), feature_names_path)
    logger.info(f"✓ Feature names saved to: {feature_names_path}")
    
    # ========== FEATURE COEFFICIENTS ==========
    logger.info("\n" + "=" * 70)
    logger.info("FEATURE IMPORTANCE")
    logger.info("=" * 70)
    
    if best_model_name == 'Logistic Regression':
        # Get coefficients
        coefficients = best_model.coef_[0]
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Coefficient': coefficients,
            'Abs_Coefficient': np.abs(coefficients)
        }).sort_values('Abs_Coefficient', ascending=False)
        
        logger.info("\nTop 10 Most Important Features (Logistic Regression Coefficients):")
        logger.info("\n" + feature_importance.head(10)[['Feature', 'Coefficient']].to_string(index=False))
        
    elif best_model_name == 'Decision Tree':
        # Get feature importance
        importances = best_model.feature_importances_
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': importances
        }).sort_values('Importance', ascending=False)
        
        logger.info("\nTop 10 Most Important Features (Decision Tree):")
        logger.info("\n" + feature_importance.head(10).to_string(index=False))
    
    # ========== FINAL SUMMARY ==========
    logger.info("\n" + "=" * 70)
    logger.info("MODEL TRAINING COMPLETE")
    logger.info("=" * 70)
    logger.info(f"✓ Best model: {best_model_name}")
    logger.info(f"✓ Model saved: {model_output_path}")
    logger.info("✓ Ready for deployment!")
    
    return best_model, X.columns.tolist(), results_df


# --- Run training if this file is executed directly ---
if __name__ == "__main__":
    train_models()
