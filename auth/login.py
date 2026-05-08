import streamlit as st
from db import get_connection


def login_page():

    # ---------------- PAGE CONFIG ----------------
    st.set_page_config(page_title="Login", layout="centered")

    # ---------------- CUSTOM CSS ----------------
    st.markdown("""
        <style>

        /* Background */
        body {
            background: linear-gradient(135deg, #0f172a, #1e293b);
        }

        /* Center card */
        .login-container {
            background-color: #111827;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0px 10px 40px rgba(0,0,0,0.4);
            width: 420px;
            margin: auto;
        }

        /* Center alignment */
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }

        /* Title styling */
        .title {
            color: white;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 20px;
        }

        /* Input styling */
        input {
            border-radius: 8px !important;
        }

        </style>
    """, unsafe_allow_html=True)

    # ---------------- CENTER LAYOUT ----------------
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown("<div class='login-container'>", unsafe_allow_html=True)

        # ---------------- LOGO ----------------
        st.markdown("<div class='center'>", unsafe_allow_html=True)

        # 👉 Replace with your client logo path
        st.image("logo.png", width=100)

        st.markdown("<div class='title'>🔐 Login</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- INPUTS ----------------
        username = st.text_input("Username", placeholder="Enter username")

        password = st.text_input("Password", type="password", placeholder="Enter password")

        # ---------------- LOGIN BUTTON ----------------
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

                st.success("Login successful ✅")
                st.rerun()

            else:
                st.error("Invalid credentials ❌")

        st.markdown("</div>", unsafe_allow_html=True)