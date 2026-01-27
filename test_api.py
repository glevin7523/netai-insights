"""
Test script for the FastAPI application
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test all API endpoints"""
    print("Testing NetAI Insights API...")
    print("=" * 50)
    
    endpoints = [
        ("/", "Root endpoint"),
        ("/api/health", "Health check"),
        ("/api/metrics/summary", "Metrics summary"),
        ("/api/logs?limit=5", "Recent logs"),
        ("/api/devices", "Device list"),
        ("/api/anomalies?limit=5", "Top anomalies"),
    ]
    
    for endpoint, description in endpoints:
        try:
            print(f"\nTesting: {description}")
            print(f"Endpoint: {endpoint}")
            
            response = requests.get(f"{BASE_URL}{endpoint}")
            
            if response.status_code == 200:
                print(f"✅ Status: {response.status_code}")
                
                # Try to parse JSON
                try:
                    data = response.json()
                    if isinstance(data, dict) and len(data) > 0:
                        print(f"   Response keys: {list(data.keys())[:5]}...")
                        if "message" in data:
                            print(f"   Message: {data['message']}")
                    elif isinstance(data, list):
                        print(f"   Response items: {len(data)}")
                except:
                    print(f"   Response: {response.text[:100]}...")
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"   Error: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to {BASE_URL}")
            print("   Make sure the API server is running!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api_endpoints()