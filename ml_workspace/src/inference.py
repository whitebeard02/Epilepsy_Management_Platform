# ml_workspace/src/inference.py

import os
import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
from typing import List, Dict, Any

# --- Configuration ---
# Get the absolute path of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(os.path.dirname(BASE_DIR), 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'xgb_model_v1.0.json')
EXPLAINER_PATH = os.path.join(MODELS_DIR, 'shap_explainer_v1.0.joblib')

# --- Artifact Loading ---
try:
    model = xgb.Booster()
    model.load_model(MODEL_PATH)
    explainer = joblib.load(EXPLAINER_PATH)
except Exception as e:
    # Handle model loading errors gracefully in a real application
    # For now, we'll raise the exception to make debugging clear.
    print(f"Error loading model artifacts: {e}")
    model = None
    explainer = None

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates time-series features from raw data.
    """
    df_feat = df.copy()
    df_feat['date'] = pd.to_datetime(df_feat['date'])
    df_feat = df_feat.set_index('date')

    # Create Lag Features
    df_feat['sleep_lag_1'] = df_feat['hours_of_sleep'].shift(1)
    df_feat['stress_lag_1'] = df_feat['stress_level'].shift(1)
    df_feat['medication_lag_1'] = df_feat['medication_taken'].shift(1)
    df_feat['eeg_lag_1'] = df_feat['eeg_feature_1'].shift(1)

    # Create Rolling Window Features
    df_feat['sleep_rolling_avg_3'] = df_feat['hours_of_sleep'].rolling(window=3, min_periods=1).mean()
    df_feat['stress_rolling_avg_3'] = df_feat['stress_level'].rolling(window=3, min_periods=1).mean()
    df_feat['sleep_rolling_avg_7'] = df_feat['hours_of_sleep'].rolling(window=7, min_periods=1).mean()
    df_feat['stress_rolling_avg_7'] = df_feat['stress_level'].rolling(window=7, min_periods=1).mean()
    
    return df_feat

def predict(patient_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generates a risk score and explainability for a single prediction.
    
    Args:
        patient_history: A list of dictionaries, where each dictionary represents
                         one day of raw data. Must contain at least 8 days of data
                         (7 historical + 1 for the prediction day).
    
    Returns:
        A dictionary containing the risk score and feature contributions.
    """
    if not model or not explainer:
        raise RuntimeError("Model artifacts are not loaded. Cannot make predictions.")
    
    if len(patient_history) < 8:
        raise ValueError("Insufficient data. At least 8 days of history are required to generate features.")

    # --- 1. Data Preparation ---
    raw_df = pd.DataFrame(patient_history)

    # --- 2. Feature Engineering ---
    features_df = create_features(raw_df)
    
    # --- 3. Select Prediction Row and Features ---
    # The prediction is for the most recent day
    prediction_row = features_df.iloc[[-1]] 
    
    # Ensure columns are in the same order as the training data
    # We drop 'patient_id' as it's not a feature for the model
    feature_columns = model.feature_names
    X_pred = prediction_row[feature_columns]

    # --- 4. Prediction ---
    dmatrix_pred = xgb.DMatrix(X_pred)
    risk_score = model.predict(dmatrix_pred)[0]

    # --- 5. Explainability ---
    shap_values = explainer.shap_values(X_pred)
    
    # Format feature contributions into a user-friendly dictionary
    feature_contributions = {
        feature: round(float(shap_value), 4) 
        for feature, shap_value in zip(feature_columns, shap_values[0])
    }

    # Sort contributions by absolute impact
    sorted_contributions = dict(sorted(feature_contributions.items(), key=lambda item: abs(item[1]), reverse=True))

    return {
        "risk_score": round(float(risk_score), 4),
        "feature_contributions": sorted_contributions
    }