import streamlit as st
import json
from datetime import date
import mysql.connector as conn
import DB_Creadentials as crd
import time
def save_goals_to_db(uid, goals, custom_activities):
    try:
        db = conn.connect(
            host=crd.host, user=crd.user, password=crd.pwd, database=crd.database
        )
        cur = db.cursor()
        query = """
        INSERT INTO goals (uid, date, goals, custom_activities, completed)
        VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(query, (uid, date.today(), json.dumps(goals), json.dumps(custom_activities), False))
        db.commit()
        db.close()
        st.success("Goals saved successfully!")
    except Exception as e:
        st.error(f"Database error: {str(e)}")

def run():
    goal_units = {
        "Weight": "kg", "Steps": "steps/day", "Sleep": "hours/night",
        "Blood Pressure": "mmHg", "Sugar": "mg/dL", "Heart Rate": "bpm",
        "Water Intake": "liters/day", "Meditation": "minutes/day",
        "Exercise/Yoga": "minutes/day", "Strength Training": "minutes/day",
        "Custom Activities": "minutes/day"
    }
    
    if "custom_activities" not in st.session_state or 'goals' not in st.session_state:
        st.session_state.goals = {}
        st.session_state.custom_activities = {}

    goal_type = st.selectbox("Select Goal Type", list(goal_units.keys()))
    unit = goal_units.get(goal_type, "")

    if goal_type != "Custom Activities":
        target_value = st.number_input(f"Enter your target for {goal_type} ({unit})", min_value=0.0)
        if st.button("Add Goal"):
            st.session_state.goals[goal_type] = target_value
            message = st.empty()
            time.sleep(0.5)
            message.success(f"✅ Added '{goal_type}' with a goal of {target_value} {unit}")
            time.sleep(2)
            message.empty()
    else:
        st.subheader("➕ Add New Custom Activity")
        activity_name = st.text_input("Enter the activity name:")
        goal_value = st.number_input("Set goal (e.g., minutes/day):", min_value=1, value=30)

        if st.button("Add Custom Activity") :
            if activity_name:
                st.session_state.custom_activities[activity_name] = goal_value
                message = st.empty()
                time.sleep(0.5)
                message.success(f"✅ Added '{activity_name}' with a goal of {goal_value} minutes/day!")
                time.sleep(2)
                message.empty()
        else:
            st.info('Enter atleast a goal')

    st.subheader("📋 Your Goals")
    for idx, activity in enumerate(st.session_state.goals):
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(f"➡️ **{activity}** - Goal: {st.session_state.goals[activity]} {goal_units.get(activity, "")}")
        if col3.button("❌ Remove", key=f"remove_{idx}"):
            st.session_state.goals.pop(idx)
            st.rerun()
            
    st.subheader("📋 Your Custom Goals")
    for idx, activity in enumerate(st.session_state.custom_activities):
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(f"➡️ **{activity}** - Goal: {st.session_state.custom_activities[activity]} min/day")
        if col3.button("❌ Remove", key=f"remove_c_{idx}"):
            st.session_state.custom_activities.pop(idx)
            st.rerun()

    if st.button("💾 Save All Goals") and (st.session_state.goals or st.session_state.custom_activities):
        save_goals_to_db(uid=1, goals=st.session_state.goals, custom_activities=st.session_state.custom_activities)
