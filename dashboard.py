"""
Streamlit Dashboard for NetAI Insights
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime

# Use try-except for imports to handle missing packages gracefully
try:
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go
    import requests
    import json
    import os
    import streamlit as st
    from datetime import datetime
except ImportError as e:
    # Fallback to minimal imports
    import json
    import os
    import streamlit as st
    from datetime import datetime
    
    st.warning(f"Some packages not available: {e}. Running in limited mode.")

# Page configuration
st.set_page_config(
    page_title="NetAI Insights",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 1rem;
    }
    .anomaly-card {
        background-color: #FEF2F2;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #DC2626;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = "http://localhost:8000"

@st.cache_data(ttl=60)
def fetch_api_data(endpoint):
    """Fetch data from API with caching"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching {endpoint}: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API server. Make sure it's running on port 8000.")
        return None

@st.cache_data(ttl=60)
def post_api_data(endpoint):
    """Post data to API"""
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error posting to {endpoint}: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API server.")
        return None

def display_overview_metrics(metrics_data):
    """Display overview metrics"""
    st.markdown('<div class="main-header">📊 NetAI Insights Dashboard</div>', unsafe_allow_html=True)
    st.markdown("AI-Driven Network Analytics Platform")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Logs",
            value=f"{metrics_data.get('total_logs', 0):,}",
            delta="+1000"
        )
    
    with col2:
        st.metric(
            label="Success Rate",
            value=f"{metrics_data.get('success_rate', 0):.1f}%",
            delta="-0.4%" if metrics_data.get('success_rate', 0) < 95 else "+0.4%"
        )
    
    with col3:
        anomaly_percent = metrics_data.get('anomaly_percentage', 0)
        st.metric(
            label="Anomalies",
            value=f"{anomaly_percent:.1f}%",
            delta=f"{metrics_data.get('anomaly_count', 0)} detected",
            delta_color="inverse" if anomaly_percent > 10 else "normal"
        )
    
    with col4:
        st.metric(
            label="Active Devices",
            value=metrics_data.get('device_distribution', [{}])[0].get('count', 0) if metrics_data.get('device_distribution') else 0,
            delta="50 total"
        )

