import streamlit as st
import time

def run():
    goal_units = {
    "Weight": "kg",
    "Steps": "steps/day",
    "Sleep": "hours/night",
    "Blood Pressure": "mmHg",
    "Sugar": "mg/dL",
    "Heart Rate": "bpm",
    "Water Intake": "liters/day",
    "Meditation": "minutes/day",
    "Exercise/Yoga": "minutes/day",
    "Strength Training": "minutes/day",
    "Custom Activities": "minutes/day"
    }
        
    # goal_type = st.selectbox("Select Goal Type", [
    #     "Steps per Day", "Exercise/Yoga", "Strength Training", "Water Drinking", 
    #     "Sugar Limit", "Sleep Duration", "Body Weight", "Blood Pressure", 
    #     "Blood Sugar", "Heart Rate", "Meditation", "Custom Activities"
    # ])
    goal_type = st.selectbox("Select Goal Type", list(goal_units.keys()))
    unit = goal_units.get(goal_type, "")

    # # Display the input box with the corresponding unit
    # target_value = st.number_input(f"Enter your target {goal_type} ({unit})", min_value=0.0)
    # deadline = st.date_input("Set Deadline")

    if goal_type != "Custom Activities":
        target_value = st.number_input(f"Enter your target for {goal_type}", min_value=0.0)
        deadline = st.date_input("Set Deadline")
        # completed = st.checkbox("Mark as Completed")

        if st.button("Save Goal"):
            st.success(f"Goal set: {goal_type} → {target_value} {unit} by {deadline}")
            # if completed:
            #     st.balloons()
            #     st.success(f"🎉 Goal for {goal_type} marked as completed!")
    else:
        custom_activities()

def custom_activities():
    if "custom_activities" not in st.session_state:
        st.session_state.custom_activities = []

    st.subheader("➕ Add New Custom Activity")
    activity_name = st.text_input("Enter the activity name:")
    goal_value = st.number_input("Set goal (e.g., minutes/day):", min_value=1, value=30)

    if st.button("Add Activity"):
        if activity_name:
            new_activity = {"name": activity_name, "goal": goal_value, "completed": False}
            st.session_state.custom_activities.append(new_activity)
            message = st.empty()
            time.sleep(0.5)
            message.success(f"✅ Added '{activity_name}' with a goal of {goal_value} minutes/day!")
            time.sleep(2)
            message.empty()
        else:
            st.error("Please enter a valid activity name.")

    if st.session_state.custom_activities:
        st.subheader("📋 Your Custom Activities")
        for idx, activity in enumerate(st.session_state.custom_activities):
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"➡️ **{activity['name']}** - Goal: {activity['goal']} min/day")
            if col2.checkbox("Completed", value=activity["completed"], key=f"completed_{idx}"):
                st.session_state.custom_activities[idx]['completed'] = True
            if col3.button("❌ Remove", key=f"remove_{idx}"):
                st.session_state.custom_activities.pop(idx)
                st.rerun()

    if st.button("💾 Save All Activities"):
        st.success("All activities saved successfully!")
