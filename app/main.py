"""
Main FastAPI application for NetAI Insights
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

# Import local modules
from app.database import get_db, create_tables
from app.models import NetworkLog, DeviceMetrics, AnomalyDetection
from app.data_service import DataService
from app.spark_processor import run_batch_analysis
# Add these imports at the top of app/main.py
from app.ml_service import AnomalyDetectionService, AnomalyDetector
import pandas as pd
import logging

logger = logging.getLogger(__name__)
# Create FastAPI app
app = FastAPI(
    title="NetAI Insights API",
    description="AI-Driven Network Analytics Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables on startup
@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    create_tables()
    print("🚀 NetAI Insights API is starting up...")

# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Welcome to NetAI Insights API",
        "description": "AI-Driven Network Analytics Platform",
        "version": "1.0.0",
        "docs": "/api/docs",
        "endpoints": [
            "/api/health",
            "/api/ingest",
            "/api/metrics/summary",
            "/api/logs",
            "/api/devices",
            "/api/anomalies"
        ]
    }

@app.get("/api/health", tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2024-01-01T00:00:00Z"  # Replace with actual timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Data ingestion endpoints
@app.post("/api/ingest", tags=["Data Ingestion"])
async def ingest_data(
    csv_path: Optional[str] = Query("data/network_logs.csv", description="Path to CSV file"),
    db: Session = Depends(get_db)
):
    """
    Ingest network logs from CSV file into database
    """
    try:
        count = DataService.ingest_csv_to_db(db, csv_path)
        return {
            "message": "Data ingestion successful",
            "records_ingested": count,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data ingestion failed: {str(e)}")

# Analytics endpoints
@app.get("/api/metrics/summary", tags=["Analytics"])
async def get_metrics_summary(db: Session = Depends(get_db)):
    """
    Get summary metrics and statistics
    """
    try:
        stats = DataService.get_summary_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting metrics: {str(e)}")

@app.get("/api/logs", tags=["Logs"])
async def get_logs(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    device_id: Optional[str] = Query(None, description="Filter by device ID"),
    device_type: Optional[str] = Query(None, description="Filter by device type"),
    db: Session = Depends(get_db)
):
    """
    Get network logs with pagination and filtering
    """
    try:
        query = db.query(NetworkLog)
        
        # Apply filters
        if device_id:
            query = query.filter(NetworkLog.device_id == device_id)
        if device_type:
            query = query.filter(NetworkLog.device_type == device_type)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        logs = query.order_by(NetworkLog.timestamp.desc()).offset(skip).limit(limit).all()
        
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "logs": [log.to_dict() for log in logs]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching logs: {str(e)}")

@app.get("/api/devices", tags=["Devices"])
async def get_devices(
    db: Session = Depends(get_db)
):
    """
    Get list of unique devices and their stats
    """
    try:
        from sqlalchemy import func
        
        # Get unique devices with their latest stats
        devices = db.query(
            NetworkLog.device_id,
            NetworkLog.device_type,
            NetworkLog.device_model,
            NetworkLog.location,
            func.count(NetworkLog.id).label("total_logs"),
            func.avg(NetworkLog.latency_ms).label("avg_latency"),
            func.avg(NetworkLog.cpu_utilization).label("avg_cpu"),
            func.max(NetworkLog.anomaly_score).label("max_anomaly_score")
        ).group_by(
            NetworkLog.device_id,
            NetworkLog.device_type,
            NetworkLog.device_model,
            NetworkLog.location
        ).order_by(NetworkLog.device_id).all()
        
        device_list = []
        for device in devices:
            device_list.append({
                "device_id": device.device_id,
                "device_type": device.device_type,
                "device_model": device.device_model,
                "location": device.location,
                "total_logs": device.total_logs,
                "avg_latency": round(device.avg_latency, 2) if device.avg_latency else 0,
                "avg_cpu": round(device.avg_cpu, 2) if device.avg_cpu else 0,
                "max_anomaly_score": round(device.max_anomaly_score, 3) if device.max_anomaly_score else 0,
                "health_status": "healthy" if (device.max_anomaly_score or 0) < 0.7 else "warning"
            })
        
        return {
            "total_devices": len(device_list),
            "devices": device_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching devices: {str(e)}")

@app.get("/api/anomalies", tags=["Anomalies"])
async def get_anomalies(
    min_score: float = Query(0.7, ge=0.0, le=1.0, description="Minimum anomaly score"),
    limit: int = Query(50, ge=1, le=500, description="Number of anomalies to return"),
    db: Session = Depends(get_db)
):
    """
    Get detected anomalies based on anomaly score
    """
    try:
        anomalies = db.query(NetworkLog).filter(
            NetworkLog.anomaly_score >= min_score
        ).order_by(
            NetworkLog.anomaly_score.desc()
        ).limit(limit).all()
        
        anomaly_list = []
        for log in anomalies:
            anomaly_list.append({
                "timestamp": log.timestamp.isoformat() if log.timestamp else None,
                "device_id": log.device_id,
                "device_type": log.device_type,
                "event_type": log.event_type,
                "anomaly_score": round(log.anomaly_score, 3),
                "latency_ms": log.latency_ms,
                "cpu_utilization": log.cpu_utilization,
                "memory_utilization": log.memory_utilization,
                "tcp_retransmissions": log.tcp_retransmissions,
                "tags": log.tags,
                "details": {
                    "source_ip": log.source_ip,
                    "destination_ip": log.destination_ip,
                    "protocol": log.protocol,
                    "error_code": log.error_code
                }
            })
        
        return {
            "total_anomalies": len(anomaly_list),
            "min_score": min_score,
            "anomalies": anomaly_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching anomalies: {str(e)}")

# ML/AI Endpoints
@app.post("/api/ml/detect", tags=["Machine Learning"])
async def detect_anomalies(
    limit: int = Query(1000, ge=1, le=10000, description="Number of records to analyze"),
    model_type: str = Query("isolation_forest", description="Model type: isolation_forest, one_class_svm, dbscan"),
    db: Session = Depends(get_db)
):
    """
    Run AI/ML anomaly detection on network data
    """
    try:
        from app.ml_service import AnomalyDetectionService
        
        stats = AnomalyDetectionService.detect_anomalies_in_db(db, limit)
        
        return {
            "message": "Anomaly detection completed successfully",
            "model_type": model_type,
            "records_analyzed": limit,
            "statistics": stats,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anomaly detection failed: {str(e)}")

@app.get("/api/ml/predict", tags=["Machine Learning"])
async def predict_anomaly(
    latency: float = Query(..., description="Latency in ms"),
    jitter: float = Query(..., description="Jitter in ms"),
    packet_loss: float = Query(..., description="Packet loss percentage"),
    cpu_util: float = Query(..., description="CPU utilization percentage"),
    memory_util: float = Query(..., description="Memory utilization percentage"),
    tcp_retrans: int = Query(..., description="TCP retransmissions count"),
    client_count: int = Query(..., description="Number of clients"),
    throughput: float = Query(..., description="Throughput in Mbps")
):
    """
    Predict if network metrics indicate an anomaly (real-time prediction)
    """
    try:
        # Create sample data
        sample_data = {
            'latency_ms': [latency],
            'jitter_ms': [jitter],
            'packet_loss': [packet_loss],
            'cpu_utilization': [cpu_util],
            'memory_utilization': [memory_util],
            'tcp_retransmissions': [tcp_retrans],
            'client_count': [client_count],
            'throughput_mbps': [throughput]
        }
        
        df = pd.DataFrame(sample_data)
        
        # Load or create detector
        try:
            detector = AnomalyDetector.load_model("models/anomaly_detector.joblib")
        except:
            # If no saved model, create new one
            detector = AnomalyDetector(model_type="isolation_forest")
            # Need some data to fit - for demo, we'll use the sample
            detector.detect_anomalies(df)
        
        # Detect anomaly
        df_with_pred, _ = detector.detect_anomalies(df)
        
        is_anomaly = bool(df_with_pred.iloc[0]['is_anomaly_ml'])
        anomaly_score = float(df_with_pred.iloc[0]['anomaly_score_ml'])
        
        # Get explanation
        explanation = detector.explain_anomaly(df_with_pred.iloc[0].to_dict())
        
        return {
            "is_anomaly": is_anomaly,
            "anomaly_score": round(anomaly_score, 3),
            "confidence": round(1 - anomaly_score, 3) if is_anomaly else round(anomaly_score, 3),
            "explanation": explanation,
            "metrics_analyzed": list(sample_data.keys()),
            "model_type": detector.model_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/api/ml/features", tags=["Machine Learning"])
async def get_ml_features():
    """
    Get features used by ML model for anomaly detection
    """
    detector = AnomalyDetector()
    
    return {
        "model_type": detector.model_type,
        "features": detector.features,
        "description": "Network metrics used for anomaly detection",
        "feature_descriptions": {
            "latency_ms": "Network latency in milliseconds",
            "jitter_ms": "Packet delay variation in milliseconds",
            "packet_loss": "Percentage of packets lost",
            "cpu_utilization": "Device CPU usage percentage",
            "memory_utilization": "Device memory usage percentage",
            "tcp_retransmissions": "Number of TCP retransmissions",
            "client_count": "Number of connected clients",
            "throughput_mbps": "Network throughput in Mbps"
        }
    }

@app.post("/api/spark/analyze", tags=["Spark Analytics"])
async def spark_analysis(
    csv_path: str = Query("data/network_logs.csv", description="Path to CSV file")
):
    """
    Run batch analytics on network data (Spark simulation)
    """
    try:
        logger.info(f"Starting batch analysis on {csv_path}")
        
        # Run batch analysis
        results = run_batch_analysis()
        
        if "error" in results:
            raise HTTPException(status_code=500, detail=f"Batch analysis failed: {results['error']}")
        
        return {
            "message": "Batch analysis completed successfully",
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )