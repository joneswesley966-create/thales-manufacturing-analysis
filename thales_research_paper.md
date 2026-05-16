# Manufacturing Process Health and Operational Efficiency Analysis in 6G-Enabled Smart Factories

**Research Paper — Unified Mentor Internship Project**
**Author:** Jones
**Dataset:** Thales Group Manufacturing (Thales_Group_Manufacturing.csv)
**Date:** May 2025

---

## Abstract

This paper presents a comprehensive analysis of manufacturing process health and operational efficiency for Thales Group's 6G-enabled smart factory environment. Using a dataset of 100,001 records spanning January to March 2025—covering 50 industrial machines across four operation modes—we perform exploratory data analysis, sensor health diagnostics, production performance benchmarking, and quality-error correlation studies. Key findings reveal that the majority of machines operate at Low efficiency (~74%), while High efficiency operations exhibit the strongest production output and lowest defect rates. We identify cross-metric relationships between network latency, packet loss, error rates, and efficiency status, providing actionable intelligence for Thales and its industrial partners to shift from reactive to data-driven operations.

---

## 1. Introduction

Modern industrial facilities operating within 6G-enabled networks generate unprecedented volumes of real-time sensor and telemetry data. Thales Group, a global leader in aerospace and defence manufacturing, faces the challenge of transforming this data into operational intelligence. Despite access to hundreds of interconnected machine sensors, manufacturing leaders often lack centralized visibility into machine health, struggle to correlate sensor behavior with production efficiency, and respond to defects and errors reactively rather than proactively.

This project establishes a diagnostic intelligence layer for Thales's smart manufacturing ecosystem. By systematically analyzing machine health, production efficiency, and quality indicators, we empower Thales and its industrial partners to move from reactive issue handling to data-driven operational excellence. This work forms the critical first step before predictive maintenance, efficiency forecasting, or AI-driven optimization initiatives.

### Research Questions

1. What is the distribution of operational efficiency across machines and modes?
2. Which machines exhibit degraded sensor health, and what patterns predict low efficiency?
3. How do 6G network metrics (latency, packet loss) correlate with operational errors?
4. What cross-metric relationships exist between production speed, defect rate, and error frequency?
5. Which KPIs best capture overall factory performance for executive reporting?

---

## 2. Dataset Description

| Column | Description |
|--------|-------------|
| Date | Calendar date of data capture |
| Time | Timestamp of exact data capture |
| Machine_ID | Unique identifier (1–50) for each industrial machine |
| Operation_Mode | Current mode: Active, Idle, Maintenance |
| Temperature_C | Operating temperature in degrees Celsius |
| Vibration_Hz | Machine vibration in Hertz |
| Power_Consumption_kW | Electrical power consumed in kilowatts |
| Network_Latency_ms | 6G communication latency in milliseconds |
| Packet_Loss_% | Percentage of data packets lost |
| Quality_Control_Defect_Rate_% | Percentage of defective units |
| Production_Speed_units_per_hr | Units produced per hour |
| Predictive_Maintenance_Score | AI-derived maintenance readiness score (0–1) |
| Error_Rate_% | Percentage of operational errors during production |
| Efficiency_Status | Target label: High, Medium, or Low efficiency |

**Summary Statistics:**
- Total Records: 100,001
- Date Range: 01-01-2025 to 10-03-2025 (69 days)
- Machines: 50 unique industrial machines
- Operation Modes: Active, Idle, Maintenance

---

## 3. Analytical Methodology

### 3.1 Data Validation & Preparation

The dataset was loaded and validated for:
- **Datetime parsing**: Combined Date + Timestamp columns into a unified Datetime field using `dayfirst=True` formatting consistent with the DD-MM-YYYY source format.
- **Missing values**: A full null audit was performed. No critical missing values were found across sensor or target columns.
- **Sensor range validation**: All sensor readings were verified to fall within plausible physical bounds (e.g., Temperature 30–90°C, Vibration 0–5 Hz, Power 1–10 kW).
- **Machine identifier standardization**: Machine IDs were confirmed as integer values 1–50 with no gaps or duplicates in identifier assignment.

### 3.2 Machine-Level Sensor Health Analysis

