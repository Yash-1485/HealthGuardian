import DB_Creadentials as crd
import mysql.connector as conn
import datetime as dt
import streamlit as st
from User import User

table_name="user"
def run():
    st.title("Signup Page")
    
    # , clear_on_submit=True
    with st.form("signup_form"):
        st.subheader("Create an Account to HealthGuardian")
        
        em = st.text_input("Email", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", placeholder="Enter a strong password")
        name = st.text_input("Name", placeholder="Enter your name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        gen = st.selectbox("Gender", ["Male", "Female", "Other"])
        height = st.text_input("Height", placeholder="Enter your height(in meters)")
        birthdate = st.date_input("Enter your birthdate",min_value=dt.date(1900,1,1),max_value=dt.date(2025,1,1))
        blood_gp = st.selectbox("Blood Group", ['A+','A-','B+','B+','O+','O-','AB+','AB-'])
        
        # Submit button
        submitted = st.form_submit_button("Sign Up")        
        
        if submitted:
            if not em or not password or not name or not age or not gen or not height:
                st.error("Please fill in all required fields.")
            else:
                
                new_user=User(name,age,gen,birthdate,blood_gp,height,em,password)
                
                insert_data(new_user)                                
                st.write("Welcome, ", name)
    clear=st.button("Clear Form")
    if(clear):
        pass
def insert_data(user:User):
    try:
        db=conn.connect(host=crd.host,user=crd.user,password=crd.pwd,database=crd.database)
        cur=db.cursor()
        query="INSERT INTO HealthGuardian.USER VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(query,(user.get_uid(),user.get_name(),user.get_age(),user.get_gender(),user.get_birthdate(),user.get_blood_group(),user.get_height(),user.get_email(),user.pwd))
        db.commit()        
        if(cur.rowcount>0):
            st.success("New User added & Account created successfully!")
            st.info("Now to use app, you should login through app first")
        db.close()
    except Exception as e:
        st.info("Something went wrong!!!")