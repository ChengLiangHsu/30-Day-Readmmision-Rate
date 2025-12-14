
import json

file_path = "hospital-readmission-rate.ipynb"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            if "save_model" in source or "pickle.dump" in source or "to_pickle" in source:
                print("FOUND SAVE LOGIC:")
                print(source)
except Exception as e:
    print(e)
