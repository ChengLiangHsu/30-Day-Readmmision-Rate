# EquiCare Lens: Hospital Readmission Prediction & Strategy System

A specialized data science application for analyzing and improving hospital readmission rates in California. This system implements "Protocol 11" to ensure fair performance evaluation through peer-group clustering.

## Features

1.  **County Dashboard (Prediction)**: Predicts 30-day readmission risk based on county-level features.
2.  **Smart Lens (Clustering)**: Automatically classifies counties into peer groups (e.g., Urban Challenge vs. High Performance) to apply fair benchmarks.
3.  **Strategy Board (Prescription)**: Recommends specific interventions (Rx) based on the identified cluster and structural conditions.

## Project Structure

*   `backend/`: Python Flask API serving the ML models.
*   `frontend/`: Vue 3 + Vite specialized dashboard UI.
*   `hospital-readmission-rate.ipynb`: Original data science analysis.

## Setup & Running

### 1. Backend (Python)

Ensure you have Python installed and the required packages (`flask`, `flask-cors`, `pandas`, `scikit-learn`, `pickle`).

```bash
cd backend
python app.py
```

The server will start at `http://localhost:5000`.

### 2. Frontend (Vue.js)

Ensure you have Node.js installed.

```bash
cd frontend
npm install
npm run dev
```

The UI will be available at `http://localhost:5173` (or similar).

## "Smart Lens" Logic

The system uses a clustering heuristic derived from KMeans analysis:
*   **High Performance**: High Income, Low Readmission Rate.
*   **Resource Deprived**: Low Income, Low Population (Rural).
*   **Urban Challenge**: High Population, High Readmission Rate.
*   **Needs Improvement**: Moderate metrics.

When a county is selected on the dashboard, the system automatically determines its cluster and updates the Strategy Board.
