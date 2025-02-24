import streamlit as st
import json
from datetime import date
import mysql.connector as conn
import DB_Creadentials as crd
from User import User

def fetch_todays_goals(uid):#For Uncompleted
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

def show_uncompleted_goals(goals):
    res={}
    for key,goal in goals.items():
        if(not goal[1]):
            res[key]=goal
    return res

def show_completed_goals(goals):
    res={}
    for key,goal in goals.items():
            if(goal[1]):
                res[key]=goal
    return res

def mark_update_all_goals_completed(uid):
    try:
        db = conn.connect(
            host=crd.host, user=crd.user, password=crd.pwd, database=crd.database
        )
        cur = db.cursor()
        query = "SELECT id,goals FROM goals WHERE uid=%s AND date=%s"
        cur.execute(query, (uid, date.today()))
        data=cur.fetchone()
        id=data[0]
        result = json.loads(data[1])
        for key,goals in result.items():
            goals[1]=True
        up_query="Update goals SET goals=%s where id=%s AND uid=%s AND date=%s"
        cur.execute(up_query,(json.dumps(result),id,uid,date.today()))
        db.commit()
        db.close()
        st.session_state["mark_all"]=True
        st.success('All goals completed')
        st.balloons()
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
    except Exception as e:
        st.error(f"Error updating completion status: {str(e)}")

def mark_goal_uncompleted(uid):
    try:
        db = conn.connect(
            host=crd.host, user=crd.user, password=crd.pwd, database=crd.database
        )
        cur = db.cursor()
        query = "UPDATE goals SET completed=%s WHERE uid=%s AND date=%s"
        cur.execute(query, (False, uid, date.today()))
        db.commit()
        db.close()        
    except Exception as e:
        st.error(f"Error updating completion status: {str(e)}")

def onclick_remove(goals,b):
    if goals:
        st.session_state["mark_all"] = False 
    else:
        st.session_state["mark_all"] = b
    

def run():
    if "mark_all" not in st.session_state:
        st.session_state.mark_all = False
    user:User=st.session_state['User']
    uid=user.uid
    data = fetch_todays_goals(uid)

    if data:
        goals_data = data[0]
        goals = show_uncompleted_goals(json.loads(goals_data))
        c_goals=show_completed_goals(json.loads(goals_data))
        st.subheader("📅 Today's Goals")
        
        # Display predefined goals
        if goals.items():
            for goal, value in goals.items():
                ck=st.checkbox(f"{goal}: {value[0]}", key=goal)
                if ck:
                    complete_Tasks(uid,goal)
                    st.rerun()
            
        st.subheader("📅 Today's Completed Goals")
        for goal, value in c_goals.items():
            st.write(f"{goal}: {value[0]} Status:✅")
            
        onclick_remove(goals.items(),True)
        m_btn=st.button("✅ Mark All as Completed", on_click=onclick_remove,args=(goals.items(),True), disabled=st.session_state['mark_all'])
        if not goals.items() and (not st.session_state.mark_all and not m_btn):
            mark_goal_completed(uid)
            mark_update_all_goals_completed(uid)            
            st.rerun()
        if (not st.session_state.mark_all and m_btn):
            mark_goal_completed(uid)
            mark_update_all_goals_completed(uid)                                    
            st.rerun()
        if(st.session_state['mark_all']==True):
            st.success('All goals completed')
            st.balloons()
        else:
            mark_goal_uncompleted(uid)
    else:
        st.info("No goals set for today.")

def complete_Tasks(uid,goal):
    try:
        db = conn.connect(
            host=crd.host, user=crd.user, password=crd.pwd, database=crd.database
        )
        cur = db.cursor()
        query = "SELECT id,goals FROM goals WHERE uid=%s AND date=%s"
        cur.execute(query, (uid, date.today()))
        data=cur.fetchone()
        print(data)
        id=data[0]
        result = json.loads(data[1])
        result[goal][1]=True
        up_query="Update goals SET goals=%s where id=%s AND uid=%s AND date=%s"
        cur.execute(up_query,(json.dumps(result),id,uid,date.today()))
        db.commit()
        db.close()
        st.success("Goals updated successfully!")
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None