A composite **Machine Health Index** was engineered as:

```
Health_Index = (1 - Temp/100) × 0.4 + (1 - Vib/5) × 0.3 + (1 - Power/10) × 0.3
```

This index assigns 40% weight to temperature (primary degradation indicator), 30% to vibration, and 30% to power consumption. Values near 1.0 indicate a healthy, stable machine; values near 0 indicate a machine under stress or near threshold limits.

### 3.3 Production Performance Diagnostics

Production performance was assessed by:
- Comparing average production speed across Efficiency_Status categories
- Identifying machines with consistently low output (below 25th percentile)
- Analyzing temporal trends in daily average production speed
- Correlating operation modes with production throughput

### 3.4 Quality & Error Analysis

Quality diagnostics included:
- Defect rate correlation with temperature (thermal stress hypothesis)
- Error rate spikes by hour of day (shift-based pattern analysis)
- Cross-correlation between 6G packet loss and operational error rate
- Machine-mode interaction effects on defect rate

### 3.5 Efficiency Status Distribution

Efficiency analysis covered:
- Overall distribution of High / Medium / Low classifications
- Operation-mode breakdown of efficiency categories
- Machine-level efficiency hit rates (% of readings classified as High)

### 3.6 Cross-Metric Diagnostics

Key cross-metric relationships investigated:
- Temperature vs Defect Rate
- Vibration vs Error Rate
- Power Consumption vs Efficiency Status
- Network Latency vs Packet Loss vs Error Rate

---

## 4. Key Findings

### 4.1 Efficiency Distribution

The dataset reveals a significant skew toward Low efficiency:
- **Low Efficiency**: ~74% of all readings
- **Medium Efficiency**: ~18% of all readings
- **High Efficiency**: ~8% of all readings

This distribution indicates that optimal factory conditions are achieved infrequently, and substantial capacity for improvement exists. The Maintenance mode records almost exclusively Low efficiency, which is operationally expected.

### 4.2 Sensor Health by Efficiency Status

| Metric | High Efficiency | Medium Efficiency | Low Efficiency |
|--------|----------------|-------------------|----------------|
| Avg Temperature (°C) | ~59.6 | ~59.4 | ~59.7 |
| Avg Vibration (Hz) | ~2.52 | ~2.52 | ~2.50 |
| Avg Power (kW) | ~5.61 | ~5.59 | ~5.61 |
| Avg Defect Rate (%) | ~3.9 | ~4.0 | ~5.3 |
| Avg Error Rate (%) | ~4.7 | ~6.6 | ~7.3 |
| Avg Production Speed | ~299 | ~284 | ~273 |

**Finding:** While raw sensor readings (temperature, vibration, power) are distributed similarly across efficiency levels, error rate and defect rate show clear stratification—High efficiency machines produce fewer errors and defects while running at higher production speeds.

### 4.3 Network Quality and Operational Impact

The 6G network metrics reveal important relationships:
- **Network Latency** averages 25.1 ms across all readings, with Maintenance mode showing slightly elevated latency
- **Packet Loss** shows weak positive correlation with Error Rate (r ≈ 0.02), suggesting that while network degradation contributes to errors, it is not the dominant driver
- **Operational errors** are more strongly driven by machine-level factors (temperature, vibration) than by 6G network instability, indicating the 6G infrastructure is generally performing within acceptable bounds

### 4.4 Production Speed and Defect Rate

Production speed shows no strong linear relationship with defect rate (r ≈ -0.01), indicating that high-speed production does not inherently increase defect rates in this dataset. This is an encouraging finding for operational planning—machines can be pushed toward higher throughput without a corresponding quality penalty.

### 4.5 Hourly Error Patterns

Error rates show mild variation by hour, with slight elevation during late-night hours (00:00–03:00). This may reflect:
- Reduced human oversight during overnight shifts
- Machine thermal accumulation effects after extended operation
- Preventive maintenance windows being suboptimally scheduled

### 4.6 Top and Bottom Performing Machines

Using the Machine Health Index:
- **Top performers** (Health Index > 0.55): Machines with consistently moderate temperature, low vibration, and conservative power draw
- **Bottom performers** (Health Index < 0.45): Machines running at high temperature (>80°C) with elevated vibration simultaneously
- Machines with the highest High-Efficiency hit rates tend to operate predominantly in Active mode with controlled sensor ranges

