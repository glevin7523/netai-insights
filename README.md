## **📝 COMPLETE README.md FILE**

Here's the complete README.md file with your details:

```markdown
# 🚀 NetAI Insights - AI-Driven Network Analytics Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![Spark](https://img.shields.io/badge/Spark-3.5-orange.svg)
![ML](https://img.shields.io/badge/ML-Scikit--learn-red.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**AI-powered network monitoring system inspired by Juniper Mist**

[![Live Demo](https://img.shields.io/badge/Live_Demo-Available-brightgreen)](https://netai-insights.onrender.com)
[![API Docs](https://img.shields.io/badge/API_Docs-Interactive-orange)](https://netai-insights.onrender.com/api/docs)
[![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-blue)](https://netai-insights.streamlit.app)

</div>

## 📋 Overview

NetAI Insights is a comprehensive AI-driven network analytics platform that simulates, monitors, and analyzes network device logs using modern AI/ML techniques. The system is designed to optimize user experiences and simplify network operations through automated event correlation, root cause identification, and proactive anomaly detection.

**Built specifically for:** MTech (AIDE) – Juniper Mist internship role requirements

## ✨ Features

### 🤖 **AI/ML Powered**
- Real-time anomaly detection using Isolation Forest
- ML model explanations with actionable insights
- Automated network performance optimization
- Real-time prediction API for network metrics

### 📡 **Network Analytics**
- Multi-device support (APs, Switches, Routers, Firewalls)
- Real-time latency & failure analysis
- Security event monitoring
- Performance threshold detection
- Device health scoring and alerts

### ⚡ **Big Data Processing**
- Spark batch analytics (simulated with Pandas)
- Scalable data processing architecture
- Historical trend analysis
- Hourly traffic pattern analysis

### 🌐 **Modern Tech Stack**
- RESTful API with FastAPI (Swagger documentation)
- Interactive Streamlit dashboard with Plotly charts
- SQL database with SQLAlchemy
- Docker containerization ready
- Microservices architecture

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Streamlit UI   │    │   FastAPI API   │    │   Batch Process │
│  (Dashboard)    │◄──►│   (Real-time)   │◄──►│   (Analytics)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                          │         │                  │
                    ┌─────▼─────┐  ┌▼───────┐    ┌────▼────┐
                    │  SQL DB   │  │  ML    │    │  CSV    │
                    │ (SQLite)  │  │ Models │    │  Files  │
                    └───────────┘  └────────┘    └─────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git
- (Optional) Docker & Docker Compose

### Local Development

1. **Clone repository**
```bash
git clone https://github.com/glevin7523/netai-insights.git
cd netai-insights
```

2. **Setup virtual environment**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

3. **Generate sample data**
```bash
python app/log_simulator.py
```

4. **Start services**
```bash
# Terminal 1: Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Streamlit dashboard
streamlit run dashboard.py
```

5. **Access the application**
- **API Documentation**: http://localhost:8000/api/docs
- **Dashboard**: http://localhost:8501
- **Health Check**: http://localhost:8000/api/health

### Docker Deployment (Simplest)
```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at:
# API: http://localhost:8000
# Dashboard: http://localhost:8501
```

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/metrics/summary` | Network metrics summary |
| `GET` | `/api/devices` | List all network devices |
| `GET` | `/api/anomalies` | Get detected anomalies |
| `POST` | `/api/ml/detect` | Run ML anomaly detection |
| `GET` | `/api/ml/predict` | Real-time anomaly prediction |
| `GET` | `/api/ml/features` | Get ML model features |
| `POST` | `/api/spark/analyze` | Run batch analytics |

## 🎨 Dashboard Features

### 📊 **Overview Tab**
- Real-time network metrics
- Device distribution charts
- Latency analysis by device type
- Success rate monitoring

### 🏥 **Device Health Tab**
- Device health status cards
- Performance metrics per device
- Location-based device grouping
- Anomaly score visualization

### 🚨 **Anomalies Tab**
- Detected anomalies list
- Anomaly score distribution
- Event details and timestamps
- Source-destination mapping

### 🤖 **AI Insights Tab**
- Real-time anomaly prediction
- Interactive ML model testing
- Feature importance explanation
- Model training controls

### ⚡ **Batch Analytics Tab**
- Spark analysis results
- Performance issue detection
- Hourly traffic patterns
- Security event analysis

## 🎯 Project Alignment with Juniper Mist Requirements

### ✅ **Direct Matches from Job Description**
- **AI/ML Techniques**: Isolation Forest for proactive anomaly detection
- **Data Ingestion**: Network logs from APs, Switches, Firewalls (simulated)
- **Microservices Architecture**: FastAPI-based REST API
- **Big Data Technologies**: Spark batch processing simulation
- **Cloud Deployment**: Docker containerization for AWS/GCP
- **Network Protocols**: L2/L3 metrics, TCP retransmissions, VLAN monitoring

### ✅ **Technical Stack Compliance**
- **Python**: Primary programming language
- **FastAPI**: Design and implement APIs
- **Spark**: Foundation knowledge demonstrated
- **SQL**: Database operations
- **Streamlit**: Data visualization and dashboard

### ✅ **Work Domain Coverage**
- **Cloud Engineering / Analytics**: Complete analytics platform
- **Data Science**: ML-based anomaly detection
- **Routing & Switching**: Network-specific metrics
- **Security**: Security event monitoring

