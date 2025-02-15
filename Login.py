import streamlit as st
import mysql.connector as conn
import DB_Creadentials as crd
from User import User

count=0
def run():
    st.title("Login Page")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Login"):
        db=conn.connect(host=crd.host,user=crd.user,password=crd.pwd,database=crd.database)
        cur=db.cursor()
        query="Select email,password from user"
        cur.execute(query)
        data=cur.fetchall()
        
        flag=False
        for em,pwd in data:
            if((em == email) and (pwd == password)):
                flag=True
                break
        
        if(flag):
            st.session_state["logged_in"] = True
            st.success("LoggedIn Successfully")
            st.session_state["User"] = fetch_user(email,password)
        else:
            global count
            count+=1
            print(count)
            st.error("Invalid email or password. Please try again.")
            
            if(count>2):
                st.info("If you haven't signed up, Sign Up First")
            
            # st.warning("Invalid email or password! Please Enter correct email or password")
        # print(data)

def fetch_user(email,pwd):
    db=conn.connect(host=crd.host,user=crd.user,password=crd.pwd,database=crd.database)
    cursor=db.cursor()
    query="SELECT * FROM USER WHERE email=%s AND password=%s"
    cursor.execute(query,(email,pwd))
    data=cursor.fetchone()
    user=User(data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8])
    user.uid=data[0]
    print(data[0])
    return user