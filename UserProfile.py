import streamlit as st
import mysql.connector as conn
import DB_Creadentials as crd
from User import User
import time

# Function to update user details in the database
def update_user_data(uid, field, new_value):
    try:
        with conn.connect(host=crd.host, user=crd.user, password=crd.pwd, database=crd.database) as db:
            cursor = db.cursor()

            query = f"UPDATE user SET {field} = %s WHERE uid = %s"
            cursor.execute(query, (new_value, uid))
            db.commit()
        
        st.success(f"✅ {field.replace('_', ' ').capitalize()} updated successfully!")
        time.sleep(2)
        st.rerun()  # Refresh page to reflect changes

    except Exception as e:
        st.error(f"❌ Error updating {field}: {e}")

# Function to fetch user details from the database
def get_user_profile(uid):
    try:
        with conn.connect(host=crd.host, user=crd.user, password=crd.pwd, database=crd.database) as db:
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM user WHERE uid = %s"
            cursor.execute(query, (uid,))
            return cursor.fetchone()

    except Exception as e:
        st.error(f"❌ Error fetching user profile: {e}")
        return None

# User Profile Page
def run():
    st.title("HealthGuardian")
    if "User" not in st.session_state:
        st.error("⚠️ User session not found. Please log in.")
        return

    user = st.session_state["User"]
    user_data = get_user_profile(user.uid)

    if not user_data:
        st.error("⚠️ Unable to fetch user profile.")
        return

    st.markdown("<h2 style='text-align: center; color: #00879E;'>👤 User Profile</h2>", unsafe_allow_html=True)

    # **Display User Information**
    profile_fields = {
        "Name": user_data["name"],
        "Age": user_data["age"],
        "Gender": user_data["gender"],
        "Birthdate": user_data["birthdate"],
        "Blood Group": user_data["blood_group"],
        "Height (m)": user_data["height"],
        "Email": user_data["email"]
    }

    for key, value in profile_fields.items():
        st.markdown(f"**{key}:** {value}")

    st.subheader("📝 Edit Your Profile")

    field_options = {
        "Name": "name",
        "Age": "age",
        "Gender": "gender",
        "Birthdate": "birthdate",
        "Blood Group": "blood_group",
        "Height": "height",
        "Email": "email"
    }

    selected_field = st.selectbox("Select a field to update:", list(field_options.keys()))
    db_field = field_options[selected_field]
    
    current_value = user_data[db_field]
    new_value = st.text_input(f"Enter new value for {selected_field}:", value=str(current_value))

    if st.button("Update"):
        if new_value.strip():
            update_user_data(user.uid, db_field, new_value)
        else:
            st.warning("⚠️ Please enter a valid value.")

if __name__ == "__main__":
    run()
