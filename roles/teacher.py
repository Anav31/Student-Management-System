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

    # ---------------- ADD STUDENT ----------------
    if menu == "Add Student":

        st.header("➕ Add Student")

        with st.form("add"):

            reg = st.text_input("Registration No")
            enrol = st.number_input("Enrollment No", step=1)
            name = st.text_input("Name")
            course = st.text_input("Course")
            dob = st.date_input("DOB", value=date(2000, 1, 1))
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
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
                    try:
                        cur.execute("""
                            INSERT INTO student (
                                registration_no,
                                enrollment_no,
                                student_name,
                                courses,
                                dob,
                                gender,
                                contact_no,
                                postal_address,
                                email_id,
                                date_of_admission,
                                time_of_admission
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            reg,
                            enrol,
                            name,
                            course,
                            dob.strftime("%Y-%m-%d"),   # ✔ clean DOB
                            gender,
                            contact,
                            address,
                            email,
                            datetime.now().strftime("%Y-%m-%d"),     # ✔ correct date
                            datetime.now().strftime("%H:%M:%S")      # ✔ correct time
                        ))

                        con.commit()
                        st.success("Student added successfully")

                    except Exception as e:
                        st.error(f"DB Error: {e}")

    # ---------------- SHOW STUDENTS ----------------
    elif menu == "Show Students":

        st.header("📋 Students List")

        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()

        if rows:

            # ✔ FIX COLUMN NAMES PROPERLY
            columns = [desc[0] for desc in cur.description]

            df = pd.DataFrame(rows, columns=columns)

            st.dataframe(df, use_container_width=True, hide_index=True)

        else:
            st.warning("No data found")

    # ---------------- SEARCH STUDENT ----------------
    elif menu == "Search Student":

        st.header("🔍 Search Student")

        key = st.text_input("Search")

        if st.button("Search"):

            cur.execute("""
                SELECT * FROM student
                WHERE student_name LIKE ?
                OR courses LIKE ?
                OR enrollment_no LIKE ?
            """, (f"%{key}%", f"%{key}%", f"%{key}%"))

            rows = cur.fetchall()

            if rows:

                # ✔ FIX COLUMN NAMES HERE TOO
                columns = [desc[0] for desc in cur.description]

                df = pd.DataFrame(rows, columns=columns)

                st.dataframe(df, use_container_width=True, hide_index=True)

            else:
                st.warning("No results found")

    cur.close()
    con.close()