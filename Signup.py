import DB_Creadentials as crd
import mysql.connector as conn
import datetime as dt
import streamlit as st
import re  # For email and password validation
from User import User

table_name = "user"

def is_valid_email(email):
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

def is_valid_password(password):
    """Ensure password has at least 8 characters, including uppercase, lowercase, number, and special character."""
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return re.match(pattern, password)

def email_exists(email):
    """Check if the email is already registered in the database."""
    db = conn.connect(host=crd.host, user=crd.user, password=crd.pwd, database=crd.database)
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM user WHERE email = %s", (email,))
    count = cur.fetchone()[0]
    db.close()
    return count > 0

def run():
    st.title("HealthGuardian")
    st.title("Signup Page")

    with st.form("signup_form"):
        st.subheader("Create an Account to HealthGuardian")

        em = st.text_input("Email", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", placeholder="Enter a strong password")
        name = st.text_input("Name", placeholder="Enter your name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        gen = st.selectbox("Gender", ["Male", "Female", "Other"])
        height = st.text_input("Height", placeholder="Enter your height (in meters)")
        birthdate = st.date_input("Enter your birthdate", min_value=dt.date(1900, 1, 1), max_value=dt.date.today())
        blood_gp = st.selectbox("Blood Group", ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'])

        submitted = st.form_submit_button("Sign Up")        

        if submitted:
            # Validations
            if not em or not password or not name or not age or not gen or not height:
                st.error("Please fill in all required fields.")
                return

            if not is_valid_email(em):
                st.error("Invalid email format. Please enter a valid email address.")
                return

            if email_exists(em):
                st.error("This email is already registered. Please use another email.")
                return

            if not is_valid_password(password):
                st.error("Password must be at least 8 characters long and contain uppercase, lowercase, number, and special character.")
                return

            try:
                height = float(height)
                if height < 0.5 or height > 2.5:
                    st.error("Invalid height. Please enter a value between 0.5m and 2.5m.")
                    return
            except ValueError:
                st.error("Invalid height format. Please enter a numeric value.")
                return

            # Create new user
            new_user = User(name, age, gen, birthdate, blood_gp, height, em, password)
            insert_data(new_user)

def insert_data(user: User):
    try:
        db = conn.connect(host=crd.host, user=crd.user, password=crd.pwd, database=crd.database)
        cur = db.cursor()
        
        query = "INSERT INTO HealthGuardian.USER VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(query, (user.get_uid(), user.get_name(), user.get_age(), user.get_gender(), user.get_birthdate(), user.get_blood_group(), user.get_height(), user.get_email(), user.pwd))
        
        db.commit()
        
        if cur.rowcount > 0:
            st.success("New User added & Account created successfully!")
            st.info("Now to use the app, you should log in first.")
        
        db.close()
    except Exception as e:
        st.error(f"Something went wrong: {e}")