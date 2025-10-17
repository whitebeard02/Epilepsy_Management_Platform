# ml_workspace/tests/test_inference.py

import pytest
import pandas as pd
from datetime import datetime, timedelta

# Import the functions from your inference script
from ml_workspace.src.inference import create_features, predict

@pytest.fixture
def sample_raw_data():
    """Provides a sample 10-day DataFrame for testing."""
    dates = pd.to_datetime(pd.date_range(end=datetime.today(), periods=10, freq='D'))
    data = {
        'date': dates,
        'patient_id': 1,
        'hours_of_sleep': [7, 8, 5, 6, 7, 8, 9, 6, 5, 7],
        'stress_level': [2, 1, 4, 3, 2, 1, 1, 3, 4, 2],
        'medication_taken': [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
        'eeg_feature_1': [100, 90, 150, 120, 110, 95, 85, 130, 160, 105],
        'mri_lesion_present': [1] * 10,
    }
    return pd.DataFrame(data)

def test_create_features(sample_raw_data):
    """Unit test for the feature engineering function."""
    features_df = create_features(sample_raw_data)
    
    # Check that new columns have been added
    assert 'sleep_lag_1' in features_df.columns
    assert 'stress_rolling_avg_7' in features_df.columns
    
    # Check a specific lag value
    # The sleep on the 2nd to last day should be the lag value on the last day
    assert features_df['sleep_lag_1'].iloc[-1] == sample_raw_data['hours_of_sleep'].iloc[-2]

    # Check that the shape is correct (no rows dropped)
    assert len(features_df) == len(sample_raw_data)


def test_predict_integration(sample_raw_data):
    """Integration test for the full predict function."""
    # Convert DataFrame to the list of dicts format the function expects
    patient_history = sample_raw_data.to_dict('records')
    
    result = predict(patient_history)
    
    # --- Assert the output structure and types ---
    assert isinstance(result, dict)
    assert 'risk_score' in result
    assert 'feature_contributions' in result
    
    assert isinstance(result['risk_score'], float)
    assert 0.0 <= result['risk_score'] <= 1.0
    
    assert isinstance(result['feature_contributions'], dict)
    
    # Check that a key feature is present in the contributions
    assert 'hours_of_sleep' in result['feature_contributions']

def test_predict_insufficient_data():
    """Test that the function raises an error with insufficient data."""
    # Create a history with only 5 days of data
    short_history = [{'date': '2025-01-01', 'hours_of_sleep': 7}] * 5
    
    with pytest.raises(ValueError, match="Insufficient data"):
        predict(short_history)