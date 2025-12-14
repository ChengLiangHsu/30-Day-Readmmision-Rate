
import pickle
import numpy as np
import pandas as pd
import os

model_path = "my_best_hospital_readmission_model.pkl"

try:
    with open(model_path, "rb") as f:
        data = pickle.load(f)
    
    print(f"Loaded type: {type(data)}")
    
    if isinstance(data, np.ndarray):
        print(f"Shape: {data.shape}")
        for i, item in enumerate(data):
            print(f"--- Item {i} ---")
            print(f"Type: {type(item)}")
            # It seems like strings?
            if isinstance(item, str):
                print(f"Value: {item}")
            else:
                print(f"Value: {item}")
            
            # If it's a PyCaret Pipeline, it might be the first item
            
except Exception as e:
    print(f"Error: {e}")
