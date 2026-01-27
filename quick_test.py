"""
Quick test to verify everything works
"""
import requests

BASE = "http://localhost:8000"

print("=== QUICK SYSTEM TEST ===\n")

# 1. Test root
print("1. Testing API root...")
r = requests.get(f"{BASE}/")
print(f"   Status: {r.status_code}")
print(f"   Message: {r.json()['message']}")

# 2. Test metrics
print("\n2. Testing metrics...")
r = requests.get(f"{BASE}/api/metrics/summary")
data = r.json()
print(f"   Total logs: {data['total_logs']}")
print(f"   Success rate: {data['success_rate']}%")
print(f"   Anomalies: {data['anomaly_count']}")

# 3. Test devices
print("\n3. Testing devices...")
r = requests.get(f"{BASE}/api/devices")
data = r.json()
print(f"   Total devices: {data['total_devices']}")
print(f"   First device: {data['devices'][0]['device_id']}")

# 4. Test ML
print("\n4. Testing ML prediction...")
params = {
    'latency': 500, 'jitter': 50, 'packet_loss': 0.2,
    'cpu_util': 90, 'memory_util': 85, 'tcp_retrans': 20,
    'client_count': 60, 'throughput': 30
}
r = requests.get(f"{BASE}/api/ml/predict", params=params)
if r.status_code == 200:
    data = r.json()
    print(f"   Is anomaly: {data['is_anomaly']}")
    print(f"   Score: {data['anomaly_score']}")
else:
    print(f"   Error (will fix): {r.status_code}")

print("\n=== TEST COMPLETE ===")