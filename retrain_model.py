import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Load Data
print("Loading primary.csv...")
df = pd.read_csv('primary.csv')

# 2. Preprocessing
print("Preprocessing...")
# Sort by County and Year to calculate lag
df = df.sort_values(by=['County', 'Year'])

# Feature Engineering
# Target: 30-day Readmission Rate (Consolidated)
# Feature 1: Last Year Rate
df['last_year_rate'] = df.groupby('County')['30-day Readmission Rate (Consolidated)'].shift(1)

# Feature 2: ICD Version (Ordinal)
# Assuming '10' in string implies ID 10, else 9. User mapped 1/0 usually?
# Let's inspect unique values if possible, but heuristic:
df['ICD Version(Ordinal)'] = df['ICD Version'].apply(lambda x: 1 if '10' in str(x) else 0)

# Feature 3: PCPI_log
df['PCPI_log'] = np.log(df['PCPI'])

# Feature 4: Total Admits people(log)
df['Total Admits people(log)'] = np.log(df['Total Admits (Consolidated)'])

# Feature 5: 30-day Readmits (Proportion)
# This column exists in primary.csv directly

# Drop first year (no last_year_rate)
df_model = df.dropna(subset=['last_year_rate', '30-day Readmits (Proportion)', 'PCPI_log', 'Total Admits people(log)'])

feature_cols = [
    '30-day Readmits (Proportion)', 
    'ICD Version(Ordinal)', 
    'PCPI_log', 
    'Total Admits people(log)', 
    'last_year_rate'
]
target_col = '30-day Readmission Rate (Consolidated)'

X = df_model[feature_cols]
y = df_model[target_col]

print(f"Training data shape: {X.shape}")

# 3. Train Model
# Using GradientBoosting for better performance on small tabular data
print("Training GradientBoostingRegressor...")
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
model.fit(X, y)

# 4. Evaluation
preds = model.predict(X)
mae = mean_absolute_error(y, preds)
r2 = r2_score(y, preds)
print(f"Training MAE: {mae:.4f}")
print(f"Training R2: {r2:.4f}")

# Save feature names for safety
model.feature_names_in_ = feature_cols

# 5. Save Model
output_path = 'my_best_hospital_readmission_model.pkl'
print(f"Saving model to {output_path}...")
with open(output_path, 'wb') as f:
    pickle.dump(model, f)

print("Done. This model is now trained on the actual primary.csv data.")
