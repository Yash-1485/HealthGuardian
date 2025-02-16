import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from Fetch_Health_Data import fetch_health_data

path='CSVs'
def plot_health_data(user_id, period, graph_type):
    data = fetch_health_data(user_id, period)[0]
    df = fetch_health_data(user_id, period)[1]
    
    if data is None or data.empty:
        st.warning(f"No {period} data available. Please enter health records.")
        return
    colors=['darkred','brown','firebrick','royalblue','cyan','m','red','olive']
    dates = data["record_date"]
    x_vals = np.arange(len(dates))  # Convert to numerical range

    metrics = {
        "Blood Pressure (Systolic)": data["bp_systolic"].astype(float),
        "Blood Pressure (Diastolic)": data["bp_diastolic"].astype(float),
        "Heartbeat": data["heartbeat"].astype(float),
        "Sugar Level": data["sugar"].astype(float),
        "Oxygen Level": data["oxygen"].astype(float),
        "Weight": data["weight"].astype(float),
        "Temperature": data["temperature"].astype(float),
        "BMI": data["bmi"].astype(float)
    }
    
    fig, axs = plt.subplots(len(metrics), 1, figsize=(8, 5 * len(metrics)))

    for i, (label, values) in enumerate(metrics.items()):
        xmin, xmax, ymin, ymax = setAxis(label, x_vals, values)  # Get limits
        axs[i].set_xlim([xmin, xmax])
        axs[i].set_ylim([ymin, ymax])  # Apply category-specific y-axis limits
        
        if graph_type == "Line":
            axs[i].plot(x_vals, values, marker="o", linestyle="-", color=colors[i], label=label)
        elif graph_type == "Bar":
            axs[i].bar(x_vals, values, color=colors[i], label=label)
        elif graph_type == "Histogram":
            axs[i].hist(values, bins=10, color=colors[i], alpha=0.7, label=label)
        elif graph_type == "Scatter":
            axs[i].scatter(x_vals, values, color=colors[i], label=label)
        elif graph_type == "Pie" and i == 0:  # Pie chart for only first metric
            fig_pie, ax_pie = plt.subplots()
            ax_pie.pie(values, labels=dates, autopct='%1.1f%%', startangle=140)
            ax_pie.set_title(label)
            st.pyplot(fig_pie)
            continue

        axs[i].set_xticks(x_vals)
        axs[i].set_xticklabels(dates, rotation=90)
        axs[i].set_title(label)
        axs[i].legend()

    btn=st.button(label="Export CSV File")
    if(btn):
        df.to_csv(path+f"/{period}_data.csv")
    
    plt.tight_layout()
    st.pyplot(fig)

def setAxis(parameter, x_vals, values):
    min_y, max_y = min(values), max(values)
    axis_limits = {
        "Blood Pressure (Systolic)": (80, 200),
        "Blood Pressure (Diastolic)": (50, 120),
        "Heartbeat": (40, 180),
        "Sugar Level": (50, 250),
        "Oxygen Level": (80, 100),
        "Weight": (30, 150),
        "Temperature": (15, 50),
        "BMI": (10, 40),
    }

    ymin, ymax = axis_limits.get(parameter, (min_y - 10, max_y + 10))
    xmin, xmax = 0, len(x_vals) - 5

    return xmin, xmax, ymin, ymax
