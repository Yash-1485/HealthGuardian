import streamlit as st
import mysql.connector as conn
import DB_Creadentials as crd
from User import User

def run():
    try:
        st.title("Welcome to the Health Guardian")
        
        flag=False
        user=None
        if("User" in st.session_state):
            user:User=st.session_state["User"]
            flag=True
            # st.write(user.name)
            
        
    except Exception as e:
        print(e)