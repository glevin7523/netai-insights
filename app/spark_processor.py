"""
Lightweight batch processing (Spark simulation using Pandas)
For demonstration purposes - shows Spark concepts without heavy dependencies
"""
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import json
import os

logger = logging.getLogger(__name__)

class BatchNetworkProcessor:
    """
    Batch processor for network analytics (simulating Spark functionality)
    """
    
    def __init__(self):
        logger.info("Batch processor initialized (Spark simulation)")
    
    def read_csv_to_dataframe(self, csv_path: str):
        """
        Read network logs from CSV into DataFrame
        """
        logger.info(f"Reading CSV from {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Convert timestamp
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        logger.info(f"Read {len(df)} records")
        logger.info(f"Columns: {list(df.columns)}")
        
        return df
    
    def analyze_device_performance(self, df):
        """
        Analyze device performance metrics
        """
        logger.info("Analyzing device performance...")
        
        device_stats = df.groupby(['device_id', 'device_type', 'location']).agg(
            total_events=('device_id', 'count'),
            avg_latency=('latency_ms', 'mean'),
            max_latency=('latency_ms', 'max'),
            avg_cpu_usage=('cpu_utilization', 'mean'),
            avg_memory_usage=('memory_utilization', 'mean'),
            avg_throughput=('throughput_mbps', 'mean'),
            total_retransmissions=('tcp_retransmissions', 'sum'),
            avg_packet_loss=('packet_loss', 'mean'),
            success_count=('success', 'sum')
        ).reset_index()
        
        device_stats['success_rate'] = (device_stats['success_count'] / device_stats['total_events']) * 100
        device_stats = device_stats.sort_values('avg_latency', ascending=False)
        
        return device_stats
    
    def analyze_hourly_traffic(self, df):
        """
        Analyze traffic patterns by hour
        """
        logger.info("Analyzing hourly traffic patterns...")
        
        df['hour'] = df['timestamp'].dt.hour
        
        hourly_stats = df.groupby(['hour', 'device_type']).agg(
            event_count=('device_id', 'count'),
            avg_latency=('latency_ms', 'mean'),
            avg_throughput=('throughput_mbps', 'mean'),
            total_bytes_sent=('bytes_sent', 'sum'),
            total_bytes_received=('bytes_received', 'sum')
        ).reset_index()
        
        hourly_stats = hourly_stats.sort_values('hour')
        
        return hourly_stats
    
    def detect_performance_issues(self, df):
        """
        Detect performance issues using thresholds
        """
        logger.info("Detecting performance issues...")
        
        # Define thresholds
        high_latency = df[df['latency_ms'] > 100]  # > 100ms is high
        high_cpu = df[df['cpu_utilization'] > 80]  # > 80% CPU
        high_packet_loss = df[df['packet_loss'] > 0.05]  # > 5% packet loss
        high_retransmissions = df[df['tcp_retransmissions'] > 10]
        
        issues = {
            "high_latency_count": len(high_latency),
            "high_cpu_count": len(high_cpu),
            "high_packet_loss_count": len(high_packet_loss),
            "high_retransmissions_count": len(high_retransmissions),
            "total_issues": len(high_latency) + len(high_cpu) + len(high_packet_loss) + len(high_retransmissions)
        }
        
        # Get top problematic devices
        mask = (df['latency_ms'] > 100) | (df['cpu_utilization'] > 80) | (df['packet_loss'] > 0.05) | (df['tcp_retransmissions'] > 10)
        problematic_devices = df[mask].groupby(['device_id', 'device_type']).agg(
            issue_count=('device_id', 'count')
        ).reset_index().sort_values('issue_count', ascending=False).head(10)
        
        return issues, problematic_devices
    
    def analyze_network_security(self, df):
        """
        Analyze security-related events
        """
        logger.info("Analyzing network security...")
        
        # FIXED VERSION:
        security_mask = (
            (df['event_category'] == 'security') | 
            df['event_type'].str.contains('fail', case=False, na=False) |
            df['event_type'].str.contains('deny', case=False, na=False) |
            df['error_code'].notna()
        )
        
        security_events = df[security_mask]
        
        if len(security_events) > 0:
            security_stats = security_events.groupby(['event_type', 'device_type']).agg(
                count=('event_type', 'count'),
                avg_anomaly_score=('anomaly_score', 'mean')
            ).reset_index().sort_values('count', ascending=False)
        else:
            security_stats = pd.DataFrame(columns=['event_type', 'device_type', 'count', 'avg_anomaly_score'])
        
        return security_stats
    
    def save_results(self, results_dict, output_dir="data/spark_output"):
        """
        Save analysis results
        """
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info(f"Saving results to {output_dir}")
        
        for name, df in results_dict.items():
            if df is not None and len(df) > 0:
                output_path = os.path.join(output_dir, f"{name}.csv")
                df.to_csv(output_path, index=False)
                logger.info(f"Saved {name} to {output_path}")
        
        # Save summary
        json_path = os.path.join(output_dir, "analysis_summary.json")
        summary = {
            "timestamp": datetime.now().isoformat(),
            "analyses_performed": list(results_dict.keys()),
            "output_directory": output_dir,
            "note": "Batch processing simulation (Spark concepts demonstrated)"
        }
        
        with open(json_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Summary saved to {json_path}")
    
    def run_complete_analysis(self, csv_path: str = "data/network_logs.csv"):
        """
        Run complete batch analysis pipeline
        """
        logger.info("Starting batch analysis (Spark simulation)...")
        
        try:
            # Read data
            df = self.read_csv_to_dataframe(csv_path)
            
            # Run analyses
            device_stats = self.analyze_device_performance(df)
            hourly_stats = self.analyze_hourly_traffic(df)
            issues, problematic_devices = self.detect_performance_issues(df)
            security_stats = self.analyze_network_security(df)
            
            # Collect results
            results = {
                "device_performance": device_stats,
                "hourly_traffic": hourly_stats,
                "problematic_devices": problematic_devices,
                "security_analysis": security_stats
            }
            
            # Save results
            self.save_results(results)
            
            # Create summary report
            summary = {
                "total_records_analyzed": len(df),
                "total_devices": df['device_id'].nunique(),
                "time_period": {
                    "min_timestamp": df['timestamp'].min().isoformat() if not df.empty else None,
                    "max_timestamp": df['timestamp'].max().isoformat() if not df.empty else None
                },
                "performance_issues": issues,
                "analysis_timestamp": datetime.now().isoformat(),
                "processing_engine": "Pandas (Spark simulation)"
            }
            
            logger.info("Batch analysis completed successfully!")
            
            return {
                "summary": summary,
                "device_stats_sample": device_stats.head(20).to_dict(orient='records'),
                "hourly_stats_sample": hourly_stats.head(24).to_dict(orient='records'),
                "total_issues": issues["total_issues"],
                "processing_note": "Using Pandas to simulate Spark batch processing for demonstration"
            }
            
        except Exception as e:
            logger.error(f"Batch analysis failed: {e}")
            return {"error": str(e)}


def run_batch_analysis():
    """
    Main function to run batch analysis
    """
    processor = BatchNetworkProcessor()
    
    try:
        results = processor.run_complete_analysis()
        return results
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # Run when file is executed directly
    print("Running batch analysis (Spark simulation)...")
    results = run_batch_analysis()
    
    if "error" not in results:
        print("\n✅ Batch Analysis Results:")
        print(f"Total issues detected: {results.get('total_issues', 0)}")
        print(f"Processing engine: {results.get('processing_note', 'N/A')}")
        
        if "device_stats_sample" in results:
            print(f"\nSample Device Stats ({len(results['device_stats_sample'])} devices):")
            for device in results['device_stats_sample'][:3]:
                print(f"  {device['device_id']}: {device['avg_latency']:.1f}ms latency, "
                      f"{device['success_rate']:.1f}% success rate")
    else:
        print(f"❌ Error: {results['error']}")