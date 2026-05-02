import streamlit as st
from components import tools
from components.pages import show_speaking_page, show_writing_page, show_home_page

st.set_page_config(page_title= "IELTS-Agent",  layout="centered")

# Initialize session state
if "current_user_id" not in st.session_state:
    st.session_state.current_user_id = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in= False
    
if "page" not in st.session_state:
    st.session_state.page = "login"

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

#=================
# Auth UI
#=================

if not st.session_state.logged_in:
    
    st.title("Welcome to IELTS-Agent !")
    
    tab1, tab2= st.tabs(["Loging", "Register"])
   
    # ----------------- Login -----------------
    with tab1:
       with st.form("login_form"):
           username = st.text_input("Username")
           password = st.text_input("Password", type="password")
           login_btn = st.form_submit_button("Login")

           if login_btn:
               user= tools.login_user(username, password)
               if user:
                   st.session_state.logged_in = True
                   st.session_state.current_user_id = user["user_id"]
                   st.session_state.current_user = user["name"] or user["username"]
                   st.session_state.page = "home"
                   st.success("Login successful!")
                   st.rerun()
               else:
                   st.error("Invalid username or password.")

   # ----------------- REGISTER -----------------
       with tab2:
           with st.form("register_form"):
                name= st.text_input("What's your name?")
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                register_btn = st.form_submit_button("Register")
                
                if register_btn:

                    if not new_username or not new_password:
                        st.error("Please fill all fields")
    
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
    
                    else:
                        # save user
                        tools.register_user(new_username, new_password,name)
                        st.success("Registration successful! Please login.")
                
# --------------------------------------------------
# MAIN APP
# --------------------------------------------------

else:
    # -------------------------
    # Sidebar Menu
    # -------------------------
    with st.sidebar:
        if st.button("Home", use_container_width=True):
            st.session_state.page = "home"
        if st.button("Writing", use_container_width=True):
            st.session_state.page = "writing"
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            
            st.rerun()

    
    # --------------------------------------------------
    # Rendering page
    # --------------------------------------------------
    page = st.session_state.get("page", "home") 
    
    if page == "home":
        show_home_page()
    
    elif page == "speaking":
        show_speaking_page()
    
    elif page == "writing":
        show_writing_page()
