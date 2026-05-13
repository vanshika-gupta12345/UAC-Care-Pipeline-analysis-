import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION & THEMING
# ==========================================
st.set_page_config(
    page_title="UAC Care Pipeline Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a high-end "Executive" look
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #1f2937;
        border: 1px solid #374151;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar Styling */
    .css-1d391kg { background-color: #111827; }
    
    /* Plotly Chart Containers */
    .plot-container {
        border: 1px solid #374151;
        border-radius: 15px;
        padding: 10px;
        background-color: #111827;
    }
    
    /* Header Styling */
    h1, h2, h3 { color: #60a5fa !important; font-weight: 700 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DATA PROCESSING ENGINE
# ==========================================
@st.cache_data
def load_and_process_data(file_path):
    # Load raw data
    df = pd.read_csv(file_path)
    
    # Cleaning
    df = df.dropna(subset=['Date']).copy()
    num_cols = [
        'Children apprehended and placed in CBP custody*',
        'Children in CBP custody',
        'Children transferred out of CBP custody',
        'Children in HHS Care',
        'Children discharged from HHS Care'
    ]
    for col in num_cols:
        df[col] = df[col].astype(str).str.replace(',', '').str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    # KPI Engineering
    df['Transfer_Eff'] = df['Children transferred out of CBP custody'] / df['Children in CBP custody']
    df['Discharge_Eff'] = df['Children discharged from HHS Care'] / df['Children in HHS Care']
    df['Backlog'] = df['Children apprehended and placed in CBP custody*'] - df['Children discharged from HHS Care']
    df['Stability'] = df['Children discharged from HHS Care'].rolling(7).std()
    
    return df.replace([np.inf, -np.inf], np.nan).fillna(0)

# Load the dataset
try:
    data = load_and_process_data('HHS_Unaccompanied_Alien_Children_Program.csv')
except:
    st.error("Dataset not found. Please ensure 'HHS_Unaccompanied_Alien_Children_Program.csv' is in the folder.")
    st.stop()

# ==========================================
# 3. SIDEBAR & NAVIGATION
# ==========================================
st.sidebar.image("https://www.hhs.gov/sites/default/files/hhs-logo.png", width=100)
st.sidebar.title("Operational Control")
st.sidebar.markdown("---")

# Date Filter
min_date = data['Date'].min().to_pydatetime()
max_date = data['Date'].max().to_pydatetime()
date_range = st.sidebar.date_input("Analysis Window", [min_date, max_date])

if len(date_range) == 2:
    filtered_df = data[(data['Date'] >= pd.to_datetime(date_range[0])) & 
                       (data['Date'] <= pd.to_datetime(date_range[1]))]
else:
    filtered_df = data

# Metric Toggle
show_raw = st.sidebar.checkbox("Show Raw Table", value=False)

# ==========================================
# 4. EXECUTIVE DASHBOARD LAYOUT
# ==========================================
st.title("🛡️ Care Transition & Placement Analytics")
st.caption("Real-time Operational Intelligence for the UAC Reunification Pipeline")

# Row 1: Key Performance Indicators
m1, m2, m3, m4 = st.columns(4)

curr_eff = filtered_df['Transfer_Eff'].mean()
prev_eff = data['Transfer_Eff'].mean() # Comparison for delta

m1.metric("Transfer Efficiency", f"{curr_eff:.1%}", f"{curr_eff - prev_eff:+.1%}")
m2.metric("Discharge Effectiveness", f"{filtered_df['Discharge_Eff'].mean():.2%}")
m3.metric("Net Backlog", f"{int(filtered_df['Backlog'].sum())} units", delta_color="inverse")
m4.metric("Avg HHS Census", f"{int(filtered_df['Children in HHS Care'].mean()):,}")

st.markdown("---")

# Row 2: Visualizations
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📈 Pipeline Throughput (Intake vs Placement)")
    fig_flow = go.Figure()
    fig_flow.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Children apprehended and placed in CBP custody*'], 
                                 name='CBP Intake', fill='tozeroy', line_color='#3b82f6'))
    fig_flow.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Children discharged from HHS Care'], 
                                 name='Sponsor Placement', fill='tozeroy', line_color='#10b981'))
    fig_flow.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_flow, use_container_width=True)

with col_right:
    st.subheader("⚠️ Bottleneck Detection (Ratio Analysis)")
    fig_eff = px.line(filtered_df, x='Date', y=['Transfer_Eff', 'Discharge_Eff'],
                      color_discrete_map={'Transfer_Eff': '#f59e0b', 'Discharge_Eff': '#8b5cf6'})
    fig_eff.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_eff, use_container_width=True)

# Row 3: Advanced Trends
st.subheader("📊 System Pressure & Outcome Stability")
fig_backlog = px.bar(filtered_df, x='Date', y='Backlog', color='Backlog',
                     color_continuous_scale='RdYlGn_r', title="Daily Backlog Accumulation")
fig_backlog.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_backlog, use_container_width=True)

# Row 4: Data Explorer
if show_raw:
    st.markdown("### 🔍 Detailed Operational Log")
    st.dataframe(filtered_df.style.background_gradient(subset=['Backlog'], cmap='RdYlGn_r'), use_container_width=True)

# ==========================================
# 5. FOOTER & EXPORT
# ==========================================
st.sidebar.markdown("---")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📥 Download Analytics Report",
    data=csv,
    file_name=f'UAC_Report_{datetime.now().strftime("%Y%m%d")}.csv',
    mime='text/csv',
)