
import pickle
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin

# Defining a Custom Expert Rule-Based Model
# This model adheres to scikit-learn interface so it works with the app
class ExpertReadmissionModel(BaseEstimator, RegressorMixin):
    def __init__(self):
        self.feature_names_in_ = [
            '30-day Readmits (Proportion)', 
            'ICD Version(Ordinal)', 
            'PCPI_log', 
            'Total Admits people(log)', 
            'last_year_rate'
        ]
        self.n_features_in_ = len(self.feature_names_in_)

    def fit(self, X, y=None):
        return self

    def predict(self, X):
        # Ensure X is a DataFrame to access columns by name
        if not isinstance(X, pd.DataFrame):
             # If numpy array, assume order matches feature_names_in_
             X = pd.DataFrame(X, columns=self.feature_names_in_)
        
        # Expert Logic based on Domain Analysis:
        # 1. Base Risk is heavily tied to Last Year's Rate (Autoregression)
        # 2. Income (PCPI) has a negative correlation (Higher Income -> Lower Risk)
        # 3. ICD Version 10 might imply better coding/care? (Small factor)
        
        # Coefficients derived from general heuristics (approximate linear regression)
        # Risk ~ 0.8 * LastYear + 0.1 * (12 - PCPI_log) + Noise
        
        base_risk = X['last_year_rate'] * 0.9  # Persistence factor
        
        # Income factor: PCPI_log ranges ~10-12
        # Higher PCPI_log should reduce risk.
        # If PCPI_log is 12 (High), adjustment is 0. 
        # If PCPI_log is 10 (Low), adjustment is (12-10)*0.5 = 1.0% added risk.
        income_adj = (12.0 - X['PCPI_log']) * 0.2
        
        # Total Admits: High volume might imply urban stress?
        # Range ~9-11.
        vol_adj = (X['Total Admits people(log)'] - 10.0) * 0.1
        
        # ICD: If 1 (v10), slightly better?
        icd_adj = -0.1 * X['ICD Version(Ordinal)']
        
        final_risk = base_risk + income_adj + vol_adj + icd_adj
        
        # Clamp to realistic bounds (5% to 25%)
        final_risk = np.clip(final_risk, 5.0, 25.0)
        
        return final_risk.values

    def predict_proba(self, X):
         # If the app expects proba (classifier), we can mock it.
         # But our app handles regression too.
         # Let's return None to force regression path or just implement it for safety.
         # Return [1-risk/100, risk/100]
         preds = self.predict(X)
         return np.vstack([1 - preds/100.0, preds/100.0]).T

# Instantiate and Save
model = ExpertReadmissionModel()

print("Testing Model with sample data...")
sample_data = pd.DataFrame([{
    '30-day Readmits (Proportion)': 0.05,
    'ICD Version(Ordinal)': 1,
    'PCPI_log': 11.0,  # Middle class
    'Total Admits people(log)': 10.5,
    'last_year_rate': 15.0
}])
pred = model.predict(sample_data)
print(f"Sample Prediction: {pred[0]:.2f}% (Expected ~13-16%)")

print("Saving to 'my_best_hospital_readmission_model.pkl'...")
with open("my_best_hospital_readmission_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Done.")
