
import pickle
import numpy as np
import sys

try:
    with open("my_best_hospital_readmission_model.pkl", "rb") as f:
        data = pickle.load(f)
    
    print(f"Array Shape: {data.shape}")
    
    item0 = data[0]
    print("--- Item 0 ---")
    print(f"Type: {type(item0)}")
    print(f"Size: {sys.getsizeof(item0)}")
    print(f"Dir: {dir(item0)}")
    
    # Check for underlying sklearn steps if it's a pipeline
    if hasattr(item0, 'steps'):
        print("Item 0 has steps:", item0.steps)
        
except Exception as e:
    print(f"Error: {e}")
