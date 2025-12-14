
# Define Model Class for Pickle Loading

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../my_best_hospital_readmission_model.pkl')
model = None

def load_model():
    global model
    try:
        # Check if file exists
        if not os.path.exists(MODEL_PATH):
            print(f"Error: Model not found at {MODEL_PATH}")
            return

        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")

load_model()
