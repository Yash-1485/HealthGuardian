import DB_Creadentials as crd
import mysql.connector as conn
from datetime import *
import streamlit as st
from User import User
from Fetch_Today_Health_Data import fetch_today_data

table_name="user"
# def add_health_data():
def run():    
    st.title("Log Your Daily Health Data")
    if "User" not in st.session_state:
        st.error("You must log in first!")
        return
    
    if "User" not in st.session_state:
        st.error("You must log in first!")
        return

    user:User=st.session_state["User"]
    user_id = user.uid
    today = date.today()

    data=fetch_today_data(user_id)
    if st.session_state['today']==True:
        st.info('You\'ve already logged today\'s data')
        return
    
    with st.form("health_data_form"):
        st.subheader("Enter today's health data")
        bp_systolic = st.text_input("Blood Pressure Systolic",value='')
        bp_diastolic = st.text_input("Blood Pressure Dystolic",value='')
        heartbeat = st.number_input("Heartbeat (bpm)", min_value=30, max_value=200, step=1)
        sugar = st.number_input("Blood Sugar Level (mg/dL)", min_value=50, max_value=400, step=1)
        oxygen = st.number_input("Oxygen Level (Oxygen Saturation(%))", min_value=70, max_value=100, step=1)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, step=0.1)
        # Temperature input in Fahrenheit
        temperature_f = st.number_input("Enter Temperature (°F)", min_value=86.0, max_value=113.0, step=0.1, key="temp_fahrenheit")

        # Convert Fahrenheit to Celsius
        temperature = (temperature_f - 32) * 5.0 / 9.0 if temperature_f else None

        bmi = float(weight) / (float(user.get_height()) ** 2)

        submitted = st.form_submit_button("Submit")
        if submitted:
            if not bp_systolic or not bp_diastolic or not heartbeat or not sugar or not oxygen or not weight or not temperature:
                st.warning("Please fill out the required fields")            
            else:
                save_health_data(user_id, today, int(bp_systolic), int(bp_diastolic), heartbeat, sugar, oxygen, weight, temperature, bmi)
                st.success("Health data added successfully!")

def save_health_data(user_id, record_date, bp1, bp2, heartbeat, sugar, oxygen, weight, temperature, bmi):
    try:
        db = conn.connect(host=crd.host, user=crd.user, password=crd.pwd, database=crd.database)
        cur = db.cursor()

        query = """
            INSERT INTO health_data (uid, record_date, bp_systolic, bp_diastolic, heartbeat, sugar, oxygen, weight, temperature, bmi)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (user_id, record_date, bp1 ,bp2, heartbeat, sugar, oxygen, weight, temperature, bmi))
        
        db.commit()
        db.close()
    
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")