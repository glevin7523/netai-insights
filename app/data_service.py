"""
Data ingestion and processing service
"""
import pandas as pd
from sqlalchemy.orm import Session
from app.models import NetworkLog
from datetime import datetime
import json
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class DataService:
    """Service for data ingestion and processing"""
    
    @staticmethod
    def ingest_csv_to_db(db: Session, csv_path: str = "data/network_logs.csv"):
        """
        Ingest CSV data into database
        """
        logger.info(f"Ingesting data from {csv_path}")
        
        try:
            # Read CSV file
            df = pd.read_csv(csv_path)
            logger.info(f"Read {len(df)} records from CSV")
            
            # Convert timestamp strings to datetime
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Insert records in batches
            batch_size = 100
            inserted_count = 0
            
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                batch_records = []
                
                for _, row in batch.iterrows():
                    # Convert row to dictionary
                    record_data = row.to_dict()
                    
                    # Handle tags conversion
                    if 'tags' in record_data and isinstance(record_data['tags'], str):
                        try:
                            # Try to parse as JSON
                            if record_data['tags'].startswith('['):
                                record_data['tags'] = json.loads(record_data['tags'])
                            else:
                                # Handle string representation of list
                                record_data['tags'] = eval(record_data['tags'])
                        except:
                            record_data['tags'] = []
                    
                    # Create NetworkLog object
                    network_log = NetworkLog(**record_data)
                    batch_records.append(network_log)
                
                # Bulk insert
                db.bulk_save_objects(batch_records)
                db.commit()
                
                inserted_count += len(batch_records)
                logger.info(f"Ingested {inserted_count}/{len(df)} records")
            
            logger.info(f"✅ Successfully ingested {inserted_count} records into database")
            return inserted_count
            
        except Exception as e:
            logger.error(f"❌ Error ingesting data: {e}")
            db.rollback()
            raise
    
    @staticmethod
    def get_summary_statistics(db: Session):
        """
        Get summary statistics from the database
        """
        from sqlalchemy import func, case
        
        try:
            # Total records
            total_logs = db.query(func.count(NetworkLog.id)).scalar() or 0
            
            # Success rate
            success_count = db.query(func.count(NetworkLog.id)).filter(NetworkLog.success == True).scalar() or 0
            success_rate = (success_count / total_logs * 100) if total_logs > 0 else 0
            
            # Device type distribution
            device_stats = db.query(
                NetworkLog.device_type,
                func.count(NetworkLog.id).label('count')
            ).group_by(NetworkLog.device_type).all()
            
            # Average latency by device type
            latency_stats = db.query(
                NetworkLog.device_type,
                func.avg(NetworkLog.latency_ms).label('avg_latency'),
                func.max(NetworkLog.latency_ms).label('max_latency'),
                func.min(NetworkLog.latency_ms).label('min_latency')
            ).group_by(NetworkLog.device_type).all()
            
            # Anomaly statistics
            anomaly_count = db.query(func.count(NetworkLog.id)).filter(
                NetworkLog.anomaly_score > 0.7
            ).scalar() or 0
            
            # Recent logs
            recent_logs = db.query(NetworkLog).order_by(NetworkLog.timestamp.desc()).limit(10).all()
            
            return {
                "total_logs": total_logs,
                "success_rate": round(success_rate, 2),
                "device_distribution": [
                    {"device_type": device, "count": count}
                    for device, count in device_stats
                ],
                "latency_stats": [
                    {
                        "device_type": device,
                        "avg_latency": round(avg, 2) if avg else 0,
                        "max_latency": round(max_val, 2) if max_val else 0,
                        "min_latency": round(min_val, 2) if min_val else 0
                    }
                    for device, avg, max_val, min_val in latency_stats
                ],
                "anomaly_count": anomaly_count,
                "anomaly_percentage": round((anomaly_count / total_logs * 100) if total_logs > 0 else 0, 2),
                "recent_logs": [log.to_dict() for log in recent_logs]
            }
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}