

import joblib
import pandas as pd
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def calculate_risk_score(user_data):
    """
    Calculate risk score using weighted scoring algorithm (Fuliza-like logic).
    
    Args:
        user_data: Dictionary containing user information
        
    Returns:
        tuple: (risk_score, risk_category)
    """
    score = 0
    
    # Income scoring (40 points max)
    income = user_data.get('Monthly Household Income', 0)
    if income < 10000:
        score += 40
    elif income <= 20000:
        score += 25
    
    # Employment status (20 points)
    employment = user_data.get('Employment Status', '')
    if employment in ['Unemployed', 'Self-employed']:
        score += 20
    
    # Routine checkup (30 points)
    routine_check = user_data.get('routine_check', 0)
    if routine_check == 0:
        score += 30
    
    # Age (10 points)
    age = user_data.get('Age', 0)
    if age >= 60:
        score += 10
    
    # Determine risk category
    if score >= 70:
        risk_category = "High Risk"
    elif score >= 40:
        risk_category = "Medium Risk"
    else:
        risk_category = "Low Risk"
    
    return score, risk_category


def get_insurance_recommendation(risk_category):
    """
    Get specific insurance recommendation based on risk category.
    
    Args:
        risk_category: Risk category (High Risk/Medium Risk/Low Risk)
        
    Returns:
        str: Specific recommendation
    """
    recommendations = {
        "High Risk": "Eligible for Government Social Protection & NHIF/SHA Subsidy",
        "Medium Risk": "Recommend Micro-insurance with weekly premium installments",
        "Low Risk": "Recommend Private Comprehensive Health Cover"
    }
    
    return recommendations.get(risk_category, "Contact insurance advisor for personalized plan")


class RiskAssessmentEngine:
    """
    Risk Assessment Engine for Healthcare Insurance Risk Prediction.
    Converts model predictions to actionable insights with recommendations.
    """
    
    def __init__(self, model_path="models/insurance_risk_model.pkl"):
        """
        Initialize the risk assessment engine.
        
        Args:
            model_path: Path to the trained model file
        """
        self.model_path = model_path
        self.feature_names_path = model_path.replace('.pkl', '_features.pkl')
        self.model = None
        self.feature_names = None
        
        self._load_model()
    
    def _load_model(self):
        """Load the trained model and feature names."""
        try:
            self.model = joblib.load(self.model_path)
            logger.info(f"✓ Model loaded from: {self.model_path}")
            
            # Load feature names
            if os.path.exists(self.feature_names_path):
                self.feature_names = joblib.load(self.feature_names_path)
                logger.info(f"✓ Feature names loaded: {len(self.feature_names)} features")
            else:
                logger.warning("⚠ Feature names file not found")
                
        except FileNotFoundError:
            logger.error(f"✗ Model file not found: {self.model_path}")
            logger.error("Please run model_training.py first!")
            raise
        except Exception as e:
            logger.error(f"✗ Error loading model: {e}")
            raise
    
    def prepare_input(self, user_data):
        """
        Prepare user input data for prediction.
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            DataFrame with proper feature encoding
        """
        # If feature names not available, use fallback feature list
        if self.feature_names is None:
            logger.warning("⚠ Feature names file missing, using fallback feature list")
            # Use model's expected features if available
            if hasattr(self.model, 'n_features_in_'):
                # Can't infer names from model, use hardcoded fallback
                features = [
                    'Age',
                    'Monthly Household Income',
                    'How many children do you have, if any?',
                    'When was the last time you visited a hospital for medical treatment? (In Months)',
                    'Have you ever had a routine check-up with a doctor or healthcare provider?_Yes',
                    'Have you ever had a cancer screening (e.g. mammogram, colonoscopy, etc.)?_Yes',
                    'Gender_Female', 'Gender_Male',
                    'Marital Status_Divorced', 'Marital Status_Married', 'Marital Status_Separated', 'Marital Status_Single', 'Marital Status_Widowed',
                    'Employment Status_Casual labor', 'Employment Status_Employed', 'Employment Status_Self-employed', 'Employment Status_Student', 'Employment Status_Unemployed'
                ]
            else:
                logger.error("✗ Cannot determine model features")
                return None
        else:
            features = self.feature_names
        
        # Create a DataFrame with zeros for all features (one-hot encoded)
        input_df = pd.DataFrame(0, index=[0], columns=features)
        
        # Map numerical features directly
        numerical_mappings = {
            'Age': 'Age',
            'Monthly Household Income': 'Monthly Household Income',
            'num_children': 'How many children do you have, if any?',
            'hospital_visit_gap': 'When was the last time you visited a hospital for medical treatment? (In Months)',
            # Binary checkup flags map to the one-hot encoded feature columns used during training
            'routine_check': 'Have you ever had a routine check-up with a doctor or healthcare provider?_Yes',
            'cancer_screening': 'Have you ever had a cancer screening (e.g. mammogram, colonoscopy, etc.)?_Yes',
        }
        
        for user_key, feature_key in numerical_mappings.items():
            if user_key in user_data and feature_key in input_df.columns:
                try:
                    input_df[feature_key] = float(user_data[user_key])
                    logger.debug(f"Set {feature_key} = {user_data[user_key]}")
                except (ValueError, TypeError) as e:
                    logger.warning(f"⚠ Could not convert {user_key} to float: {e}")
            elif user_key in user_data:
                logger.warning(f"⚠ Feature '{feature_key}' not found in model features")
        
        # Map categorical features with one-hot encoding
        categorical_mappings = {
            'Gender': 'Gender',
            'Marital Status': 'Marital Status',
            'Employment Status': 'Employment Status'
        }
        
        for user_key, feature_prefix in categorical_mappings.items():
            if user_key in user_data:
                value = user_data[user_key]
                
                # Handle Employment Status mapping for missing categories
                if user_key == 'Employment Status' and value not in features:
                    # Map missing employment values to available ones
                    employment_mapping = {
                        'Employed': 'Self-employed',  # Map Employed to Self-employed as closest match
                        'Student': 'Unemployed',  # Students treated as unemployed for model
                        'Retired': 'Unemployed',  # Retirees treated as unemployed for model
                        'Casual labor': 'Self-employed'  # Casual labor similar to self-employed
                    }
                    if value in employment_mapping:
                        value = employment_mapping[value]
                        logger.info(f"Mapped employment '{user_data[user_key]}' to '{value}'")
                
                # Create the one-hot encoded column name
                encoded_col = f"{feature_prefix}_{value}"
                if encoded_col in input_df.columns:
                    input_df[encoded_col] = 1
                    logger.debug(f"Set {encoded_col} = 1")
                else:
                    logger.warning(f"⚠ Feature '{encoded_col}' not found in model features")
                    # Try to find similar features
                    similar = [col for col in input_df.columns if feature_prefix in col]
                    if similar:
                        logger.warning(f"  Available {feature_prefix} options: {similar}")
        
        
        logger.info(f"Prepared input shape: {input_df.shape}, non-zero features: {input_df.sum().sum()}")
        return input_df
    
    def predict_risk(self, user_data):
        """
        Predict insurance risk for a given user.
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            Dictionary with risk assessment results
        """
        try:
            # Check if model is loaded
            if self.model is None:
                logger.error("✗ Model not loaded. Initialization failed.")
                return {
                    "error": "Model not available - initialization failed",
                    "risk_level": "Unknown",
                    "probability": 0.0,
                    "insurance_likelihood": 0.0,
                    "reasons": [],
                    "recommendations": [],
                    "eligible_insurance": [],
                    "interpretation": "Model is not available. Please contact administrator.",
                    "rule_based_score": 0,
                    "rule_based_category": "Unknown",
                    "rule_based_recommendation": "Contact support."
                }
            
            if self.feature_names is None:
                logger.warning("⚠ Feature names not loaded, attempting prediction anyway")
            
            # Prepare input
            input_df = self.prepare_input(user_data)
            
            if input_df is None:
                logger.error("✗ Could not prepare input dataframe")
                return {
                    "error": "Could not prepare input data",
                    "risk_level": "Unknown",
                    "probability": 0.0,
                    "insurance_likelihood": 0.0,
                    "reasons": [],
                    "recommendations": [],
                    "eligible_insurance": [],
                    "interpretation": "Unable to process your information.",
                    "rule_based_score": 0,
                    "rule_based_category": "Unknown",
                    "rule_based_recommendation": "Please try again with valid information."
                }
            
            logger.info(f"Input features shape: {input_df.shape}")
            logger.info(f"Model expects {self.model.n_features_in_ if hasattr(self.model, 'n_features_in_') else 'unknown'} features")
            logger.info(f"Input has {len(input_df.columns)} features")
            
            # Predict probability using class labels for robustness
            # Classes: 0 = uninsured, 1 = insured
            try:
                logger.info(f"Model classes: {self.model.classes_}")
                proba = self.model.predict_proba(input_df)[0]
                logger.info(f"Prediction probabilities: {proba}")
                class_insured_idx = list(self.model.classes_).index(1) if 1 in self.model.classes_ else 1
                prob_insured = proba[class_insured_idx]
                prob_uninsured = 1 - prob_insured
            except Exception as e:
                logger.error(f"✗ Error during model prediction: {e}")
                return {
                    "error": f"Model prediction failed: {str(e)}",
                    "risk_level": "Unknown",
                    "probability": 0.0,
                    "insurance_likelihood": 0.0,
                    "reasons": [],
                    "recommendations": [],
                    "eligible_insurance": [],
                    "interpretation": "Model prediction failed. Please try again later.",
                    "rule_based_score": 0,
                    "rule_based_category": "Unknown",
                    "rule_based_recommendation": "Contact support if the issue persists."
                }
            
            # Classify risk level based on uninsured probability
            risk_level = self._classify_risk(prob_uninsured)
            
            # Identify risk factors
            try:
                risk_factors = self._identify_risk_factors(user_data, prob_uninsured)
            except Exception as e:
                logger.warning(f"⚠ Error identifying risk factors: {e}")
                risk_factors = []
            
            # Get recommendations
            try:
                recommendations = self._get_recommendations(risk_level, risk_factors, user_data)
            except Exception as e:
                logger.warning(f"⚠ Error getting recommendations: {e}")
                recommendations = []
            
            # Get eligible insurance options
            try:
                eligible_insurance = self._get_eligible_insurance(user_data, risk_level)
            except Exception as e:
                logger.warning(f"⚠ Error getting eligible insurance: {e}")
                eligible_insurance = []
            
            # Calculate rule-based risk score (Fuliza-like logic)
            try:
                rule_score, rule_category = calculate_risk_score(user_data)
                rule_recommendation = get_insurance_recommendation(rule_category)
            except Exception as e:
                logger.warning(f"⚠ Error calculating rule-based score: {e}")
                rule_score = 0
                rule_category = "Unknown"
                rule_recommendation = "Contact support"
            
            # Get interpretation
            try:
                interpretation = self._get_interpretation(risk_level, prob_uninsured)
            except Exception as e:
                logger.warning(f"⚠ Error getting interpretation: {e}")
                interpretation = f"Assessment complete. Risk level: {risk_level}"
            
            # Build response with both ML and rule-based insights
            return {
                "risk_level": risk_level,
                "probability": float(round(prob_uninsured * 100, 2)),  # Probability of being uninsured
                "insurance_likelihood": float(round(prob_insured * 100, 2)),  # Probability of being insured (for display)
                "reasons": risk_factors,
                "recommendations": recommendations,
                "eligible_insurance": eligible_insurance,
                "interpretation": interpretation,
                "rule_based_score": int(rule_score),
                "rule_based_category": rule_category,
                "rule_based_recommendation": rule_recommendation
            }
            
        except Exception as e:
            import traceback
            logger.error(f"✗ Unexpected error during prediction: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                "error": str(e),
                "risk_level": "Unknown",
                "probability": 0.0,
                "insurance_likelihood": 0.0,
                "reasons": [],
                "recommendations": [],
                "eligible_insurance": [],
                "interpretation": f"An unexpected error occurred. Please contact support.",
                "rule_based_score": 0,
                "rule_based_category": "Unknown",
                "rule_based_recommendation": "Please contact support."
            }
    
    def _classify_risk(self, probability):
        """
        Classify risk level based on probability.
        
        Args:
            probability: Probability of being uninsured (0-1)
            
        Returns:
            Risk level string
        """
        if probability < 0.3:
            return "Low Risk"
        elif probability < 0.6:
            return "Medium Risk"
        else:
            return "High Risk"
    
    def _identify_risk_factors(self, user_data, probability):
        """
        Identify top contributing risk factors based on user data.
        
        Args:
            user_data: Dictionary with user information
            probability: Predicted probability
            
        Returns:
            List of risk factor descriptions
        """
        risk_factors = []
        
        # Check income
        income = user_data.get('Monthly Household Income', 0)
        if income < 15000:
            risk_factors.append("Very low household income (below 15,000 KES)")
        elif income < 25000:
            risk_factors.append("Low household income (below 25,000 KES)")
        
        # Check employment status
        employment = user_data.get('Employment Status', '')
        if employment in ['Unemployed', 'Casual labor']:
            risk_factors.append(f"Unstable employment status ({employment})")
        
        # Check education level
        education = user_data.get('education_level', '')
        if education in ['No formal education', 'Primary']:
            risk_factors.append(f"Limited education level ({education})")
        
        # Check chronic illness
        chronic = user_data.get('chronic_illness', 'None')
        if chronic != 'None':
            risk_factors.append(f"Chronic health condition present ({chronic})")
        
        # Check healthcare knowledge
        knowledge = user_data.get('healthcare_knowledge', '')
        if knowledge in ['No knowledge', 'Basic']:
            risk_factors.append("Limited healthcare insurance knowledge")
        
        # Check family size vs income
        family_size = user_data.get('family_size', 1)
        if family_size > 5 and income < 40000:
            risk_factors.append(f"Large family size ({int(family_size)}) with limited income")
        
        # Check number of children
        children = user_data.get('num_children', 0)
        if children > 4:
            risk_factors.append(f"Many dependents ({int(children)} children)")
        
        # Check preventive care score
        preventive_score = user_data.get('preventive_care_score', 0)
        if preventive_score == 0:
            risk_factors.append("No preventive care history (no checkups or screenings)")
        elif preventive_score < 2:
            risk_factors.append("Minimal preventive care engagement")
        
        # Check hospital visit gap
        visit_gap = user_data.get('hospital_visit_gap', 0)
        if visit_gap > 24:
            risk_factors.append("No recent hospital visits (more than 2 years ago)")
        elif visit_gap > 12:
            risk_factors.append("Infrequent healthcare access (last visit over 1 year ago)")
        
        # Check residence type
        residence = user_data.get('residence_type', '')
        if residence == 'Rural':
            risk_factors.append("Rural residence (limited healthcare access)")
        
        # Check age
        age = user_data.get('Age', 0)
        if age < 25:
            risk_factors.append("Young adult age group (lower insurance awareness)")
        elif age > 60:
            risk_factors.append("Elderly age group (higher healthcare needs)")
        
        # Check marital status
        marital = user_data.get('Marital Status', '')
        if marital == 'Single' and children > 0:
            risk_factors.append("Single parent household")
        
        # If no specific factors identified but high risk
        if not risk_factors and probability > 0.5:
            risk_factors.append("Multiple demographic and socioeconomic factors")
        
        # Return top 6 factors
        return risk_factors[:5]  # Return top 5 factors
    
    def _get_recommendations(self, risk_level, risk_factors, user_data):
        """
        Generate recommendations based on risk level and factors.
        
        Args:
            risk_level: Risk level classification
            risk_factors: List of identified risk factors
            user_data: Original user data
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # General recommendations by risk level
        if risk_level == "High Risk":
            recommendations.extend([
                " Enroll in National Hospital Insurance Fund (NHIF) immediately",
                " Apply for subsidized insurance programs for low-income households",
                " Register for the Chronic Illness Fund to manage pre-existing conditions",
                " Prioritize visits to Level 4 or 5 hospitals for specialized care",
                " Connect with a local Community Health Promoter (CHP) for home-based monitoring",
                " Verify eligibility for the Essential Drug List to access subsidized medication"
            ])
        
        if risk_level in ["High Risk", "Medium Risk"]:
            recommendations.extend([
                " Explore community-based health insurance options",
                " Consider family-based insurance packages for better coverage",
                " Map out the nearest SHIF-accredited facilities for quick access",
                " Evaluate private 'Top-up' covers to supplement basic SHA benefits",
                " Explore SACCO-based medical savings products as a secondary safety net",
                " Start a digital health folder to track screenings and diagnostic history"
            ])
        
        # Specific recommendations based on risk factors
        for factor in risk_factors:
            factor_lower = factor.lower()

            if "low" in factor_lower and "income" in factor_lower:
                recommendations.append(" Seek government subsidies or income-based insurance plans")
            
            if "unemployed" in factor_lower or "employment" in factor_lower:
                recommendations.append(" Join cooperative insurance schemes or community health funds")
            
            if "preventive care" in factor_lower or "routine" in factor_lower:
                recommendations.extend([
                    "🩺 Schedule regular health checkups to detect issues early",
                    " Learn about preventive healthcare and available screening programs"
                ])
            
            if "hospital visit" in factor_lower:
                recommendations.append(" Visit nearby health facilities for routine wellness checks")
            
            if "family size" in factor_lower or "children" in factor_lower:
                recommendations.append(" Explore family health insurance plans with dependent coverage")
            
            if "rural" in factor_lower or "location" in factor_lower:
                recommendations.append(" Access mobile clinic services and rural health programs")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recommendations.append(rec)
        
        return unique_recommendations[:6]  # Return top 6 recommendations
    
    def _get_eligible_insurance(self, user_data, risk_level):
        """
        Recommend specific insurance providers based on user profile.
        Uses actual insurance types from the training dataset.
        
        Args:
            user_data: Dictionary with user information
            risk_level: Assessed risk level
            
        Returns:
            List of dictionaries with insurance recommendations
        """
        eligible_options = []
        
        income = user_data.get('Monthly Household Income', 0)
        employment = user_data.get('Employment Status', '')
        age = user_data.get('Age', 0)
        chronic = user_data.get('chronic_illness', 'None')
        
        # NHIF (National Hospital Insurance Fund) - Government scheme
        # Most common in dataset (5325 people), suitable for all Kenyans
        nhif_reason = "Government-mandated health insurance for all Kenyans"
        if employment == 'Employed':
            nhif_reason = "Mandatory for employed individuals, contributions deducted from salary"
        elif income < 30000:
            nhif_reason = "Affordable premiums starting from KES 500/month for low-income earners"
        
        eligible_options.append({
            'name': 'NHIF/SHA (Social Health Authority)',
            'priority': 'High Priority',
            'reason': nhif_reason,
            'coverage': 'Outpatient, inpatient, maternity, surgery',
            'estimated_cost': 'KES 500 - 1,700/month based on income',
            'website': 'https://sha.go.ke',
            'learn_more': '/blog#nhif-guide'
        })
        
        # Linda Mama - Free maternity program
        if user_data.get('Gender', '') == 'Female' and 18 <= age <= 49:
            eligible_options.append({
                'name': 'Linda Mama Program',
                'priority': 'High Priority',
                'reason': 'Free maternity services for all expectant mothers',
                'coverage': 'Antenatal care, delivery, postnatal care',
                'estimated_cost': 'FREE (Government-funded)',
                'website': 'https://kmhfl.health.go.ke',
                'learn_more': '/blog#linda-mama-info'
            })
        
        # Private insurance recommendations based on income
        if income >= 40000:
            # Britam (125 people in dataset) and Jubilee (149 people in dataset)
            eligible_options.extend([
                {
                    'name': 'Britam Insurance',
                    'priority': 'Recommended',
                    'reason': 'Comprehensive private cover for middle to high-income earners',
                    'coverage': 'Inpatient, outpatient, dental, optical, maternity',
                    'estimated_cost': 'KES 3,000 - 15,000/month',
                    'website': 'https://www.britam.com',
                    'learn_more': '/blog#private-insurance-comparison'
                },
                {
                    'name': 'Jubilee Insurance',
                    'priority': 'Recommended',
                    'reason': 'Wide network of hospitals, good for families',
                    'coverage': 'Comprehensive medical, dental, optical',
                    'estimated_cost': 'KES 3,500 - 12,000/month',
                    'website': 'https://www.jubileeinsurance.com/ke',
                    'learn_more': '/blog#family-insurance-plans'
                }
            ])
        
        if income >= 50000 or employment == 'Employed':
            # APA Insurance (108 people in dataset)
            eligible_options.append({
                'name': 'APA Insurance',
                'priority': 'Recommended',
                'reason': 'Quality coverage with good claim settlement',
                'coverage': 'Inpatient, outpatient, emergency, chronic illness',
                'estimated_cost': 'KES 4,000 - 18,000/month',
                'website': 'https://www.apainsurance.org',
                'learn_more': '/blog#apa-insurance-review'
            })
            
            # CIC Insurance (54 people in dataset)
            if chronic != 'None' or age > 50:
                eligible_options.append({
                    'name': 'CIC Insurance',
                    'priority': 'Recommended',
                    'reason': 'Good for chronic conditions and elderly care',
                    'coverage': 'Comprehensive including chronic disease management',
                    'estimated_cost': 'KES 3,500 - 16,000/month',
                    'website': 'https://www.cicinsurancegroup.com',
                    'learn_more': '/blog#chronic-illness-coverage'
                })
        
        if income >= 30000 and income < 50000:
            # Madison Insurance (56 people in dataset)
            eligible_options.append({
                'name': 'Madison Insurance',
                'priority': 'Affordable Option',
                'reason': 'Mid-range coverage for middle-income families',
                'coverage': 'Inpatient, outpatient, maternity',
                'estimated_cost': 'KES 2,500 - 8,000/month',
                'website': 'https://www.madison.co.ke',
                'learn_more': '/blog#affordable-insurance-options'
            })
        
        if income >= 60000 or employment in ['Employed', 'Self-employed']:
            # AAR Insurance (25 people in dataset)
            eligible_options.append({
                'name': 'AAR Insurance',
                'priority': 'Premium Option',
                'reason': 'Premium coverage with international hospitals',
                'coverage': 'Comprehensive with worldwide coverage',
                'estimated_cost': 'KES 5,000 - 25,000/month',
                'website': 'https://www.aar-insurance.com',
                'learn_more': '/blog#premium-health-coverage'
            })
        
        # Community-based options for low income
        if income < 25000 or employment in ['Unemployed', 'Casual labor']:
            eligible_options.append({
                'name': 'Community-Based Health Insurance',
                'priority': 'Affordable Option',
                'reason': 'Low-cost cooperative health schemes for low-income households',
                'coverage': 'Basic inpatient and outpatient care',
                'estimated_cost': 'KES 300 - 1,000/month',
                'website': 'https://www.who.int/news-room/fact-sheets/detail/community-based-health-insurance-CBHI',
                'learn_more': '/blog#community-insurance-schemes'
            })
        
        # Family packages for large families
        family_size = user_data.get('family_size', 1)
        children = user_data.get('num_children', 0)
        if family_size > 4 or children > 2:
            eligible_options.append({
                'name': 'Family Health Package (Various Providers)',
                'priority': 'Recommended',
                'reason': f'Covers all {int(family_size)} family members under one policy',
                'coverage': 'Depends on provider (NHIF, Britam, Jubilee offer family plans)',
                'estimated_cost': 'KES 4,000 - 20,000/month for entire family',
                'website': 'https://www.nhif.or.ke/family-cover',
                'learn_more': '/blog#family-insurance-guide'
            })
        
        return eligible_options
    
    def _get_interpretation(self, risk_level, probability):
        """
        Generate human-readable interpretation of the risk assessment.
        
        Args:
            risk_level: Risk level classification
            probability: Probability value
            
        Returns:
            Interpretation string
        """
        prob_insured = (1 - probability) * 100
        
        if risk_level == "Low Risk":
            return f"You have a {prob_insured:.1f}% likelihood of obtaining insurance coverage. Your socioeconomic and healthcare access factors are favorable. Continue maintaining regular healthcare access and consider comprehensive coverage options."
        
        elif risk_level == "Medium Risk":
            return f"You have a {prob_insured:.1f}% likelihood of obtaining insurance coverage. Some factors may affect your insurance access. Explore affordable insurance options like NHIF/SHA and more others as indicated in the options below"
        
        else:  # High Risk
            return f"You have a {prob_insured:.1f}% likelihood of obtaining insurance coverage without assistance. Multiple factors indicate you may benefit from government subsidies and social protection programs. Immediate enrollment in government insurance programs with subsidy is recommended."


def assess_risk(user_data, model_path="models/insurance_risk_model.pkl"):
    """
    Standalone function to assess insurance risk.
    
    Args:
        user_data: Dictionary with user information
        model_path: Path to trained model
        
    Returns:
        Risk assessment results
    """
    engine = RiskAssessmentEngine(model_path)
    return engine.predict_risk(user_data)


# --- Test the engine if this file is executed directly ---
if __name__ == "__main__":
    # Example test data
    test_user = {
        'Age': 28,
        'Monthly Household Income': 15000,
        'Employment Status': 'Casual labor',
        'num_children': 2,
        'Marital Status': 'Single',
        'hospital_visit_gap': 18,
        'preventive_care_score': 0,
        'routine_check': 0,
        'cancer_screening': 0
    }
    
    logger.info("Testing Risk Assessment Engine...")
    logger.info("=" * 60)
    
    result = assess_risk(test_user)
    
    logger.info(f"\nRisk Level: {result['risk_level']}")
    logger.info(f"Probability: {result['probability']}%")
    logger.info(f"\nRisk Factors:")
    for factor in result['reasons']:
        logger.info(f"  - {factor}")
    logger.info(f"\nRecommendations:")
    for rec in result['recommendations']:
        logger.info(f"  {rec}")
