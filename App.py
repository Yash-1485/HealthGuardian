import DB_Creadentials as crd
import DB_Creation as dbc
import Signup
import Login
import Home
import streamlit as st
from streamlit_option_menu import option_menu as om


st.set_page_config(
    page_title="HealthGuardian",
    page_icon="🏥"
)

# Initializing session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def run():
    # Sidebar Navigation
    with st.sidebar:
        page = om(
            menu_title="Navigation",
            options=["Home", "Login", "Signup"],
            icons=["house-fill", "person-fill", "pencil-square"],
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#b3e5fc"},
                "icon": {"color": "black", "font-size": "25px"}, 
                "nav-link": {"color": "#000", "font-size": "18px", "text-align": "left"},
                "nav-link-selected": {"background-color": "#6bbf8a"},
            },
        )

    # Page Content
    if page == "Home":
        if st.session_state["logged_in"]:
            Home.run()
            pass
        else:
            st.warning("You haven't logged in yet. Please log in first!")
    elif page == "Login":
        Login.run()
        pass
    elif page == "Signup":
        Signup.run()

if __name__ == "__main__":
    dbc.db_creation()
    run()