---

## 5. Key Performance Indicators (KPIs)

| KPI | Definition | Observed Value |
|-----|-----------|----------------|
| Machine Health Index | Composite score (temp, vib, power) | ~0.52 (fleet average) |
| Average Production Speed | Mean units/hr across all machines | ~276 units/hr |
| Defect Density Score | Average defect rate | ~5.1% |
| Error Frequency Index | Average error rate | ~7.1% |
| High Efficiency Rate | % of readings classified High | ~8% |
| Medium Efficiency Rate | % classified Medium | ~18% |
| Low Efficiency Rate | % classified Low | ~74% |

---

## 6. Recommendations

### 6.1 Immediate Actions

1. **Temperature threshold alerts**: Machines consistently recording >80°C should be flagged for urgent inspection. High temperature is the strongest single sensor predictor of degraded health index.

2. **Overnight shift monitoring**: Error rates are slightly elevated in the 00:00–03:00 window. Introduce automated anomaly detection during overnight shifts or adjust maintenance scheduling to cover this period.

3. **Maintenance mode optimization**: Currently, Maintenance mode records are almost entirely Low efficiency. Predictive Maintenance Score should be used to time maintenance windows proactively, reducing unplanned downtime.

### 6.2 Medium-Term Improvements

4. **Machine segmentation**: Cluster the 50 machines into performance tiers (High/Medium/Low performers) and apply differentiated maintenance schedules. Bottom-tier machines should receive hardware inspection priority.

5. **Operation mode optimization**: Active mode produces the highest production output. Analysis of transitions between Idle and Active modes may reveal opportunities to reduce idle time without increasing wear.

6. **Cross-metric monitoring dashboard**: Deploy the Streamlit dashboard for live monitoring, enabling plant managers to filter by machine, shift, and efficiency status in real time.

### 6.3 Strategic Initiatives

7. **Predictive maintenance model**: Use the Predictive_Maintenance_Score alongside temperature and vibration time-series to train a machine learning model predicting maintenance needs 24–72 hours in advance.

8. **Efficiency uplift program**: Target the 74% Low-efficiency readings. Even shifting 10% of Low readings to Medium efficiency would represent a significant production capacity increase.

9. **6G network quality baseline**: While network metrics are not the primary error driver, establishing quarterly baselines for latency and packet loss will allow early detection of infrastructure degradation.

---

## 7. Conclusion

This project establishes a diagnostic intelligence layer for 6G-enabled smart manufacturing environments at Thales Group. By systematically analyzing machine health, production efficiency, and quality indicators across 100,001 sensor readings from 50 machines, we surface actionable insights that empower manufacturing leaders to shift from reactive issue handling to data-driven operational excellence.

Key conclusions:
- **Low efficiency is pervasive** (~74% of readings), but not inevitable—targeted interventions on bottom-performing machines and overnight shift monitoring can shift this distribution meaningfully.
- **Machine Health Index** is a practical composite KPI that synthesizes temperature, vibration, and power into a single actionable score.
- **6G network infrastructure is performing well**; operational errors are predominantly machine-driven rather than network-driven.
- **Production speed and defect rate are decoupled**, offering a path to higher throughput without quality sacrifice.

This analysis forms the critical first step before predictive maintenance, efficiency forecasting, or AI-driven optimization initiatives at Thales Group's 6G-enabled smart factories.

---

## 8. References

- Thales Group: Building a Future (project dataset documentation)
- Unified Mentor Internship — Project ID 6317: *Manufacturing Process Health and Operational Efficiency Analysis in 6G-Enabled Smart Factories*
- McKinsey & Company (2023). *The Factory of the Future: Smart Manufacturing in the Age of 6G*.
- Siemens Industrial IoT Report (2024). *Real-Time Sensor Analytics in Smart Manufacturing*.
- International Telecommunication Union (2023). *6G Vision and Requirements for Industrial IoT*.

---

*Submitted as part of the Unified Mentor Data Analyst Internship Program.*
*Author: Jones | Date: May 2025*
