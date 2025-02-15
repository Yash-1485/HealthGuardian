import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from Fetch_Health_Data import fetch_health_data

def plot_health_data(user_id, period, graph_type):
    data = fetch_health_data(user_id, period)
    
    if data is None or data.empty:
        st.warning(f"No {period} data available. Please enter health records.")
        return
    
    dates = data["record_date"]
    
    metrics = {
        "Blood Pressure (Systolic)": data["bp_systolic"],
        "Blood Pressure (Diastolic)": data["bp_diastolic"],
        "Heartbeat": data["heartbeat"],
        "Sugar Level": data["sugar"],
        "Oxygen Level": data["oxygen"],
        "Weight": data["weight"],
        "Temperature": data["temperature"],
        "BMI": data["bmi"]
    }
    
    fig, axs = plt.subplots(len(metrics), 1, figsize=(8, 5 * len(metrics)))
    
    for i, (label, values) in enumerate(metrics.items()):
        x_vals = np.arange(len(dates))
        
        if graph_type == "Line":
            axs[i].plot(x_vals, values, marker="o", linestyle="-", label=label, color="blue")
        elif graph_type == "Bar":
            axs[i].bar(x_vals, values, color="green", label=label)
        elif graph_type == "Histogram":
            axs[i].hist(values, bins=10, color="purple", alpha=0.7, label=label)
        elif graph_type == "Scatter":
            axs[i].scatter(x_vals, values, color="red", label=label)
        elif graph_type == "Pie" and i == 0:  # Pie chart can only be done for one metric
            fig_pie, ax_pie = plt.subplots()
            ax_pie.pie(values, labels=dates, autopct='%1.1f%%', startangle=140)
            ax_pie.set_title(label)
            st.pyplot(fig_pie)
            continue

        axs[i].set_xticks(x_vals)
        axs[i].set_xticklabels(dates, rotation=45)
        axs[i].set_title(label)
        axs[i].legend()
    
    plt.tight_layout()
    st.pyplot(fig)