def display_device_distribution(metrics_data):
    """Display device distribution chart"""
    st.markdown('<div class="sub-header">📱 Device Distribution</div>', unsafe_allow_html=True)
    
    if metrics_data.get('device_distribution'):
        device_df = pd.DataFrame(metrics_data['device_distribution'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig = px.pie(
                device_df,
                values='count',
                names='device_type',
                title='Device Type Distribution',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Bar chart
            fig = px.bar(
                device_df,
                x='device_type',
                y='count',
                title='Device Count by Type',
                color='device_type',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(xaxis_title="Device Type", yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)

def display_latency_analysis(metrics_data):
    """Display latency analysis"""
    st.markdown('<div class="sub-header">⏱️ Latency Analysis</div>', unsafe_allow_html=True)
    
    if metrics_data.get('latency_stats'):
        latency_df = pd.DataFrame(metrics_data['latency_stats'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                latency_df,
                x='device_type',
                y='avg_latency',
                title='Average Latency by Device Type',
                color='device_type',
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            fig.update_layout(xaxis_title="Device Type", yaxis_title="Average Latency (ms)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure(data=[
                go.Bar(name='Avg Latency', x=latency_df['device_type'], y=latency_df['avg_latency']),
                go.Bar(name='Max Latency', x=latency_df['device_type'], y=latency_df['max_latency'])
            ])
            fig.update_layout(
                title='Latency Comparison',
                barmode='group',
                xaxis_title="Device Type",
                yaxis_title="Latency (ms)"
            )
            st.plotly_chart(fig, use_container_width=True)

def display_device_health(devices_data):
    """Display device health status"""
    st.markdown('<div class="sub-header">🏥 Device Health Status</div>', unsafe_allow_html=True)
    
    if devices_data.get('devices'):
        devices_df = pd.DataFrame(devices_data['devices'])
        
        # Create health status column
        devices_df['health_color'] = devices_df['health_status'].apply(
            lambda x: 'green' if x == 'healthy' else 'orange' if x == 'warning' else 'red'
        )
        
        # Display in columns
        cols = st.columns(3)
        for idx, device in devices_df.head(9).iterrows():
            with cols[idx % 3]:
                with st.container():
                    color = "🟢" if device['health_status'] == 'healthy' else "🟠" if device['health_status'] == 'warning' else "🔴"
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>{color} {device['device_id']}</h4>
                        <p><strong>Type:</strong> {device['device_type']}</p>
                        <p><strong>Location:</strong> {device['location']}</p>
                        <p><strong>Latency:</strong> {device['avg_latency']:.1f}ms</p>
                        <p><strong>Anomaly Score:</strong> {device['max_anomaly_score']:.3f}</p>
                        <p><strong>Status:</strong> {device['health_status'].upper()}</p>
                    </div>
                    """, unsafe_allow_html=True)

def display_anomalies(anomalies_data):
    """Display detected anomalies"""
    st.markdown('<div class="sub-header">🚨 Detected Anomalies</div>', unsafe_allow_html=True)
    
    if anomalies_data.get('anomalies'):
        anomalies_df = pd.DataFrame(anomalies_data['anomalies'])
        
        # Display top anomalies
        for idx, anomaly in anomalies_df.head(5).iterrows():
            with st.container():
                st.markdown(f"""
                <div class="anomaly-card">
                    <h4>🔴 {anomaly['device_id']} - {anomaly['event_type']}</h4>
                    <p><strong>Time:</strong> {anomaly['timestamp']}</p>
                    <p><strong>Anomaly Score:</strong> {anomaly['anomaly_score']:.3f}</p>
                    <p><strong>Latency:</strong> {anomaly['latency_ms']}ms</p>
                    <p><strong>CPU:</strong> {anomaly['cpu_utilization']}%</p>
                    <p><strong>Details:</strong> {anomaly['details']['protocol']} from {anomaly['details']['source_ip']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Anomaly score distribution
        if len(anomalies_df) > 0:
            fig = px.histogram(
                anomalies_df,
                x='anomaly_score',
                title='Anomaly Score Distribution',
                nbins=20,
                color_discrete_sequence=['#DC2626']
            )
            fig.update_layout(xaxis_title="Anomaly Score", yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)

def display_ml_insights():
    """Display ML/AI insights"""
    st.markdown('<div class="sub-header">🤖 AI/ML Insights</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Real-time Anomaly Detection")
        
        # Interactive prediction form
        with st.form("prediction_form"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                latency = st.slider("Latency (ms)", 1, 2000, 100)
                jitter = st.slider("Jitter (ms)", 1, 200, 20)
                packet_loss = st.slider("Packet Loss (%)", 0.0, 1.0, 0.05)
                cpu_util = st.slider("CPU Utilization (%)", 0, 100, 50)
            
            with col_b:
                memory_util = st.slider("Memory Utilization (%)", 0, 100, 60)
                tcp_retrans = st.slider("TCP Retransmissions", 0, 100, 5)
                client_count = st.slider("Client Count", 0, 200, 30)
                throughput = st.slider("Throughput (Mbps)", 0, 1000, 200)
            
            predict_button = st.form_submit_button("🔍 Predict Anomaly")
            
            if predict_button:
                params = {
                    'latency': latency,
                    'jitter': jitter,
                    'packet_loss': packet_loss,
                    'cpu_util': cpu_util,
                    'memory_util': memory_util,
                    'tcp_retrans': tcp_retrans,
                    'client_count': client_count,
                    'throughput': throughput
                }
                
                response = requests.get(f"{API_BASE_URL}/api/ml/predict", params=params)
                if response.status_code == 200:
                    prediction = response.json()
                    
                    if prediction['is_anomaly']:
                        st.error(f"🚨 ANOMALY DETECTED! Score: {prediction['anomaly_score']:.3f}")
                        if prediction.get('explanation') and prediction['explanation'].get('reasons'):
                            st.warning("**Reasons:**")
                            for reason in prediction['explanation']['reasons']:
                                st.write(f"• {reason}")
                    else:
                        st.success(f"✅ Normal Operation. Score: {prediction['anomaly_score']:.3f}")
    
    with col2:
        st.markdown("##### ML Model Information")
        
        # Get ML features
        ml_data = fetch_api_data("/api/ml/features")
        if ml_data:
            st.info(f"**Model Type:** {ml_data.get('model_type', 'N/A')}")
            st.info(f"**Features Used:** {len(ml_data.get('features', []))}")
            
            features_df = pd.DataFrame({
                'Feature': ml_data.get('features', []),
                'Description': [ml_data.get('feature_descriptions', {}).get(f, '') for f in ml_data.get('features', [])]
            })
            st.dataframe(features_df, use_container_width=True, hide_index=True)
        
        # Run ML detection button
        if st.button("🔄 Run Anomaly Detection", type="primary"):
            with st.spinner("Running AI anomaly detection..."):
                result = post_api_data("/api/ml/detect?limit=500")
                if result:
                    st.success(f"Detected {result.get('statistics', {}).get('total_anomalies', 0)} anomalies")
                    st.rerun()

def display_spark_analytics():
    """Display Spark batch analytics results"""
    st.markdown('<div class="sub-header">⚡ Batch Analytics (Spark)</div>', unsafe_allow_html=True)
    
    if st.button("🚀 Run Batch Analysis", type="secondary"):
        with st.spinner("Running Spark batch analysis..."):
            result = post_api_data("/api/spark/analyze")
            if result:
                st.success("Batch analysis completed!")
                
                # Show summary
                results = result.get('results', {})
                summary = results.get('summary', {})
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Records Analyzed", summary.get('total_records_analyzed', 0))
                with col2:
                    st.metric("Unique Devices", summary.get('total_devices', 0))
                with col3:
                    issues = summary.get('performance_issues', {})
                    st.metric("Total Issues", issues.get('total_issues', 0))
                
                # Show top problematic devices
                if results.get('device_stats_sample'):
                    st.markdown("##### Top Problematic Devices")
                    issues_df = pd.DataFrame(results['device_stats_sample']).head(5)
                    st.dataframe(issues_df[['device_id', 'device_type', 'avg_latency', 'success_rate']], 
                               use_container_width=True, hide_index=True)

def main():
    """Main dashboard function"""
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/network.png", width=100)
        st.title("NetAI Insights")
        st.markdown("---")
        
        st.markdown("### 📊 Navigation")
        page = st.radio(
            "Go to",
            ["Overview", "Device Health", "Anomalies", "AI Insights", "Batch Analytics"]
        )
        
        st.markdown("---")
        st.markdown("### ⚙️ Actions")
        if st.button("🔄 Refresh All Data", type="primary"):
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📈 Quick Stats")
        
        # Fetch metrics for sidebar
        metrics = fetch_api_data("/api/metrics/summary")
        if metrics:
            st.metric("Total Logs", f"{metrics.get('total_logs', 0):,}")
            st.metric("Success Rate", f"{metrics.get('success_rate', 0):.1f}%")
            st.metric("Anomalies", f"{metrics.get('anomaly_count', 0)}")
    
    # Main content based on selected page
    if page == "Overview":
        metrics = fetch_api_data("/api/metrics/summary")
        if metrics:
            display_overview_metrics(metrics)
            display_device_distribution(metrics)
            display_latency_analysis(metrics)
    
    elif page == "Device Health":
        devices = fetch_api_data("/api/devices")
        if devices:
            display_device_health(devices)
    
    elif page == "Anomalies":
        anomalies = fetch_api_data("/api/anomalies?limit=10")
        if anomalies:
            display_anomalies(anomalies)
    
    elif page == "AI Insights":
        display_ml_insights()
    
    elif page == "Batch Analytics":
        display_spark_analytics()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>NetAI Insights Dashboard • AI-Driven Network Analytics • Built with FastAPI, Streamlit & Scikit-learn</p>
        <p>Data last updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
