"""
=============================================================================
THALES GROUP MANUFACTURING – STREAMLIT DASHBOARD
Manufacturing Process Health and Operational Efficiency Analysis
in 6G-Enabled Smart Factories
=============================================================================
Run: streamlit run thales_dashboard.py
=============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Thales Smart Factory Analytics",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Dark Theme CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main Background */
    .stApp { background-color: #0D1117; color: #E6EDF3; }
    .block-container { padding-top: 1rem; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }

    /* Metric Cards */
    [data-testid="metric-container"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 16px;
    }
    [data-testid="metric-container"] label { color: #8B949E !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #4FC3F7 !important; font-size: 2rem !important;
    }

    /* Headers */
    h1, h2, h3 { color: #E6EDF3 !important; }

    /* Section Divider */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #4FC3F7;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #30363D;
        padding-bottom: 4px;
    }

    /* Status badges */
    .badge-high   { background:#00FFB2; color:#0D1117; padding:3px 10px; border-radius:20px; font-weight:bold; }
    .badge-medium { background:#FFD700; color:#0D1117; padding:3px 10px; border-radius:20px; font-weight:bold; }
    .badge-low    { background:#FF4F4F; color:#ffffff; padding:3px 10px; border-radius:20px; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

COLORS = {
    "High": "#00FFB2", "Medium": "#FFD700", "Low": "#FF4F4F",
    "accent": "#4FC3F7", "bg": "#0D1117", "card": "#161B22",
}

# ── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Thales_Group_Manufacturing.csv")
    df["Datetime"] = pd.to_datetime(
        df["Date"] + " " + df["Timestamp"], dayfirst=True, errors="coerce"
    )
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df["Hour"] = df["Datetime"].dt.hour
    df["Machine_Health_Index"] = (
        (1 - df["Temperature_C"] / 100) * 0.4
        + (1 - df["Vibration_Hz"] / 5) * 0.3
        + (1 - df["Power_Consumption_kW"] / 10) * 0.3
    ).clip(0, 1)
    return df

df = load_data()

# ── Sidebar Filters ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏭 Thales Smart Factory")
    st.markdown("---")
    st.markdown("### 🔍 Filters")

    # Machine selector
    machines = sorted(df["Machine_ID"].unique())
    selected_machines = st.multiselect(
        "Machine ID", machines, default=machines[:10],
        help="Select one or more machines"
    )

    # Operation Mode
    op_modes = df["Operation_Mode"].unique().tolist()
    selected_modes = st.multiselect(
        "Operation Mode", op_modes, default=op_modes
    )

    # Efficiency Status
    eff_opts = ["High", "Medium", "Low"]
    selected_eff = st.multiselect(
        "Efficiency Status", eff_opts, default=eff_opts
    )

    # Date Range
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    date_range = st.date_input(
        "Date Range", value=(min_date, max_date),
        min_value=min_date, max_value=max_date
    )

    st.markdown("---")
    st.markdown("### 📊 Metric Comparison")
    compare_x = st.selectbox("X-axis metric", [
        "Temperature_C", "Vibration_Hz", "Power_Consumption_kW",
        "Production_Speed_units_per_hr", "Error_Rate_%",
        "Network_Latency_ms", "Packet_Loss_%",
    ], index=0)
    compare_y = st.selectbox("Y-axis metric", [
        "Quality_Control_Defect_Rate_%", "Error_Rate_%",
        "Production_Speed_units_per_hr", "Machine_Health_Index",
        "Predictive_Maintenance_Score",
    ], index=0)

    st.markdown("---")
    st.caption("📅 Data: Jan–Mar 2025 | Thales Group")

# ── Apply Filters ────────────────────────────────────────────────────────────
if len(date_range) == 2:
    start_d = pd.Timestamp(date_range[0])
    end_d   = pd.Timestamp(date_range[1])
else:
    start_d = df["Date"].min()
    end_d   = df["Date"].max()

mask = (
    df["Machine_ID"].isin(selected_machines if selected_machines else machines)
    & df["Operation_Mode"].isin(selected_modes if selected_modes else op_modes)
    & df["Efficiency_Status"].isin(selected_eff if selected_eff else eff_opts)
    & (df["Date"] >= start_d) & (df["Date"] <= end_d)
)
fdf = df[mask].copy()

if fdf.empty:
    st.warning("⚠️ No data matches the current filters. Please adjust the sidebar.")
    st.stop()

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("# 🏭 Manufacturing Process Health & Efficiency Analytics")
st.markdown("**Thales Group | 6G-Enabled Smart Factory | Real-Time Sensor Dashboard**")
st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
# MODULE 1 – FACTORY HEALTH OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📡 Factory Health Overview</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Records",   f"{len(fdf):,}")
c2.metric("Machines Active", fdf["Machine_ID"].nunique())
c3.metric("Avg Health Index", f"{fdf['Machine_Health_Index'].mean():.3f}")
c4.metric("Avg Production Speed", f"{fdf['Production_Speed_units_per_hr'].mean():.1f} u/hr")
c5.metric("Avg Defect Rate", f"{fdf['Quality_Control_Defect_Rate_%'].mean():.2f}%")

st.markdown("")
col_left, col_right = st.columns([1, 2])

with col_left:
    eff_counts = fdf["Efficiency_Status"].value_counts().reset_index()
    eff_counts.columns = ["Status", "Count"]
    fig_pie = px.pie(
        eff_counts, names="Status", values="Count",
        color="Status",
        color_discrete_map=COLORS,
        hole=0.55, title="Efficiency Distribution"
    )
    fig_pie.update_traces(textfont_color="#0D1117", textfont_size=13)
    fig_pie.update_layout(
        paper_bgcolor=COLORS["card"], plot_bgcolor=COLORS["card"],
        font_color="#E6EDF3", legend_font_color="#E6EDF3",
        title_font_color="#E6EDF3", margin=dict(t=40, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    sensor_means = fdf.groupby("Efficiency_Status")[
        ["Temperature_C", "Vibration_Hz", "Power_Consumption_kW",
         "Network_Latency_ms", "Packet_Loss_%"]
    ].mean().reset_index()
    sensor_melt = sensor_means.melt(
        id_vars="Efficiency_Status", var_name="Sensor", value_name="Avg Value"
    )
    fig_bar = px.bar(
        sensor_melt, x="Sensor", y="Avg Value", color="Efficiency_Status",
        barmode="group", color_discrete_map=COLORS,
        title="Average Sensor Readings by Efficiency Status"
    )
    fig_bar.update_layout(
        paper_bgcolor=COLORS["card"], plot_bgcolor=COLORS["card"],
        font_color="#E6EDF3", legend_font_color="#E6EDF3",
        title_font_color="#E6EDF3", xaxis=dict(gridcolor="#30363D"),
        yaxis=dict(gridcolor="#30363D"), margin=dict(t=40, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# MODULE 2 – MACHINE HEALTH DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">🔧 Machine Health Dashboard</div>', unsafe_allow_html=True)

machine_kpi = fdf.groupby("Machine_ID").agg(
    Health_Index=("Machine_Health_Index", "mean"),
    Avg_Temp=("Temperature_C", "mean"),
    Avg_Vib=("Vibration_Hz", "mean"),
    Avg_Power=("Power_Consumption_kW", "mean"),
    Avg_Defect=("Quality_Control_Defect_Rate_%", "mean"),
    Avg_Speed=("Production_Speed_units_per_hr", "mean"),
).reset_index().sort_values("Health_Index", ascending=False)

col1, col2 = st.columns(2)

with col1:
    fig_health = px.bar(
        machine_kpi, x="Machine_ID", y="Health_Index",
        color="Health_Index", color_continuous_scale=["#FF4F4F", "#FFD700", "#00FFB2"],
        range_color=[0, 1], title="Machine Health Index (All Selected Machines)"
    )
    fig_health.update_layout(
        paper_bgcolor=COLORS["card"], plot_bgcolor=COLORS["card"],
        font_color="#E6EDF3", title_font_color="#E6EDF3",
        xaxis=dict(gridcolor="#30363D"), yaxis=dict(gridcolor="#30363D"),
        coloraxis_colorbar=dict(tickfont=dict(color="#E6EDF3"),
                                title=dict(text="Index", font=dict(color="#E6EDF3")))
    )
    st.plotly_chart(fig_health, use_container_width=True)

with col2:
    fig_scatter = px.scatter(
        machine_kpi, x="Avg_Temp", y="Avg_Vib",
        size="Avg_Power", color="Health_Index",
        hover_name="Machine_ID",
        color_continuous_scale=["#FF4F4F", "#FFD700", "#00FFB2"],
        range_color=[0, 1],
        title="Temperature vs Vibration (size=Power, colour=Health)"
    )
    fig_scatter.update_layout(
        paper_bgcolor=COLORS["card"], plot_bgcolor=COLORS["card"],
        font_color="#E6EDF3", title_font_color="#E6EDF3",
        xaxis=dict(gridcolor="#30363D"), yaxis=dict(gridcolor="#30363D"),
        coloraxis_colorbar=dict(tickfont=dict(color="#E6EDF3"),
                                title=dict(text="Health", font=dict(color="#E6EDF3")))
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# Health Scorecard Table
st.markdown("#### 📋 Machine Health Scorecard")
score_display = machine_kpi.copy()
score_display["Machine_ID"] = score_display["Machine_ID"].apply(lambda x: f"M-{int(x)}")
score_display = score_display.rename(columns={
    "Machine_ID": "Machine", "Health_Index": "Health Index",
    "Avg_Temp": "Temp (°C)", "Avg_Vib": "Vib (Hz)",
    "Avg_Power": "Power (kW)", "Avg_Defect": "Defect Rate (%)",
    "Avg_Speed": "Speed (u/hr)"
}).round(3)
st.dataframe(score_display, use_container_width=True, height=300)

# ════════════════════════════════════════════════════════════════════════════
# MODULE 3 – PRODUCTION & QUALITY PANEL
# ════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">⚡ Production & Quality Panel</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Production speed trend
    daily_speed = fdf.groupby("Date")["Production_Speed_units_per_hr"].mean().reset_index()
    fig_trend = px.area(
        daily_speed, x="Date", y="Production_Speed_units_per_hr",
        title="Daily Average Production Speed", color_discrete_sequence=[COLORS["accent"]]
    )
    fig_trend.update_layout(
        paper_bgcolor=COLORS["card"], plot_bgcolor=COLORS["card"],
        font_color="#E6EDF3", title_font_color="#E6EDF3",
        xaxis=dict(gridcolor="#30363D"), yaxis=dict(gridcolor="#30363D")
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    # Speed vs Defect Rate scatter
    sample_plot = fdf.sample(min(5000, len(fdf)), random_state=42)
    fig_spd_def = px.scatter(
        sample_plot, x="Production_Speed_units_per_hr",
        y="Quality_Control_Defect_Rate_%",
        color="Efficiency_Status", color_discrete_map=COLORS,
        opacity=0.4, title="Production Speed vs Defect Rate"
    )
    fig_spd_def.update_layout(
        paper_bgcolor=COLORS["card"], plot_bgcolor=COLORS["card"],
        font_color="#E6EDF3", title_font_color="#E6EDF3",
        xaxis=dict(gridcolor="#30363D"), yaxis=dict(gridcolor="#30363D")
    )
    st.plotly_chart(fig_spd_def, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    # Defect Rate by Operation Mode (box)
    fig_box = px.box(
        fdf, x="Operation_Mode", y="Quality_Control_Defect_Rate_%",
        color="Operation_Mode", title="Defect Rate by Operation Mode",
        color_discrete_sequence=["#00FFB2", "#FFD700", "#4FC3F7", "#FF8C00"]
    )
    fig_box.update_layout(
        paper_bgcolor=COLORS["card"], plot_bgcolor=COLORS["card"],
        font_color="#E6EDF3", title_font_color="#E6EDF3",
        xaxis=dict(gridcolor="#30363D"), yaxis=dict(gridcolor="#30363D"),
        showlegend=False
    )
    st.plotly_chart(fig_box, use_container_width=True)

with col4:
    # Error frequency by hour
    hourly_err = fdf.groupby("Hour")["Error_Rate_%"].mean().reset_index()
    fig_hour = px.bar(
        hourly_err, x="Hour", y="Error_Rate_%",
        title="Average Error Rate by Hour of Day",
        color="Error_Rate_%",
        color_continuous_scale=["#00FFB2", "#FFD700", "#FF4F4F"]
    )
    fig_hour.update_layout(
        paper_bgcolor=COLORS["card"], plot_bgcolor=COLORS["card"],
        font_color="#E6EDF3", title_font_color="#E6EDF3",
        xaxis=dict(gridcolor="#30363D"), yaxis=dict(gridcolor="#30363D"),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_hour, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# MODULE 4 – EFFICIENCY DIAGNOSTICS VIEW
# ════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">📊 Efficiency Diagnostics View</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Stacked efficiency by operation mode
    eff_mode = fdf.groupby(["Operation_Mode", "Efficiency_Status"]).size().reset_index(name="Count")
    fig_stack = px.bar(
        eff_mode, x="Operation_Mode", y="Count", color="Efficiency_Status",
        color_discrete_map=COLORS, barmode="stack",
        title="Efficiency Distribution by Operation Mode"
    )
    fig_stack.update_layout(
        paper_bgcolor=COLORS["card"], plot_bgcolor=COLORS["card"],
        font_color="#E6EDF3", title_font_color="#E6EDF3",
        xaxis=dict(gridcolor="#30363D"), yaxis=dict(gridcolor="#30363D")
    )
    st.plotly_chart(fig_stack, use_container_width=True)

with col2:
    # Metric comparison scatter (user-selected)
    fig_cmp = px.scatter(
        sample_plot, x=compare_x, y=compare_y,
        color="Efficiency_Status", color_discrete_map=COLORS,
        opacity=0.4, title=f"{compare_x.replace('_',' ')} vs {compare_y.replace('_',' ')}",
        marginal_x="histogram", marginal_y="histogram"
    )
    fig_cmp.update_layout(
        paper_bgcolor=COLORS["card"], plot_bgcolor=COLORS["card"],
        font_color="#E6EDF3", title_font_color="#E6EDF3",
        xaxis=dict(gridcolor="#30363D"), yaxis=dict(gridcolor="#30363D")
    )
    st.plotly_chart(fig_cmp, use_container_width=True)

# Correlation Heatmap
st.markdown("#### 🔗 Feature Correlation Matrix")
numeric_cols = [
    "Temperature_C", "Vibration_Hz", "Power_Consumption_kW",
    "Network_Latency_ms", "Packet_Loss_%",
    "Quality_Control_Defect_Rate_%", "Production_Speed_units_per_hr",
    "Predictive_Maintenance_Score", "Error_Rate_%", "Machine_Health_Index"
]
short_names = ["Temp", "Vib", "Power", "Latency", "PktLoss",
               "Defect", "Speed", "MaintScore", "Error", "Health"]
corr = fdf[numeric_cols].corr()
fig_corr = go.Figure(data=go.Heatmap(
    z=corr.values.tolist(),
    x=short_names, y=short_names,
    colorscale="RdYlGn", zmin=-1, zmax=1,
    text=[[f"{v:.2f}" for v in row] for row in corr.values],
    texttemplate="%{text}", textfont={"size": 9, "color": "black"}
))
fig_corr.update_layout(
    paper_bgcolor=COLORS["card"], plot_bgcolor=COLORS["card"],
    font_color="#E6EDF3", height=450, margin=dict(t=20, b=20, l=20, r=20)
)
st.plotly_chart(fig_corr, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    "<center style='color:#8B949E;font-size:0.8rem;'>"
    "🏭 Thales Group Manufacturing Analytics &nbsp;|&nbsp; "
    "6G-Enabled Smart Factory &nbsp;|&nbsp; "
    "Unified Mentor Internship Project &nbsp;|&nbsp; Jones"
    "</center>",
    unsafe_allow_html=True
)