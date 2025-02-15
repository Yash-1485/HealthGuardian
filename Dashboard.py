import streamlit as st
from User import User
from Fetch_Health_Data import fetch_today_data

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
        st.write(f"💖 Blood Pressure: {data[3]}")
        st.write(f"💓 Heartbeat: {data[4]} bpm")
        st.write(f"🍬 Sugar Level: {data[5]} mg/dL")
        st.write(f"🫁 Oxygen Level: {data[6]}%")
        st.write(f"⚖ Weight: {data[7]} kg")
        st.write(f"🌡 Temperature: {data[8]}°C")
        st.write(f"📊 BMI: {data[9]}")
    else:
        st.warning("No health data found for today. Please enter your health details.")
