"""
Network Log Simulator
Generates realistic network device logs similar to Juniper Mist environment
"""
import json
import random
import time
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import List, Dict
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NetworkLogSimulator:
    """Simulates network logs from various devices"""
    
    def __init__(self):
        # Network device configurations
        self.device_types = ['access_point', 'switch', 'firewall', 'router']
        self.device_models = {
            'access_point': ['AP-45', 'AP-63', 'AP-33'],
            'switch': ['EX-4300', 'EX-2300', 'QFX-5100'],
            'firewall': ['SRX-3400', 'SRX-1500'],
            'router': ['MX-204', 'MX-10003']
        }
        
        # Network events specific to Juniper Mist environment
        self.events = {
            'authentication': ['auth_success', 'auth_failure', 'reauth'],
            'association': ['assoc', 'disassoc', 'roam'],
            'dhcp': ['dhcp_discover', 'dhcp_offer', 'dhcp_request', 'dhcp_ack'],
            'dns': ['dns_query', 'dns_response', 'dns_failure'],
            'network': ['interface_up', 'interface_down', 'bgp_update', 'ospf_hello'],
            'security': ['firewall_allow', 'firewall_deny', 'ips_alert']
        }
        
        # VLAN configurations
        self.vlans = {
            'data': range(10, 50),
            'voice': range(50, 60),
            'management': range(100, 110),
            'guest': range(200, 210)
        }
        
        # IP ranges (simulating different subnets)
        self.ip_ranges = [
            '192.168.{}.{}',      # Internal
            '10.0.{}.{}',         # Management
            '172.16.{}.{}',       # Infrastructure
            '203.0.113.{}'        # Public
        ]
        
        # Device pool
        self.devices = self._generate_device_pool(50)
        
    def _generate_device_pool(self, count: int) -> List[Dict]:
        """Generate a pool of network devices"""
        devices = []
        for i in range(count):
            dev_type = random.choice(self.device_types)
            devices.append({
                'device_id': f"{dev_type[:2].upper()}{i:04d}",
                'device_type': dev_type,
                'model': random.choice(self.device_models[dev_type]),
                'location': random.choice(['Floor1', 'Floor2', 'DataCenter', 'Branch1', 'Branch2']),
                'ip_address': f"10.10.{random.randint(1, 254)}.{random.randint(2, 254)}"
            })
        return devices
    
    def _generate_network_metrics(self) -> Dict:
        """Generate realistic network metrics"""
        # Normal values with occasional anomalies
        if random.random() > 0.95:  # 5% chance of anomaly
            return {
                'latency_ms': random.randint(500, 2000),
                'jitter_ms': random.randint(50, 200),
                'packet_loss': random.uniform(0.1, 0.5),
                'throughput_mbps': random.randint(10, 50),
                'cpu_utilization': random.randint(80, 100),
                'memory_utilization': random.randint(85, 100),
                'tcp_retransmissions': random.randint(20, 100),
                'wireless_signal_strength': random.randint(-90, -70),
                'client_count': random.randint(50, 100),
                'is_anomaly': True
            }
        else:
            return {
                'latency_ms': random.randint(1, 100),
                'jitter_ms': random.randint(1, 20),
                'packet_loss': random.uniform(0.0, 0.05),
                'throughput_mbps': random.randint(100, 1000),
                'cpu_utilization': random.randint(10, 60),
                'memory_utilization': random.randint(20, 70),
                'tcp_retransmissions': random.randint(0, 5),
                'wireless_signal_strength': random.randint(-60, -40),
                'client_count': random.randint(5, 30),
                'is_anomaly': False
            }
    
    def generate_single_log(self, timestamp: datetime = None) -> Dict:
        """Generate a single network log entry"""
        if timestamp is None:
            # Generate timestamp within last 7 days
            timestamp = datetime.now() - timedelta(
                days=random.randint(0, 7),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
        
        device = random.choice(self.devices)
        event_category = random.choice(list(self.events.keys()))
        event_type = random.choice(self.events[event_category])
        
        # Generate source and destination IPs
        src_ip_template = random.choice(self.ip_ranges)
        dst_ip_template = random.choice(self.ip_ranges)
        
        src_ip = src_ip_template.format(random.randint(1, 254), random.randint(1, 254))
        dst_ip = dst_ip_template.format(random.randint(1, 254), random.randint(1, 254))
        
        # Get network metrics
        metrics = self._generate_network_metrics()
        
        # Build the complete log
        log = {
            'timestamp': timestamp.isoformat(),
            'device_id': device['device_id'],
            'device_type': device['device_type'],
            'device_model': device['model'],
            'location': device['location'],
            'event_category': event_category,
            'event_type': event_type,
            'source_ip': src_ip,
            'destination_ip': dst_ip,
            'source_mac': ':'.join(f'{random.randint(0, 255):02x}' for _ in range(6)),
            'destination_mac': ':'.join(f'{random.randint(0, 255):02x}' for _ in range(6)),
            'protocol': random.choice(['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS', 'DNS', 'DHCP']),
            'source_port': random.randint(1024, 65535),
            'destination_port': random.choice([80, 443, 22, 53, 67, 68, 161]),
            'vlan_id': random.choice(list(self.vlans.values()))[0],
            'bytes_sent': random.randint(100, 100000),
            'bytes_received': random.randint(100, 100000),
            'packets_sent': random.randint(1, 1000),
            'packets_received': random.randint(1, 1000),
            'session_duration_seconds': random.randint(1, 3600),
            'success': random.random() > 0.05,  # 95% success rate
            'error_code': None if random.random() > 0.05 else random.choice(['TIMEOUT', 'AUTH_FAIL', 'DHCP_NAK', 'DNS_NXDOMAIN']),
            'anomaly_score': random.uniform(0, 1) if not metrics['is_anomaly'] else random.uniform(0.7, 1.0),
            'tags': ['normal'] if not metrics['is_anomaly'] else ['anomaly', 'investigate']
        }
        
        # Add network metrics
        log.update({k: v for k, v in metrics.items() if k != 'is_anomaly'})
        
        return log
    
    def generate_logs(self, count: int = 1000) -> List[Dict]:
        """Generate multiple log entries"""
        logger.info(f"Generating {count} network logs...")
        logs = []
        
        # Create base timestamp and increment
        base_time = datetime.now() - timedelta(days=7)
        
        for i in range(count):
            # Generate timestamp with slight increments
            timestamp = base_time + timedelta(
                seconds=random.randint(1, 300) * i  # Simulate real-time streaming
            )
            log = self.generate_single_log(timestamp)
            logs.append(log)
            
            # Progress indicator
            if (i + 1) % 100 == 0:
                logger.info(f"Generated {i + 1}/{count} logs")
        
        logger.info(f"Successfully generated {len(logs)} network logs")
        return logs
    
    def save_to_csv(self, logs: List[Dict], filename: str = 'network_logs.csv'):
        """Save logs to CSV file"""
        df = pd.DataFrame(logs)
        
        # Ensure data directory exists
        import os
        data_dir = 'data'
        os.makedirs(data_dir, exist_ok=True)
        
        filepath = os.path.join(data_dir, filename)
        df.to_csv(filepath, index=False)
        logger.info(f"Saved {len(logs)} logs to {filepath}")
        
        # Also save a sample for quick testing
        sample_filename = filename.replace('.csv', '_sample.csv')
        sample_filepath = os.path.join(data_dir, sample_filename)
        df.head(100).to_csv(sample_filepath, index=False)
        logger.info(f"Saved sample to {sample_filepath}")
        
        return filepath

    def generate_and_save(self, count: int = 10000):
        """Generate and save logs in one step"""
        logs = self.generate_logs(count)
        return self.save_to_csv(logs)

# Quick test function
def test_generator():
    """Test the log generator"""
    print("Testing Network Log Simulator...")
    print("=" * 50)
    
    simulator = NetworkLogSimulator()
    
    # Generate 10 sample logs
    sample_logs = []
    for _ in range(5):
        log = simulator.generate_single_log()
        sample_logs.append(log)
        print(f"\nSample Log {_ + 1}:")
        print(f"  Device: {log['device_id']} ({log['device_type']})")
        print(f"  Event: {log['event_type']}")
        print(f"  Latency: {log['latency_ms']}ms")
        print(f"  Anomaly: {log.get('is_anomaly', False)}")
        print(f"  Tags: {log['tags']}")
    
    # Generate and save a larger dataset
    print("\n" + "=" * 50)
    print("Generating full dataset...")
    filepath = simulator.generate_and_save(1000)  # Start with 1000 logs
    
    print(f"\nDataset saved to: {filepath}")
    print(f"Sample saved to: data/network_logs_sample.csv")
    
    # Show statistics
    df = pd.DataFrame(sample_logs)
    print("\nDataset Statistics:")
    print(f"Total logs generated: 1000")
    print(f"Device types: {df['device_type'].unique().tolist()}")
    print(f"Event categories: {df['event_category'].unique().tolist()}")
    
    return filepath

if __name__ == "__main__":
    # Run test when file is executed directly
    test_generator()