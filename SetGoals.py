import streamlit as st
import json
from datetime import date
import mysql.connector as conn
import DB_Creadentials as crd
import time
from User import User

def save_goals_to_db(uid, goals):
    try:
        db = conn.connect(
            host=crd.host, user=crd.user, password=crd.pwd, database=crd.database
        )
        cur = db.cursor()
        query = """
        INSERT INTO goals (uid, date, goals, completed)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(query, (uid, date.today(), json.dumps(goals), False))
        db.commit()
        db.close()
        st.success("Goals saved successfully!")
    except Exception as e:
        st.error(f"Database error: {str(e)}")

def update_goals_from_db(uid,goals):
    try:
        db = conn.connect(
            host=crd.host, user=crd.user, password=crd.pwd, database=crd.database
        )
        cur = db.cursor()
        query = "SELECT id,goals FROM goals WHERE uid=%s AND date=%s"
        cur.execute(query, (uid, date.today()))
        data=cur.fetchone()
        id=data[0]
        # result = eval(data[1].replace('true','True').replace('false','False'))
        result = json.loads(data[1])
        for key,value in goals.items():
            result[key]=value
        up_query="Update goals SET goals=%s where id=%s AND uid=%s AND date=%s"
        cur.execute(up_query,(json.dumps(result),id,uid,date.today()))
        db.commit()
        db.close()
        # st.success("Goals updated successfully!")
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None

def check_goals_from_db(uid):
    try:
        db = conn.connect(
            host=crd.host, user=crd.user, password=crd.pwd, database=crd.database
        )
        cur = db.cursor()
        query = """
        SELECT * FROM goals where uid=%s and date=%s
        """
        cur.execute(query,(uid,date.today()))
        data=cur.fetchall()
        db.commit()
        db.close()
        return True if data else False
    except Exception as e:
        st.error(f"Database error: {str(e)}")

def run():
    user:User=st.session_state['User']
    goal_units = {
        "Weight": "kg", "Steps": "steps/day", "Sleep": "hours/night",
        "Blood Pressure": "mmHg", "Sugar": "mg/dL", "Heart Rate": "bpm",
        "Water Intake": "liters/day", "Meditation": "minutes/day",
        "Exercise/Yoga": "minutes/day", "Strength Training": "minutes/day",
        "Custom Activities": "minutes/day"
    }
    
    if 'goals' not in st.session_state:
        st.session_state.goals = {}
    if 'count_goals' not in st.session_state:
        st.session_state.count_goals = 0

    goal_type = st.selectbox("Select Goal Type", list(goal_units.keys()))
    unit = goal_units.get(goal_type, "")

    if goal_type != "Custom Activities":
        target_value = st.number_input(f"Enter your target for {goal_type} ({unit})", min_value=0.0)
        if st.button("Add Goal"):
            st.session_state.goals[goal_type] = [target_value,False]
            message = st.empty()
            time.sleep(0.5)
            message.success(f"✅ Added '{goal_type}' with a goal of {target_value} {unit}")
            time.sleep(1)
            message.empty()
    else:
        st.subheader("➕ Add New Custom Activity")
        activity_name = st.text_input("Enter the activity name:")
        goal_value = st.number_input("Set goal (e.g., minutes/day):", min_value=1, value=30)

        if st.button("Add Custom Activity"):
            if activity_name:
                st.session_state.goals[f'Custom Activities - {activity_name}'] = [goal_value,False]
                message = st.empty()
                time.sleep(0.5)
                message.success(f"✅ Added '{activity_name}' with a goal of {goal_value} minutes/day!")
                time.sleep(1)
                message.empty()
            else:
                st.info('Enter atleast a goal')

    st.subheader("📋 Your Goals")
    for idx, activity in enumerate(st.session_state.goals):
        col1, col2, col3 = st.columns([3, 1, 1])
        if activity.find('Custom Activities')!=-1:
            col1.write(f"➡️ **{activity}** - Goal: {st.session_state.goals[activity][0]} {goal_units.get('Custom Activities', "")}")
        else:
            col1.write(f"➡️ **{activity}** - Goal: {st.session_state.goals[activity][0]} {goal_units.get(activity, "")}")
        if col3.button("❌ Remove", key=f"remove_{activity}"):
            st.session_state.goals.pop(activity)
            st.rerun()

    if st.button("💾 Save All Goals"):
        if (st.session_state.goals):
            if not check_goals_from_db(user.uid):
                save_goals_to_db(uid=user.uid, goals=st.session_state.goals)
                st.session_state.goals = {}
            else:
                print(user.uid,st.session_state.goals)
                update_goals_from_db(uid=user.uid,goals=st.session_state.goals)
                st.session_state.goals = {}
        else:
            st.info('Set atleast a Goal')
        st.success('Goals set successfully')
        time.sleep(2)
        st.rerun()
    
    if check_goals_from_db(user.uid):
        st.session_state.count_goals+=1
        # print(st.session_state.count_goals)
        if st.session_state.count_goals<2:
            st.info('You\'ve already added todays goals, If you want to see than you can go to the \'Goals Today\' tab.')