## 📁 Project Structure

```
netai-insights/
├── app/                    # Core application
│   ├── __init__.py
│   ├── main.py            # FastAPI application
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── data_service.py    # Data ingestion service
│   ├── log_simulator.py   # Network log generator
│   ├── ml_service.py      # AI/ML anomaly detection
│   └── spark_processor.py # Batch analytics (Spark simulation)
├── data/                  # Data files
│   ├── network_logs.csv   # Sample network data
│   ├── network_analytics.db # SQLite database
│   └── spark_output/      # Batch analysis results
├── dashboard.py           # Streamlit dashboard
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Multi-service deployment
├── Procfile             # Platform deployment
└── README.md            # This file
```

## 🛠️ Technologies Used

### **Backend & API**
- **FastAPI**: Modern, fast web framework for APIs
- **SQLAlchemy**: Database ORM and migrations
- **Uvicorn**: ASGI server for FastAPI
- **Pydantic**: Data validation and settings management

### **AI/ML & Data Processing**
- **Scikit-learn**: Machine learning algorithms
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Joblib**: Model persistence

### **Frontend & Visualization**
- **Streamlit**: Interactive web dashboard
- **Plotly**: Interactive charts and graphs
- **Requests**: HTTP client for API calls

### **DevOps & Deployment**
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Render/Heroku**: Cloud deployment platforms

## 📈 Sample Use Cases

### 1. **Network Health Monitoring**
- Real-time dashboard showing device performance metrics
- Automated alerts for high latency or packet loss
- Historical trend analysis for capacity planning

### 2. **Anomaly Detection & Investigation**
- AI identifies abnormal network behavior
- Detailed explanations for detected anomalies
- Root cause analysis for network issues

### 3. **Security Monitoring**
- Detection of suspicious network activities
- Security event correlation
- Firewall rule effectiveness analysis

### 4. **Performance Optimization**
- Identification of bottleneck devices
- Recommendations for network improvements
- Automated reporting for IT teams

## 🚀 Deployment

### Option 1: Deploy Everything on Render (Recommended)
1. Fork this repository to your GitHub account
2. Go to [render.com](https://render.com)
3. Sign up with GitHub
4. Create a new "Web Service"
5. Connect your GitHub repository
6. Configure:
   - **Name**: `netai-insights`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host=0.0.0.0 --port=$PORT`
7. Deploy!

### Option 2: Separate Deployment (API + Dashboard)

#### Deploy API on Render:
Follow steps above for API deployment

#### Deploy Dashboard on Streamlit Cloud:
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `glevin7523/netai-insights`
5. Select file: `dashboard.py`
6. Set API URL in dashboard code to your Render API URL
7. Deploy!

### Option 3: Docker Deployment
```bash
# Build Docker image
docker build -t netai-insights .

# Run container
docker run -p 8000:8000 -p 8501:8501 netai-insights

# Or use Docker Compose
docker-compose up
```

## 🔧 Configuration

### Environment Variables
```bash
# Database (for production)
DATABASE_URL=postgresql://user:password@host:port/database

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Dashboard
DASHBOARD_PORT=8501
API_BASE_URL=http://localhost:8000  # Change for production
```

## 🧪 Testing

Run the test scripts:
```bash
# Test API endpoints
python test_api.py

# Test ML functionality
python test_ml.py

# Test batch analytics
python test_spark.py
```

## 👨‍💻 Author

**Glevin Roche**  
📧 Email: [glevinroche@gmail.com](mailto:glevinroche@gmail.com)  
🔗 GitHub: [github.com/glevin7523](https://github.com/glevin7523)  
📂 Project Repository: [github.com/glevin7523/netai-insights](https://github.com/glevin7523/netai-insights)

### About the Author
MTech student specializing in AI & Data Engineering. Passionate about building intelligent systems that solve real-world problems. This project was developed as part of the application for Juniper Mist's AI-driven networking internship, demonstrating practical implementation of AI/ML techniques in network analytics.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by **Juniper Mist**'s AI-driven networking solutions
- Built for **MTech (AIDE) internship application**
- Thanks to the **open-source community** for amazing libraries
- Special thanks to **FastAPI**, **Streamlit**, and **Scikit-learn** teams

## 📚 References

1. Juniper Mist Job Description: AI-driven automation for network operations
2. Isolation Forest Algorithm: Liu, Fei Tony, Ting, Kai Ming, and Zhou, Zhi-Hua. "Isolation Forest." ICDM 2008.
3. FastAPI Documentation: https://fastapi.tiangolo.com
4. Streamlit Documentation: https://docs.streamlit.io

---

<div align="center">
  
### ⭐ **Star this repo if you find it useful!**

[![GitHub stars](https://img.shields.io/github/stars/glevin7523/netai-insights?style=social)](https://github.com/glevin7523/netai-insights/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/glevin7523/netai-insights?style=social)](https://github.com/glevin7523/netai-insights/network/members)

**Made with ❤️ by Glevin**

[Report Bug](https://github.com/glevin7523/netai-insights/issues) · 
[Request Feature](https://github.com/glevin7523/netai-insights/issues) · 
[View Demo](https://netai-insights.streamlit.app)

</div>
```