import streamlit as st
from db import init_db
from auth.login import login_page
from roles.admin import admin_dashboard
from roles.teacher import teacher_dashboard

st.set_page_config("Student Management System", layout="wide")

# ---------- INIT DB ----------
init_db()

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None

# ---------- LOGIN ----------
if not st.session_state.logged_in:
    login_page()
    st.stop()

# ---------- SIDEBAR ----------
st.sidebar.success(f"👋 {st.session_state.username}")
st.sidebar.info(f"Role: {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

# ---------- ROLE ROUTING ----------
if st.session_state.role == "Admin":
    admin_dashboard()
else:
    teacher_dashboard()
