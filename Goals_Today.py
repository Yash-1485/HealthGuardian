import streamlit as st
import json
from datetime import date
import mysql.connector as conn
import DB_Creadentials as crd
from User import User

def fetch_todays_goals(uid):
    try:
        db = conn.connect(
            host=crd.host, user=crd.user, password=crd.pwd, database=crd.database
        )
        cur = db.cursor()
        query = "SELECT goals FROM goals WHERE uid=%s AND date=%s"
        cur.execute(query, (uid, date.today()))
        result = cur.fetchone()
        db.close()
        return result
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None

def mark_goal_completed(uid):
    try:
        db = conn.connect(
            host=crd.host, user=crd.user, password=crd.pwd, database=crd.database
        )
        cur = db.cursor()
        query = "UPDATE goals SET completed=%s WHERE uid=%s AND date=%s"
        cur.execute(query, (True, uid, date.today()))
        db.commit()
        db.close()
        st.success("🎉 All goals for today marked as completed!")
    except Exception as e:
        st.error(f"Error updating completion status: {str(e)}")

def run():
    user:User=st.session_state['User']
    uid=user.uid
    data = fetch_todays_goals(uid)

    if data:
        goals = json.loads(data[0])
        st.subheader("📅 Today's Goals")
        
        # Display predefined goals
        for goal, value in goals.items():
            ck=st.checkbox(f"{goal}: {value[0]}", key=goal)

        # Display custom activities
        if st.button("✅ Mark All as Completed"):
            mark_goal_completed(uid)
    else:
        st.info("No goals set for today.")
