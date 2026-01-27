import pandas as pd
import json

def verify_generated_data():
    print("Verifying generated network logs...")
    print("=" * 50)
    
    try:
        # Load the data
        df = pd.read_csv('../data/network_logs.csv')
        
        print(f"Total records: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print(f"\nDevice Type Distribution:")
        print(df['device_type'].value_counts())
        
        print(f"\nEvent Category Distribution:")
        print(df['event_category'].value_counts())
        
        print(f"\nBasic Statistics:")
        print(f"Average Latency: {df['latency_ms'].mean():.2f} ms")
        print(f"Max Latency: {df['latency_ms'].max():.2f} ms")
        print(f"Failure Rate: {(df['success'] == False).sum() / len(df) * 100:.2f}%")
        
        # Check for anomalies
        if 'anomaly_score' in df.columns:
            anomalies = df[df['anomaly_score'] > 0.7]
            print(f"\nPotential Anomalies: {len(anomalies)} ({len(anomalies)/len(df)*100:.2f}%)")
            
            # Display sample anomalies
            if len(anomalies) > 0:
                print("\nSample Anomalies:")
                for i, (_, row) in enumerate(anomalies.head(3).iterrows(), 1):
                    print(f"  {i}. Device: {row['device_id']}, "
                          f"Latency: {row['latency_ms']}ms, "
                          f"Score: {row['anomaly_score']:.3f}")
        
        print("\n✅ Data verification complete!")
        
    except FileNotFoundError:
        print("❌ Data file not found. Run the log simulator first.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_generated_data()