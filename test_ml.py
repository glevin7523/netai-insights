"""
Test ML anomaly detection
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_ml_endpoints():
    """Test ML endpoints"""
    print("Testing ML Anomaly Detection API...")
    print("=" * 50)
    
    # Test 1: Get ML features
    print("\n1. Testing ML features endpoint:")
    response = requests.get(f"{BASE_URL}/api/ml/features")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Features: {data['features']}")
        print(f"   Model type: {data['model_type']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # Test 2: Run anomaly detection on database
    print("\n2. Running anomaly detection on database:")
    response = requests.post(f"{BASE_URL}/api/ml/detect?limit=500")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Detection complete!")
        print(f"   Records analyzed: {data['records_analyzed']}")
        if 'statistics' in data:
            stats = data['statistics']
            print(f"   Anomalies detected: {stats.get('total_anomalies', 'N/A')}")
            print(f"   Anomaly percentage: {stats.get('anomaly_percentage', 'N/A'):.2f}%")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   {response.text[:200]}")
    
    # Test 3: Real-time prediction
    print("\n3. Testing real-time anomaly prediction:")
    params = {
        'latency': 150,      # High latency
        'jitter': 25,        # High jitter
        'packet_loss': 0.1,  # High packet loss
        'cpu_util': 85,      # High CPU
        'memory_util': 75,
        'tcp_retrans': 15,   # High retransmissions
        'client_count': 40,
        'throughput': 50
    }
    
    response = requests.get(f"{BASE_URL}/api/ml/predict", params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Prediction received!")
        print(f"   Is anomaly: {data['is_anomaly']}")
        print(f"   Anomaly score: {data['anomaly_score']}")
        print(f"   Confidence: {data['confidence']}")
        
        if 'explanation' in data:
            exp = data['explanation']
            print(f"   Reasons: {exp.get('reasons', [])[:2]}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # Test 4: Test with normal values
    print("\n4. Testing with normal network values:")
    normal_params = {
        'latency': 30,
        'jitter': 5,
        'packet_loss': 0.01,
        'cpu_util': 45,
        'memory_util': 60,
        'tcp_retrans': 2,
        'client_count': 20,
        'throughput': 200
    }
    
    response = requests.get(f"{BASE_URL}/api/ml/predict", params=normal_params)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Normal values check:")
        print(f"   Is anomaly: {data['is_anomaly']}")
        print(f"   Anomaly score: {data['anomaly_score']}")
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    test_ml_endpoints()