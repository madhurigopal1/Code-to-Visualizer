# Simple MLOps Dashboard (FastAPI + minimal frontend)

A single-page dashboard that can trigger evaluation runs for the example algorithms and show results.

Endpoints:
- GET /dashboard -> HTML page
- GET /api/algorithms -> list of available algorithms
- POST /api/run/{algorithm} -> runs training for the given algorithm and returns JSON metrics

