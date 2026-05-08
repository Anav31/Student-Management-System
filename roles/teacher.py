import streamlit as st
import pandas as pd
from datetime import datetime, date
from db import get_connection
from utils import *

def teacher_dashboard():

    con = get_connection()
    cur = con.cursor()

    menu = st.sidebar.radio(
        "Teacher Menu",
        ["Add Student", "Show Students", "Search Student"]
    )

    # ---------------- ADD ----------------
    if menu == "Add Student":

        st.header("➕ Add Student")

        with st.form("add"):

            reg = st.text_input("Registration No")
            enrol = st.number_input("Enrollment No", step=1)
            name = st.text_input("Name")
            course = st.text_input("Course")
            dob = st.date_input("DOB", value=date(2000,1,1))
            gender = st.selectbox("Gender", ["Male","Female","Other"])
            contact = st.text_input("Contact")
            address = st.text_area("Address")
            email = st.text_input("Email")

            submit = st.form_submit_button("Add")

            if submit:

                if enrollment_exists(cur, enrol):
                    st.error("Enrollment exists")
                elif not validate_mobile(contact):
                    st.error("Invalid mobile")
                elif not validate_email(email):
                    st.error("Invalid email")
                else:
                    cur.execute("""
                        INSERT INTO student VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        reg, enrol, name, course,
                        str(dob), gender, contact,
                        address, email,
                        str(datetime.now().date()),
                        str(datetime.now().time())
                    ))

                    con.commit()
                    st.success("Added successfully")

    # ---------------- SHOW ----------------
    elif menu == "Show Students":

        cur.execute("SELECT * FROM student")
        data = cur.fetchall()

        st.dataframe(pd.DataFrame(data))

    # ---------------- SEARCH ----------------
    elif menu == "Search Student":

        key = st.text_input("Search")

        if st.button("Search"):

            cur.execute("""
                SELECT * FROM student
                WHERE student_name LIKE ?
                OR courses LIKE ?
                OR enrollment_no LIKE ?
            """, (f"%{key}%", f"%{key}%", f"%{key}%"))

            st.dataframe(pd.DataFrame(cur.fetchall()))

    cur.close()
    con.close()