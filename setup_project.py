#!/usr/bin/env python3
"""
Setup script for NetAI Insights
Creates all necessary files for GitHub deployment
"""
import os
import sys

def create_file(filepath, content):
    """Create a file with given content"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created {filepath}")

def main():
    print("🚀 Setting up NetAI Insights for GitHub deployment...")
    
    # Create .gitignore if not exists
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Data files (don't commit)
data/network_analytics.db
data/spark_output/
models/anomaly_detector.joblib
data/network_logs.csv
data/network_logs_sample.csv

# Logs
*.log
logs/

# Temp files
*.tmp
*.temp
"""
    create_file('.gitignore', gitignore_content)
    
    # Create requirements.txt if not exists
    requirements_content = """fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pandas==2.1.3
numpy==1.26.4
scikit-learn==1.3.2
joblib==1.3.2
streamlit==1.28.1
plotly==5.18.0
requests==2.31.0
python-multipart==0.0.6
"""
    create_file('requirements.txt', requirements_content)
    
    # Create runtime.txt for deployment platforms
    create_file('runtime.txt', 'python-3.9.18')
    
    print("\n✅ Project setup complete!")
    print("\n📋 Next steps:")
    print("1. git add .")
    print("2. git commit -m 'Your message'")
    print("3. git push origin main")
    print("4. Deploy to Streamlit Cloud: https://share.streamlit.io")

if __name__ == "__main__":
    main()