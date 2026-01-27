import sys

print("=== Checking Python Version ===")
print(f"Python {sys.version}")

try:
    import fastapi
    print("✓ FastAPI installed")
except ImportError:
    print("✗ FastAPI not installed")

try:
    import pandas
    print("✓ pandas installed")
except ImportError:
    print("✗ pandas not installed")

try:
    import sklearn
    print("✓ scikit-learn installed")
except ImportError:
    print("✗ scikit-learn not installed")

try:
    import pyspark
    print("✓ pyspark installed")
except ImportError:
    print("✗ pyspark not installed")

try:
    import streamlit
    print("✓ streamlit installed")
except ImportError:
    print("✗ streamlit not installed")

print("\n=== All Checks Complete ===")