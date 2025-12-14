
import pandas as pd
import pickle
import numpy as np

# Check CSV
try:
    df = pd.read_csv("primary.csv")
    print("CSV Columns:", df.columns.tolist())
except:
    print("CSV not found in current dir, trying default path")
    try:
        df = pd.read_csv("/kaggle/input/hospital-readmission-rates-in-california/primary.csv") # Path from notebook
    except:
        print("Cannot find CSV")

# Check Broken Pickle
try:
    with open("my_best_hospital_readmission_model.pkl", "rb") as f:
        data = pickle.load(f)
    print("Pickle Content:", data)
except Exception as e:
    print("Pickle check failed:", e)
