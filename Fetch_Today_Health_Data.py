import mysql.connector as conn
import DB_Creadentials as crd
import streamlit as st
from datetime import date

def fetch_today_data(user_id):
    try:
        db = conn.connect(host=crd.host, user=crd.user, password=crd.pwd, database=crd.database)
        cur = db.cursor()

        today = date.today()
        query = "SELECT * FROM health_data WHERE uid = %s AND record_date = %s"
        cur.execute(query, (user_id, today))
        data = cur.fetchone()
        if(data):
            st.session_state["today"]=True
        else:
            st.session_state["today"]=False
        db.close()
        return data
    
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None
