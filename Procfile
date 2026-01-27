web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8000}
dashboard: streamlit run dashboard.py --server.port=${PORT2:-8501} --server.address=0.0.0.0