import streamlit as st
import pandas as pd
from datetime import date, datetime
from db import get_connection
from utils import *

def admin_dashboard():

    con = get_connection()
    cur = con.cursor()

    st.sidebar.title("Admin Panel")

    menu = st.sidebar.radio(
        "Admin Menu",
        ["Add Student", "Show Students", "Search Student", "Update Student", "Delete Student"]
    )

    # ---------------- ADD STUDENT ----------------
    if menu == "Add Student":

        st.header("➕ Add Student")

        with st.form("add_form"):

            reg = st.text_input("Registration No")
            enrol = st.number_input("Enrollment No", step=1)
            name = st.text_input("Student Name")

            course = st.selectbox(
                "Course",
                ["PDDM + AI", "PDEAB + AI", "PDGD + AI", "ADCA + AI", "ADFA + AI", "ADOA + AI"]
            )

            dob = st.date_input(
                "DOB",
                value=date(2000, 1, 1),
                min_value=date(1960, 1, 1),
                max_value=date.today()
            )

            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            contact = st.text_input("Contact")
            address = st.text_area("Address")
            email = st.text_input("Email")

            submitted = st.form_submit_button("Add Student")

            if submitted:

                if not reg or not name or not contact or not address or not email:
                    st.error("⚠️ All fields required")

                elif not validate_enrollment(enrol):
                    st.error("❌ Invalid Enrollment Number")

                elif not validate_mobile(contact):
                    st.error("❌ Mobile must be 10 digits")

                elif not validate_email(email):
                    st.error("❌ Invalid email")

                elif enrollment_exists(cur, enrol):
                    st.error("❌ Enrollment already exists")

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
                            reg, enrol, name, course, str(dob), gender,
                            contact, address, email,
                            str(datetime.now().date()),
                            str(datetime.now().time())
                        ))

                        con.commit()
                        st.success("✅ Student added successfully")

                    except Exception as e:
                        st.error(f"DB Error: {e}")

    # ---------------- SHOW ----------------
    elif menu == "Show Students":
        st.header("📋 Students")

        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()

        if rows:
            st.dataframe(pd.DataFrame(rows))
        else:
            st.warning("No data found")

    # ---------------- SEARCH ----------------
    elif menu == "Search Student":

        st.header("🔍 Search")

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
                st.dataframe(pd.DataFrame(rows))
            else:
                st.warning("No results")

    # ---------------- UPDATE ----------------
    elif menu == "Update Student":

        st.header("✏️ Update")

        enrol = st.number_input("Enrollment No", step=1)

        if st.button("Fetch"):

            cur.execute("SELECT * FROM student WHERE enrollment_no = ?", (enrol,))
            student = cur.fetchone()

            if not student:
                st.error("Student not found")
                st.session_state.show = False
            else:
                st.session_state.student = student
                st.session_state.show = True

        if st.session_state.get("show", False):

            s = st.session_state.student

            with st.form("update"):

                name = st.text_input("Name", s["student_name"])
                course = st.text_input("Course", s["courses"])
                contact = st.text_input("Contact", s["contact_no"])
                address = st.text_area("Address", s["postal_address"])
                email = st.text_input("Email", s["email_id"])

                submit = st.form_submit_button("Update")

                if submit:

                    if not validate_mobile(contact):
                        st.error("Invalid mobile")
                    elif not validate_email(email):
                        st.error("Invalid email")
                    else:
                        cur.execute("""
                            UPDATE student SET
                            student_name=?,
                            courses=?,
                            contact_no=?,
                            postal_address=?,
                            email_id=?
                            WHERE enrollment_no=?
                        """, (name, course, contact, address, email, enrol))

                        con.commit()
                        st.success("Updated successfully")
                        st.session_state.show = False

    # ---------------- DELETE ----------------
    elif menu == "Delete Student":

        st.header("🗑️ Delete")

        enrol = st.number_input("Enrollment No", step=1)

        if st.button("Delete"):

            cur.execute("SELECT 1 FROM student WHERE enrollment_no = ?", (enrol,))

            if not cur.fetchone():
                st.error("Student not found")
            else:
                cur.execute("DELETE FROM student WHERE enrollment_no = ?", (enrol,))
                con.commit()
                st.success("Deleted successfully")

    cur.close()
    con.close()