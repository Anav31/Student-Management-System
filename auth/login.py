import streamlit as st
from db import get_connection

def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "SELECT role FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cur.fetchone()
        con.close()

        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = user["role"]
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")
