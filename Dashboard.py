import streamlit as st
from User import User
from Fetch_Today_Health_Data import fetch_today_data
from Plot_Health_Data import *

def run():
    st.title("Your Health Dashboard")

    user:User=st.session_state["User"]
    user_id = user.uid
    data = fetch_today_data(user_id)

    if not st.session_state['today']:
        st.warning("You haven't logged today's data!")
        return
    if data:
        st.subheader("Today's Health Data")
        st.write(f"📅 Date: {data[2]}")
        st.write(f"💖 Blood Pressure: {data[3]}/{data[4]}")
        st.write(f"💓 Heartbeat: {data[5]} bpm")
        st.write(f"🍬 Sugar Level: {data[6]} mg/dL")
        st.write(f"🫁 Oxygen Level: {data[7]}%")
        st.write(f"⚖ Weight: {data[8]} kg")
        st.write(f"🌡 Temperature: {data[9]}°C")
        st.write(f"📊 BMI: {data[10]}")
    else:
        st.warning("No health data found for today. Please enter your health details.")
        
    period = st.radio("Select Time Period", ["Daily", "Weekly", "Monthly"])
    graph_type = st.selectbox("Select Graph Type", ["Line", "Bar", "Scatter"])
    
    plot_health_data(user_id, period.lower(), graph_type)