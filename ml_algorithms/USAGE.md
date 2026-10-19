# Update README with instructions for MLOps dashboard and ML examples

Added ML algorithm examples (15) and a prototype single-page MLOps Dashboard.

How to run the dashboard locally
1. Install requirements:
   pip install -r requirements_ml.txt
2. Run the dashboard:
   uvicorn dashboard.app:app --reload --port 9000
3. Open http://localhost:9000/dashboard

Notes
- The dashboard dynamically discovers modules under ml_algorithms and calls train_and_eval() on demand. Use it for quick prototype testing only (not production).
