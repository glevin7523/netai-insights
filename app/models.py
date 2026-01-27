"""
SQLAlchemy Models for Network Analytics
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class NetworkLog(Base):
    """Network log entry from devices"""
    __tablename__ = "network_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    device_id = Column(String(50), index=True)
    device_type = Column(String(50), index=True)
    device_model = Column(String(50))
    location = Column(String(100))
    event_category = Column(String(50))
    event_type = Column(String(50))
    source_ip = Column(String(45))
    destination_ip = Column(String(45))
    source_mac = Column(String(50))
    destination_mac = Column(String(50))
    protocol = Column(String(20))
    source_port = Column(Integer)
    destination_port = Column(Integer)
    vlan_id = Column(Integer)
    bytes_sent = Column(Integer)
    bytes_received = Column(Integer)
    packets_sent = Column(Integer)
    packets_received = Column(Integer)
    session_duration_seconds = Column(Integer)
    latency_ms = Column(Float)
    jitter_ms = Column(Float)
    packet_loss = Column(Float)
    throughput_mbps = Column(Float)
    cpu_utilization = Column(Float)
    memory_utilization = Column(Float)
    tcp_retransmissions = Column(Integer)
    wireless_signal_strength = Column(Integer)
    client_count = Column(Integer)
    success = Column(Boolean)
    error_code = Column(String(50), nullable=True)
    anomaly_score = Column(Float)
    tags = Column(JSON)  # Store as JSON array
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "device_id": self.device_id,
            "device_type": self.device_type,
            "device_model": self.device_model,
            "location": self.location,
            "event_category": self.event_category,
            "event_type": self.event_type,
            "source_ip": self.source_ip,
            "destination_ip": self.destination_ip,
            "protocol": self.protocol,
            "latency_ms": self.latency_ms,
            "jitter_ms": self.jitter_ms,
            "packet_loss": self.packet_loss,
            "throughput_mbps": self.throughput_mbps,
            "cpu_utilization": self.cpu_utilization,
            "memory_utilization": self.memory_utilization,
            "tcp_retransmissions": self.tcp_retransmissions,
            "wireless_signal_strength": self.wireless_signal_strength,
            "client_count": self.client_count,
            "success": self.success,
            "error_code": self.error_code,
            "anomaly_score": self.anomaly_score,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class DeviceMetrics(Base):
    """Aggregated device metrics"""
    __tablename__ = "device_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(50), index=True)
    device_type = Column(String(50))
    timestamp = Column(DateTime, index=True)
    
    # Performance metrics
    avg_latency = Column(Float)
    max_latency = Column(Float)
    min_latency = Column(Float)
    avg_jitter = Column(Float)
    avg_packet_loss = Column(Float)
    avg_throughput = Column(Float)
    avg_cpu_utilization = Column(Float)
    avg_memory_utilization = Column(Float)
    total_errors = Column(Integer)
    total_success = Column(Integer)
    
    # Network specific
    total_tcp_retransmissions = Column(Integer)
    avg_wireless_signal = Column(Float)
    total_clients = Column(Integer)
    
    # Anomaly metrics
    anomaly_count = Column(Integer)
    anomaly_score_avg = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class AnomalyDetection(Base):
    """Detected anomalies"""
    __tablename__ = "anomalies"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    device_id = Column(String(50), index=True)
    anomaly_type = Column(String(100))
    severity = Column(String(20))  # low, medium, high, critical
    description = Column(Text)
    metrics = Column(JSON)  # Store affected metrics
    recommendation = Column(Text)
    status = Column(String(20), default="detected")  # detected, investigating, resolved
    detected_at = Column(DateTime, default=datetime.utcnow)