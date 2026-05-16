"""
=============================================================================
THALES GROUP MANUFACTURING - EDA SCRIPT
Manufacturing Process Health and Operational Efficiency Analysis
in 6G-Enabled Smart Factories
=============================================================================
Author  : Jones
Project : Unified Mentor Internship
Dataset : Thales_Group_Manufacturing.csv
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings("ignore")

# ── Plot Style ──────────────────────────────────────────────────────────────
plt.style.use("dark_background")
COLORS = {
    "High":   "#00FFB2",
    "Medium": "#FFD700",
    "Low":    "#FF4F4F",
    "accent": "#4FC3F7",
    "bg":     "#0D1117",
    "card":   "#161B22",
    "text":   "#E6EDF3",
}
PALETTE = ["#00FFB2", "#FFD700", "#FF4F4F", "#4FC3F7", "#FF8C00", "#A78BFA"]

# ── 1. Load & Inspect ────────────────────────────────────────────────────────
print("=" * 60)
print("  THALES MANUFACTURING – EDA")
print("=" * 60)

df = pd.read_csv("Thales_Group_Manufacturing.csv")

# Parse datetime
df["Datetime"] = pd.to_datetime(
    df["Date"] + " " + df["Timestamp"], dayfirst=True, errors="coerce"
)
df["Date"]   = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
df["Hour"]   = df["Datetime"].dt.hour
df["DayOfWeek"] = df["Datetime"].dt.day_name()

print(f"\n📦 Shape       : {df.shape}")
print(f"📅 Date range  : {df['Date'].min().date()} → {df['Date'].max().date()}")
print(f"🔢 Machines    : {df['Machine_ID'].nunique()} unique")
print(f"⚙️  Op modes   : {df['Operation_Mode'].unique()}")

print("\n─── Dtypes ───")
print(df.dtypes)

print("\n─── Missing values ───")
print(df.isnull().sum())

print("\n─── Descriptive Statistics ───")
numeric_cols = [
    "Temperature_C", "Vibration_Hz", "Power_Consumption_kW",
    "Network_Latency_ms", "Packet_Loss_%",
    "Quality_Control_Defect_Rate_%", "Production_Speed_units_per_hr",
    "Predictive_Maintenance_Score", "Error_Rate_%",
]
print(df[numeric_cols].describe().round(3).to_string())

# ── 2. Efficiency Distribution ───────────────────────────────────────────────
eff_counts = df["Efficiency_Status"].value_counts()
eff_pct    = df["Efficiency_Status"].value_counts(normalize=True) * 100
print("\n─── Efficiency Status Distribution ───")
for status, pct in eff_pct.items():
    print(f"  {status:8s}: {pct:.1f}%")

# ── 3. KPIs ──────────────────────────────────────────────────────────────────
df["Machine_Health_Index"] = (
    (1 - df["Temperature_C"] / 100) * 0.4
    + (1 - df["Vibration_Hz"] / 5)  * 0.3
    + (1 - df["Power_Consumption_kW"] / 10) * 0.3
).clip(0, 1)

kpi_summary = df.groupby("Efficiency_Status").agg(
    Avg_Production_Speed=("Production_Speed_units_per_hr", "mean"),
    Avg_Defect_Rate=("Quality_Control_Defect_Rate_%", "mean"),
    Avg_Error_Rate=("Error_Rate_%", "mean"),
    Avg_Machine_Health=("Machine_Health_Index", "mean"),
    Count=("Machine_ID", "count"),
).round(3)
print("\n─── KPI Summary by Efficiency Status ───")
print(kpi_summary.to_string())

# ── 4. Machine-Level Summary ──────────────────────────────────────────────────
machine_summary = df.groupby("Machine_ID").agg(
    Avg_Temp=("Temperature_C", "mean"),
    Avg_Vibration=("Vibration_Hz", "mean"),
    Avg_Power=("Power_Consumption_kW", "mean"),
    Avg_Defect=("Quality_Control_Defect_Rate_%", "mean"),
    Avg_Speed=("Production_Speed_units_per_hr", "mean"),
    Avg_Error=("Error_Rate_%", "mean"),
    Health_Index=("Machine_Health_Index", "mean"),
).round(3)
machine_summary["High_Eff_%"] = (
    df[df["Efficiency_Status"] == "High"]
    .groupby("Machine_ID").size() / df.groupby("Machine_ID").size() * 100
).reindex(machine_summary.index).fillna(0).round(1)

print("\n─── Top 10 Machines by Health Index ───")
print(machine_summary.sort_values("Health_Index", ascending=False).head(10).to_string())

print("\n─── Bottom 10 Machines (Lowest Health) ───")
print(machine_summary.sort_values("Health_Index").head(10).to_string())

# ────────────────────────────────────────────────────────────────────────────
# ██  VISUALIZATIONS
# ────────────────────────────────────────────────────────────────────────────

# ── Fig 1 : Overview Dashboard ───────────────────────────────────────────────
fig = plt.figure(figsize=(20, 12), facecolor=COLORS["bg"])
fig.suptitle(
    "Thales Group Manufacturing — Operational Health Overview",
    fontsize=22, fontweight="bold", color=COLORS["text"], y=0.97,
)
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

# (a) Efficiency Pie
ax1 = fig.add_subplot(gs[0, 0])
pie_colors = [COLORS[s] for s in eff_counts.index]
wedges, texts, autotexts = ax1.pie(
    eff_counts, labels=eff_counts.index,
    autopct="%1.1f%%", colors=pie_colors,
    startangle=90, pctdistance=0.75,
    wedgeprops=dict(width=0.6, edgecolor=COLORS["bg"], linewidth=2),
)
for t in texts:   t.set_color(COLORS["text"]); t.set_fontsize(11)
for at in autotexts: at.set_color(COLORS["bg"]); at.set_fontweight("bold")
ax1.set_title("Efficiency Status Distribution", color=COLORS["text"], fontsize=13, pad=10)

# (b) Operation Mode bar
ax2 = fig.add_subplot(gs[0, 1])
op_counts = df["Operation_Mode"].value_counts()
bars = ax2.bar(op_counts.index, op_counts.values,
               color=PALETTE[:len(op_counts)], edgecolor=COLORS["bg"], linewidth=1.2)
for bar in bars:
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200,
             f"{bar.get_height():,}", ha="center", va="bottom",
             color=COLORS["text"], fontsize=9)
ax2.set_title("Records by Operation Mode", color=COLORS["text"], fontsize=13)
ax2.tick_params(colors=COLORS["text"])
ax2.set_facecolor(COLORS["card"])
ax2.spines[:].set_color("#30363D")

# (c) Sensor Averages by Efficiency
ax3 = fig.add_subplot(gs[0, 2])
metrics = ["Temperature_C", "Vibration_Hz", "Power_Consumption_kW"]
eff_order = ["High", "Medium", "Low"]
x = np.arange(len(metrics))
width = 0.25
for i, eff in enumerate(eff_order):
    vals = [df[df["Efficiency_Status"] == eff][m].mean() for m in metrics]
    ax3.bar(x + i * width, vals, width, label=eff,
            color=COLORS[eff], edgecolor=COLORS["bg"], linewidth=1)
ax3.set_xticks(x + width)
ax3.set_xticklabels(["Temp (°C)", "Vibration (Hz)", "Power (kW)"], color=COLORS["text"])
ax3.set_title("Avg Sensor Readings by Efficiency", color=COLORS["text"], fontsize=13)
ax3.legend(facecolor=COLORS["card"], labelcolor=COLORS["text"], fontsize=9)
ax3.tick_params(colors=COLORS["text"]); ax3.set_facecolor(COLORS["card"])
ax3.spines[:].set_color("#30363D")

# (d) Production Speed Distribution
ax4 = fig.add_subplot(gs[1, 0])
for eff in eff_order:
    subset = df[df["Efficiency_Status"] == eff]["Production_Speed_units_per_hr"]
    ax4.hist(subset, bins=40, alpha=0.65, label=eff, color=COLORS[eff])
ax4.set_title("Production Speed Distribution", color=COLORS["text"], fontsize=13)
ax4.set_xlabel("Units/hr", color=COLORS["text"])
ax4.legend(facecolor=COLORS["card"], labelcolor=COLORS["text"], fontsize=9)
ax4.tick_params(colors=COLORS["text"]); ax4.set_facecolor(COLORS["card"])
ax4.spines[:].set_color("#30363D")

# (e) Defect Rate vs Production Speed scatter
ax5 = fig.add_subplot(gs[1, 1])
sample = df.sample(min(5000, len(df)), random_state=42)
for eff in eff_order:
    s = sample[sample["Efficiency_Status"] == eff]
    ax5.scatter(s["Production_Speed_units_per_hr"],
                s["Quality_Control_Defect_Rate_%"],
                alpha=0.35, s=8, c=COLORS[eff], label=eff)
ax5.set_xlabel("Production Speed (units/hr)", color=COLORS["text"])
ax5.set_ylabel("Defect Rate (%)", color=COLORS["text"])
ax5.set_title("Speed vs Defect Rate", color=COLORS["text"], fontsize=13)
ax5.legend(facecolor=COLORS["card"], labelcolor=COLORS["text"], fontsize=9, markerscale=3)
ax5.tick_params(colors=COLORS["text"]); ax5.set_facecolor(COLORS["card"])
ax5.spines[:].set_color("#30363D")

# (f) Error Rate by Operation Mode
ax6 = fig.add_subplot(gs[1, 2])
err_by_mode = df.groupby("Operation_Mode")["Error_Rate_%"].mean().sort_values()
ax6.barh(err_by_mode.index, err_by_mode.values,
         color=[PALETTE[i] for i in range(len(err_by_mode))],
         edgecolor=COLORS["bg"], linewidth=1.2)
for i, (val, label) in enumerate(zip(err_by_mode.values, err_by_mode.index)):
    ax6.text(val + 0.05, i, f"{val:.2f}%", va="center", color=COLORS["text"], fontsize=10)
ax6.set_title("Avg Error Rate by Operation Mode", color=COLORS["text"], fontsize=13)
ax6.tick_params(colors=COLORS["text"]); ax6.set_facecolor(COLORS["card"])
ax6.spines[:].set_color("#30363D")

plt.savefig("fig1_overview_dashboard.png", dpi=150, bbox_inches="tight",
            facecolor=COLORS["bg"])
print("\n✅ Saved: fig1_overview_dashboard.png")
plt.close()

# ── Fig 2 : Machine Health Analysis ──────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(18, 10), facecolor=COLORS["bg"])
fig.suptitle("Machine-Level Sensor Health Analysis",
             fontsize=20, fontweight="bold", color=COLORS["text"], y=0.98)

# (a) Top/Bottom 15 machines by Health Index
ax = axes[0, 0]
top15 = machine_summary.sort_values("Health_Index", ascending=False).head(15)
bot15 = machine_summary.sort_values("Health_Index").head(15)
combined = pd.concat([top15, bot15]).drop_duplicates()
colors_bar = [COLORS["High"] if v >= combined["Health_Index"].median()
              else COLORS["Low"] for v in combined["Health_Index"]]
ax.barh([f"M-{int(m)}" for m in combined.index],
        combined["Health_Index"], color=colors_bar,
        edgecolor=COLORS["bg"], linewidth=0.8)
ax.axvline(combined["Health_Index"].median(), color=COLORS["accent"],
           linestyle="--", linewidth=1.5, label="Median")
ax.set_title("Machine Health Index (Top & Bottom)", color=COLORS["text"], fontsize=12)
ax.tick_params(colors=COLORS["text"]); ax.set_facecolor(COLORS["card"])
ax.spines[:].set_color("#30363D"); ax.legend(facecolor=COLORS["card"], labelcolor=COLORS["text"])

# (b) Temperature vs Vibration per machine
ax = axes[0, 1]
sc = ax.scatter(machine_summary["Avg_Temp"], machine_summary["Avg_Vibration"],
                c=machine_summary["Health_Index"], cmap="RdYlGn",
                s=100, edgecolors=COLORS["bg"], linewidth=0.8, vmin=0, vmax=1)
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label("Health Index", color=COLORS["text"])
cbar.ax.yaxis.set_tick_params(color=COLORS["text"])
plt.setp(cbar.ax.yaxis.get_ticklabels(), color=COLORS["text"])
ax.set_xlabel("Avg Temperature (°C)", color=COLORS["text"])
ax.set_ylabel("Avg Vibration (Hz)", color=COLORS["text"])
ax.set_title("Temperature vs Vibration (colour=Health)", color=COLORS["text"], fontsize=12)
ax.tick_params(colors=COLORS["text"]); ax.set_facecolor(COLORS["card"])
ax.spines[:].set_color("#30363D")

# (c) Predictive Maintenance Score distribution
ax = axes[1, 0]
for eff in eff_order:
    vals = df[df["Efficiency_Status"] == eff]["Predictive_Maintenance_Score"]
    ax.hist(vals, bins=30, alpha=0.65, label=eff, color=COLORS[eff])
ax.set_title("Predictive Maintenance Score by Efficiency", color=COLORS["text"], fontsize=12)
ax.set_xlabel("Score", color=COLORS["text"])
ax.legend(facecolor=COLORS["card"], labelcolor=COLORS["text"])
ax.tick_params(colors=COLORS["text"]); ax.set_facecolor(COLORS["card"])
ax.spines[:].set_color("#30363D")

# (d) Power Consumption by Operation Mode
ax = axes[1, 1]
power_mode = df.groupby(["Operation_Mode", "Efficiency_Status"])["Power_Consumption_kW"].mean().unstack()
power_mode.plot(kind="bar", ax=ax, color=[COLORS[c] for c in power_mode.columns],
                edgecolor=COLORS["bg"], linewidth=0.8)
ax.set_title("Avg Power Consumption: Mode × Efficiency", color=COLORS["text"], fontsize=12)
ax.set_xlabel(""); ax.tick_params(colors=COLORS["text"], rotation=0)
ax.legend(facecolor=COLORS["card"], labelcolor=COLORS["text"])
ax.set_facecolor(COLORS["card"]); ax.spines[:].set_color("#30363D")

for a in axes.flat:
    for spine in a.spines.values(): spine.set_color("#30363D")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("fig2_machine_health.png", dpi=150, bbox_inches="tight",
            facecolor=COLORS["bg"])
print("✅ Saved: fig2_machine_health.png")
plt.close()

# ── Fig 3 : Quality & Error Analysis ─────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(18, 10), facecolor=COLORS["bg"])
fig.suptitle("Quality & Error Rate Analysis",
             fontsize=20, fontweight="bold", color=COLORS["text"], y=0.98)

# (a) Defect Rate boxplot by Operation Mode
ax = axes[0, 0]
op_modes = df["Operation_Mode"].unique()
data_bp  = [df[df["Operation_Mode"] == m]["Quality_Control_Defect_Rate_%"].values
            for m in op_modes]
bp = ax.boxplot(data_bp, labels=op_modes, patch_artist=True,
                medianprops=dict(color=COLORS["bg"], linewidth=2))
for patch, color in zip(bp["boxes"], PALETTE):
    patch.set_facecolor(color); patch.set_alpha(0.8)
ax.set_title("Defect Rate by Operation Mode", color=COLORS["text"], fontsize=12)
ax.set_ylabel("Defect Rate (%)", color=COLORS["text"])
ax.tick_params(colors=COLORS["text"]); ax.set_facecolor(COLORS["card"])
ax.spines[:].set_color("#30363D")

# (b) Error Rate heatmap by hour
ax = axes[0, 1]
hour_eff = df.pivot_table(values="Error_Rate_%", index="Hour",
                           columns="Efficiency_Status", aggfunc="mean")
hour_eff = hour_eff[["High", "Medium", "Low"]] if "High" in hour_eff.columns else hour_eff
im = ax.imshow(hour_eff.T, aspect="auto", cmap="RdYlGn_r")
ax.set_xticks(range(len(hour_eff.index))); ax.set_xticklabels(hour_eff.index, fontsize=7)
ax.set_yticks(range(len(hour_eff.columns))); ax.set_yticklabels(hour_eff.columns)
ax.set_title("Hourly Error Rate Heatmap", color=COLORS["text"], fontsize=12)
ax.set_xlabel("Hour of Day", color=COLORS["text"])
plt.colorbar(im, ax=ax).set_label("Avg Error Rate %", color=COLORS["text"])
ax.tick_params(colors=COLORS["text"])

# (c) Defect Rate vs Temperature
ax = axes[1, 0]
for eff in eff_order:
    s = sample[sample["Efficiency_Status"] == eff]
    ax.scatter(s["Temperature_C"], s["Quality_Control_Defect_Rate_%"],
               alpha=0.3, s=8, c=COLORS[eff], label=eff)
ax.set_xlabel("Temperature (°C)", color=COLORS["text"])
ax.set_ylabel("Defect Rate (%)", color=COLORS["text"])
ax.set_title("Temperature vs Defect Rate", color=COLORS["text"], fontsize=12)
ax.legend(facecolor=COLORS["card"], labelcolor=COLORS["text"], markerscale=3)
ax.tick_params(colors=COLORS["text"]); ax.set_facecolor(COLORS["card"])
ax.spines[:].set_color("#30363D")

# (d) Packet Loss vs Error Rate
ax = axes[1, 1]
for eff in eff_order:
    s = sample[sample["Efficiency_Status"] == eff]
    ax.scatter(s["Packet_Loss_%"], s["Error_Rate_%"],
               alpha=0.3, s=8, c=COLORS[eff], label=eff)
ax.set_xlabel("Packet Loss (%)", color=COLORS["text"])
ax.set_ylabel("Error Rate (%)", color=COLORS["text"])
ax.set_title("6G Packet Loss vs Operational Error Rate", color=COLORS["text"], fontsize=12)
ax.legend(facecolor=COLORS["card"], labelcolor=COLORS["text"], markerscale=3)
ax.tick_params(colors=COLORS["text"]); ax.set_facecolor(COLORS["card"])
ax.spines[:].set_color("#30363D")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("fig3_quality_error.png", dpi=150, bbox_inches="tight",
            facecolor=COLORS["bg"])
print("✅ Saved: fig3_quality_error.png")
plt.close()

# ── Fig 4 : Efficiency Diagnostics ────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(18, 10), facecolor=COLORS["bg"])
fig.suptitle("Efficiency Status Diagnostics",
             fontsize=20, fontweight="bold", color=COLORS["text"], y=0.98)

# (a) Efficiency by Operation Mode
ax = axes[0, 0]
eff_mode = df.groupby(["Operation_Mode", "Efficiency_Status"]).size().unstack(fill_value=0)
eff_mode_pct = eff_mode.div(eff_mode.sum(axis=1), axis=0) * 100
bottom = np.zeros(len(eff_mode_pct))
for eff in ["High", "Medium", "Low"]:
    if eff in eff_mode_pct.columns:
        ax.bar(eff_mode_pct.index, eff_mode_pct[eff], bottom=bottom,
               label=eff, color=COLORS[eff])
        bottom += eff_mode_pct[eff].values
ax.set_title("Efficiency % by Operation Mode", color=COLORS["text"], fontsize=12)
ax.set_ylabel("%", color=COLORS["text"])
ax.legend(facecolor=COLORS["card"], labelcolor=COLORS["text"])
ax.tick_params(colors=COLORS["text"]); ax.set_facecolor(COLORS["card"])
ax.spines[:].set_color("#30363D")

# (b) Network Latency by Efficiency
ax = axes[0, 1]
for eff in eff_order:
    vals = df[df["Efficiency_Status"] == eff]["Network_Latency_ms"]
    ax.hist(vals, bins=30, alpha=0.65, label=eff, color=COLORS[eff])
ax.set_title("Network Latency Distribution", color=COLORS["text"], fontsize=12)
ax.set_xlabel("Latency (ms)", color=COLORS["text"])
ax.legend(facecolor=COLORS["card"], labelcolor=COLORS["text"])
ax.tick_params(colors=COLORS["text"]); ax.set_facecolor(COLORS["card"])
ax.spines[:].set_color("#30363D")

# (c) Production trend over time (daily avg)
ax = axes[1, 0]
daily = df.groupby("Date")["Production_Speed_units_per_hr"].mean()
ax.plot(daily.index, daily.values, color=COLORS["accent"], linewidth=1.5)
ax.fill_between(daily.index, daily.values, alpha=0.15, color=COLORS["accent"])
ax.set_title("Daily Average Production Speed", color=COLORS["text"], fontsize=12)
ax.set_xlabel("Date", color=COLORS["text"])
ax.set_ylabel("Units/hr", color=COLORS["text"])
ax.tick_params(colors=COLORS["text"]); ax.set_facecolor(COLORS["card"])
ax.spines[:].set_color("#30363D")

# (d) Correlation heatmap
ax = axes[1, 1]
corr = df[numeric_cols].corr()
im = ax.imshow(corr, cmap="RdYlGn", vmin=-1, vmax=1)
ax.set_xticks(range(len(numeric_cols)))
ax.set_yticks(range(len(numeric_cols)))
short = ["Temp", "Vib", "Power", "Latency", "PktLoss", "Defect", "Speed", "MaintScore", "Error"]
ax.set_xticklabels(short, rotation=45, ha="right", fontsize=8, color=COLORS["text"])
ax.set_yticklabels(short, fontsize=8, color=COLORS["text"])
for i in range(len(numeric_cols)):
    for j in range(len(numeric_cols)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center",
                fontsize=6, color="black")
plt.colorbar(im, ax=ax).set_label("Correlation", color=COLORS["text"])
ax.set_title("Feature Correlation Matrix", color=COLORS["text"], fontsize=12)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("fig4_efficiency_diagnostics.png", dpi=150, bbox_inches="tight",
            facecolor=COLORS["bg"])
print("✅ Saved: fig4_efficiency_diagnostics.png")
plt.close()

# ── 5. Final KPI Summary Table ────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  KEY PERFORMANCE INDICATORS SUMMARY")
print("=" * 60)

kpis = {
    "Machine Health Index (avg)":
        f"{df['Machine_Health_Index'].mean():.4f}",
    "Average Production Speed (units/hr)":
        f"{df['Production_Speed_units_per_hr'].mean():.2f}",
    "Defect Density Score (avg %)":
        f"{df['Quality_Control_Defect_Rate_%'].mean():.2f}%",
    "Error Frequency Index (avg %)":
        f"{df['Error_Rate_%'].mean():.2f}%",
    "High Efficiency %":
        f"{eff_pct.get('High', 0):.1f}%",
    "Medium Efficiency %":
        f"{eff_pct.get('Medium', 0):.1f}%",
    "Low Efficiency %":
        f"{eff_pct.get('Low', 0):.1f}%",
    "Machines in dataset":
        str(df["Machine_ID"].nunique()),
    "Total records":
        f"{len(df):,}",
}
for k, v in kpis.items():
    print(f"  {k:<45}: {v}")

print("\n✅ EDA Complete — 4 figures saved.")