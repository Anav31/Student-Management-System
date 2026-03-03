import streamlit as st
import pandas as pd
from datetime import datetime
from db import get_connection

def teacher_dashboard():
    con = get_connection()
    cur = con.cursor()

    menu = st.sidebar.radio(
        "Teacher Menu",
        ["Add Student","Show Students", "Search Student"]
    )
    import datetime

    if menu == "Add Student":
        st.header("➕ Add Student")

        with st.form("add_form"):
            reg = st.text_input("Registration No")
            enrol = st.number_input("Enrollment No", step=1)
            name = st.text_input("Student Name")
            course = st.text_input("Courses")

            # ✅ FIXED DOB INPUT (1960 onwards)
            dob = st.date_input(
                "DOB",
                value=datetime.date(2000, 1, 1),
                min_value=datetime.date(1960, 1, 1),
                max_value=datetime.date.today()
            )

            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            contact = st.text_input("Contact")
            address = st.text_area("Address")
            email = st.text_input("Email")

            if st.form_submit_button("Add"):
                try:
                    cur.execute("""
                        INSERT INTO student VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        reg, enrol, name, course, dob, gender,
                        contact, address, email,
                        datetime.now().date(),
                        datetime.now().time()
                    ))
                    st.success("Student added successfully")
                except Exception as e:
                    st.error(e)

                    
    if menu == "Show Students":
        st.header("📋 All Students")
        cur.execute("SELECT * FROM student")
        st.dataframe(pd.DataFrame(cur.fetchall()))

    elif menu == "Search Student":
        st.header("🔍 Search Student")
        key = st.text_input("Name / Course / Enrollment")

        if st.button("Search"):
            cur.execute("""
                SELECT * FROM student
                WHERE student_name LIKE %s
                OR courses LIKE %s
                OR enrollment_no LIKE %s
            """, (f"%{key}%", f"%{key}%", f"%{key}%"))
            st.dataframe(pd.DataFrame(cur.fetchall()))

    con.close()
