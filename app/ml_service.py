"""
Machine Learning service for anomaly detection
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.svm import OneClassSVM
import joblib
import json
from datetime import datetime
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class AnomalyDetector:
    """
    AI-based anomaly detection for network logs
    """
    
    def __init__(self, model_type: str = "isolation_forest"):
        """
        Initialize anomaly detector
        
        Args:
            model_type: 'isolation_forest', 'one_class_svm', or 'dbscan'
        """
        self.model_type = model_type
        self.scaler = StandardScaler()
        self.model = None
        self.features = [
            'latency_ms', 
            'jitter_ms',
            'packet_loss',
            'cpu_utilization',
            'memory_utilization',
            'tcp_retransmissions',
            'client_count',
            'throughput_mbps'
        ]
        
        # Initialize model based on type
        if model_type == "isolation_forest":
            self.model = IsolationForest(
                n_estimators=100,
                contamination=0.1,  # Expected anomaly proportion
                random_state=42,
                n_jobs=-1
            )
        elif model_type == "one_class_svm":
            self.model = OneClassSVM(
                nu=0.1,  # Expected anomaly proportion
                kernel="rbf",
                gamma="auto"
            )
        elif model_type == "dbscan":
            self.model = DBSCAN(
                eps=0.5,
                min_samples=10,
                metric="euclidean"
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        logger.info(f"Initialized {model_type} anomaly detector")
    
    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """
        Prepare features for anomaly detection
        """
        # Select and fill missing values
        X = df[self.features].copy()
        X = X.fillna(X.median())
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled
    
    def detect_anomalies(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        Detect anomalies in network data
        
        Returns:
            DataFrame with anomaly predictions and scores
            Dictionary with anomaly statistics
        """

        if 'is_anomaly_ml' not in df.columns:
            df['is_anomaly_ml'] = False
            df['anomaly_score_ml'] = 0.0

        if len(df) < 10:
            logger.warning(f"Insufficient data: {len(df)} records")
            return df, {}
        
        # Prepare features
        X = self.prepare_features(df)
        
        # Make predictions based on model type
        if self.model_type in ["isolation_forest", "one_class_svm"]:
            predictions = self.model.fit_predict(X)
            # Convert to anomaly scores (1 = normal, -1 = anomaly for Isolation Forest)
            if self.model_type == "isolation_forest":
                anomaly_scores = self.model.decision_function(X)
                # Convert to 0-1 scale where higher = more anomalous
                df['anomaly_score_ml'] = 1 - ((anomaly_scores - anomaly_scores.min()) / 
                                            (anomaly_scores.max() - anomaly_scores.min()))
                df['is_anomaly_ml'] = predictions == -1
            else:  # one_class_svm
                df['is_anomaly_ml'] = predictions == -1
                df['anomaly_score_ml'] = self.model.decision_function(X)
                
        elif self.model_type == "dbscan":
            predictions = self.model.fit_predict(X)
            # In DBSCAN, -1 = anomaly, others = cluster labels
            df['is_anomaly_ml'] = predictions == -1
            df['anomaly_score_ml'] = np.where(predictions == -1, 0.8, 0.2)
        
        # Calculate anomaly statistics
        anomaly_stats = self._calculate_anomaly_statistics(df)
        
        logger.info(f"Detected {anomaly_stats['total_anomalies']} anomalies "
                   f"({anomaly_stats['anomaly_percentage']:.2f}%)")
        
        return df, anomaly_stats
    


    def _calculate_anomaly_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calculate statistics about detected anomalies
        """
        if 'is_anomaly_ml' not in df.columns:
            return {}
        
        total_records = len(df)
        anomalies = df[df['is_anomaly_ml'] == True]
        total_anomalies = len(anomalies)
        
        stats = {
            "total_records": total_records,
            "total_anomalies": total_anomalies,
            "anomaly_percentage": (total_anomalies / total_records * 100) if total_records > 0 else 0,
            "model_type": self.model_type,
            "detection_time": datetime.now().isoformat()
        }
        
        if total_anomalies > 0:
            # Analyze by device type
            device_anomalies = anomalies['device_type'].value_counts().to_dict()
            stats["anomalies_by_device_type"] = device_anomalies
            
            # Analyze by feature
            for feature in self.features:
                if feature in anomalies.columns:
                    stats[f"avg_{feature}_anomalies"] = float(anomalies[feature].mean())
                    stats[f"max_{feature}_anomalies"] = float(anomalies[feature].max())
            
            # Find top anomalous devices
            if 'device_id' in anomalies.columns and 'anomaly_score_ml' in anomalies.columns:
                top_devices = anomalies.groupby('device_id')['anomaly_score_ml'].mean().nlargest(5)
                stats["top_anomalous_devices"] = top_devices.to_dict()
        
        return stats
    
    def explain_anomaly(self, record: Dict) -> Dict:
        """
        Provide explanation for why a record is anomalous
        """
        explanation = {
            "device_id": record.get('device_id'),
            "timestamp": record.get('timestamp'),
            "is_anomalous": record.get('is_anomaly_ml', False),
            "anomaly_score": round(record.get('anomaly_score_ml', 0), 3),
            "reasons": [],
            "recommendations": []
        }
        
        if not explanation["is_anomalous"]:
            explanation["reasons"].append("No anomaly detected")
            return explanation
        
        # Check each feature for abnormal values
        feature_thresholds = {
            'latency_ms': 100,  # ms
            'jitter_ms': 20,    # ms
            'packet_loss': 0.05, # 5%
            'cpu_utilization': 80, # %
            'memory_utilization': 80, # %
            'tcp_retransmissions': 10,
            'client_count': 50
        }
        
        for feature, threshold in feature_thresholds.items():
            if feature in record and record[feature] is not None:
                value = float(record[feature])
                if value > threshold:
                    explanation["reasons"].append(
                        f"High {feature}: {value:.2f} (threshold: {threshold})"
                    )
                    
                    # Add recommendations
                    if feature == 'latency_ms':
                        explanation["recommendations"].append(
                            "Check network congestion or routing issues"
                        )
                    elif feature == 'cpu_utilization':
                        explanation["recommendations"].append(
                            "Consider load balancing or device upgrade"
                        )
                    elif feature == 'tcp_retransmissions':
                        explanation["recommendations"].append(
                            "Investigate network stability or packet loss"
                        )
        
        if not explanation["reasons"]:
            explanation["reasons"].append(
                "Anomaly detected by ML model based on feature combinations"
            )
        
        return explanation
    
    def save_model(self, filepath: str = "models/anomaly_detector.joblib"):
        """
        Save trained model to file
        """
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'model_type': self.model_type,
            'features': self.features,
            'trained_at': datetime.now().isoformat()
        }
        
        joblib.dump(model_data, filepath)
        logger.info(f"Model saved to {filepath}")
    
    @classmethod
    def load_model(cls, filepath: str = "models/anomaly_detector.joblib"):
        """
        Load trained model from file
        """
        model_data = joblib.load(filepath)
        
        detector = cls(model_type=model_data['model_type'])
        detector.model = model_data['model']
        detector.scaler = model_data['scaler']
        detector.features = model_data['features']
        
        logger.info(f"Model loaded from {filepath}")
        return detector


class AnomalyDetectionService:
    """
    Service for running anomaly detection on network data
    """
    
    @staticmethod
    def detect_anomalies_in_db(db_session, limit: int = 1000):
        """
        Run anomaly detection on database records
        """
        from app.models import NetworkLog
        import pandas as pd
        
        logger.info(f"Running anomaly detection on {limit} records...")
        
        # Fetch recent logs
        logs = db_session.query(NetworkLog).order_by(
            NetworkLog.timestamp.desc()
        ).limit(limit).all()
        
        if not logs:
            logger.warning("No logs found in database")
            return {}
        
        # Convert to DataFrame
        log_dicts = [log.to_dict() for log in logs]
        df = pd.DataFrame(log_dicts)
        
        # Initialize and run anomaly detector
        detector = AnomalyDetector(model_type="isolation_forest")
        df_with_anomalies, stats = detector.detect_anomalies(df)
        
        # Save model
        detector.save_model()
        
        # Get detailed explanations for top anomalies
        top_anomalies = df_with_anomalies[
            df_with_anomalies['is_anomaly_ml'] == True
        ].nlargest(5, 'anomaly_score_ml')
        
        explanations = []
        for _, anomaly in top_anomalies.iterrows():
            explanation = detector.explain_anomaly(anomaly.to_dict())
            explanations.append(explanation)
        
        stats["top_anomaly_explanations"] = explanations
        
        logger.info(f"Anomaly detection complete. Stats: {stats}")
        
        return stats