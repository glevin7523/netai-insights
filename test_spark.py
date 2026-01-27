"""
Test Spark batch processing
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_spark_analysis():
    """Test Spark batch analytics"""
    print("Testing Spark Batch Processing...")
    print("=" * 50)
    
    print("\n1. Starting Spark analysis...")
    start_time = time.time()
    
    try:
        # Note: This is a POST request
        response = requests.post(f"{BASE_URL}/api/spark/analyze")
        
        if response.status_code == 200:
            data = response.json()
            elapsed = time.time() - start_time
            
            print(f"✅ Spark analysis completed in {elapsed:.2f} seconds")
            print(f"   Status: {data['status']}")
            
            if 'results' in data:
                results = data['results']
                if 'summary' in results:
                    summary = results['summary']
                    print(f"\n📊 Analysis Summary:")
                    print(f"   Records analyzed: {summary.get('total_records_analyzed', 'N/A')}")
                    print(f"   Unique devices: {summary.get('total_devices', 'N/A')}")
                    
                    if 'performance_issues' in summary:
                        issues = summary['performance_issues']
                        print(f"   Performance issues: {issues.get('total_issues', 0)}")
                        print(f"   - High latency: {issues.get('high_latency_count', 0)}")
                        print(f"   - High CPU: {issues.get('high_cpu_count', 0)}")
                        print(f"   - High packet loss: {issues.get('high_packet_loss_count', 0)}")
                
                if 'device_stats_sample' in results and len(results['device_stats_sample']) > 0:
                    print(f"\n📈 Sample Device Performance:")
                    for device in results['device_stats_sample'][:3]:
                        print(f"   {device['device_id']}: "
                              f"Latency: {device.get('avg_latency', 0):.1f}ms, "
                              f"Success: {device.get('success_rate', 0):.1f}%")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text[:200]}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to {BASE_URL}")
        print("   Make sure the API server is running!")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_spark_output():
    """Check if Spark output files were created"""
    print("\n2. Checking Spark output files...")
    
    import os
    
    spark_output_dir = "data/spark_output"
    if os.path.exists(spark_output_dir):
        files = os.listdir(spark_output_dir)
        print(f"✅ Spark output directory exists")
        print(f"   Files found: {files}")
        
        for file in files:
            filepath = os.path.join(spark_output_dir, file)
            size = os.path.getsize(filepath)
            print(f"   - {file}: {size:,} bytes")
    else:
        print(f"❌ Spark output directory not found")

if __name__ == "__main__":
    test_spark_analysis()
    check_spark_output()