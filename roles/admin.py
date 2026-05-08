import streamlit as st
import pandas as pd
from datetime import date, datetime
from db import get_connection
import re


# ---------------- VALIDATION FUNCTIONS ----------------

def validate_mobile(contact):
    return contact.isdigit() and len(contact) == 10


def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


# ---------------- MAIN DASHBOARD ----------------

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

            reg = st.text_input("Registration No").strip()

            enrol = st.number_input("Enrollment No", min_value=1, step=1)

            name = st.text_input("Student Name").strip()

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

            address = st.text_area("Address").strip()

            email = st.text_input("Email").strip()

            submitted = st.form_submit_button("Add Student")

            if submitted:

                if not reg or not name or not contact or not address or not email:
                    st.error("⚠️ Please fill all required fields")

                elif not validate_mobile(contact):
                    st.error("❌ Mobile number must be exactly 10 digits")

                elif not validate_email(email):
                    st.error("❌ Invalid email address")

                else:
                    try:

                        cur.execute(
                            "SELECT * FROM student WHERE enrollment_no=%s",
                            (enrol,)
                        )

                        if cur.fetchone():
                            st.error(f"❌ Student with Enrollment No {enrol} already exists")

                        else:
                            cur.execute("""
                                INSERT INTO student VALUES
                                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """, (
                                reg,
                                enrol,
                                name,
                                course,
                                dob,
                                gender,
                                contact,
                                address,
                                email,
                                datetime.now().date(),
                                datetime.now().time()
                            ))

                            con.commit()
                            st.success("✅ Student added successfully")

                    except Exception as e:
                        st.error(f"Database Error: {e}")

    # ---------------- SHOW STUDENTS ----------------
    elif menu == "Show Students":

        st.header("📋 All Students")

        try:
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()

            if rows:
                st.dataframe(pd.DataFrame(rows), use_container_width=True)
            else:
                st.warning("⚠️ No student records found")

        except Exception as e:
            st.error(f"Error: {e}")

    # ---------------- SEARCH STUDENT ----------------
    elif menu == "Search Student":

        st.header("🔍 Search Student")

        key = st.text_input("Name / Course / Enrollment").strip()

        if st.button("Search"):

            if not key:
                st.warning("⚠️ Enter search value")

            else:
                try:
                    cur.execute("""
                        SELECT * FROM student
                        WHERE student_name LIKE %s
                        OR courses LIKE %s
                        OR CAST(enrollment_no AS CHAR) LIKE %s
                    """, (f"%{key}%", f"%{key}%", f"%{key}%"))

                    rows = cur.fetchall()

                    if rows:
                        st.dataframe(pd.DataFrame(rows))
                    else:
                        st.warning("⚠️ No student found")

                except Exception as e:
                    st.error(f"Search Error: {e}")

    # ---------------- UPDATE STUDENT ----------------
    elif menu == "Update Student":

        st.header("✏️ Update Student")

        course_list = [
            "PDDM + AI",
            "PDEAB + AI",
            "PDGD + AI",
            "ADCA + AI",
            "ADFA + AI",
            "ADOA + AI"
        ]

        enrol = st.number_input("Enrollment No", min_value=1, step=1)

        if st.button("Fetch"):

            try:
                cur.execute(
                    "SELECT * FROM student WHERE enrollment_no=%s",
                    (enrol,)
                )

                student = cur.fetchone()

                if not student:
                    st.error("❌ Student not found")
                    st.session_state.show_form = False
                else:
                    st.session_state.student = student
                    st.session_state.show_form = True

            except Exception as e:
                st.error(f"Fetch Error: {e}")

        if st.session_state.get("show_form", False):

            student = st.session_state.student

            db_course = student["courses"]

            course_index = course_list.index(db_course) if db_course in course_list else 0

            with st.form("update_form"):

                name = st.text_input("Name", student["student_name"]).strip()

                course = st.selectbox("Course", course_list, index=course_index)

                contact = st.text_input("Contact", student["contact_no"])

                address = st.text_area("Address", student["postal_address"]).strip()

                email = st.text_input("Email", student["email_id"]).strip()

                submitted = st.form_submit_button("Update")

                if submitted:

                    if not name or not contact or not address or not email:
                        st.error("⚠️ All fields required")

                    elif not validate_mobile(contact):
                        st.error("❌ Mobile must be 10 digits")

                    elif not validate_email(email):
                        st.error("❌ Invalid email")

                    else:
                        try:
                            cur.execute("""
                                UPDATE student SET
                                student_name=%s,
                                courses=%s,
                                contact_no=%s,
                                postal_address=%s,
                                email_id=%s
                                WHERE enrollment_no=%s
                            """, (name, course, contact, address, email, enrol))

                            con.commit()

                            st.success("✅ Updated successfully")
                            st.session_state.show_form = False

                        except Exception as e:
                            st.error(f"Update Error: {e}")

    # ---------------- DELETE STUDENT ----------------
    elif menu == "Delete Student":

        st.header("🗑️ Delete Student")

        enrol = st.number_input("Enrollment No", min_value=1, step=1)

        if st.button("Delete"):

            try:
                cur.execute(
                    "SELECT * FROM student WHERE enrollment_no=%s",
                    (enrol,)
                )

                if not cur.fetchone():
                    st.error("❌ Student does not exist")

                else:
                    cur.execute(
                        "DELETE FROM student WHERE enrollment_no=%s",
                        (enrol,)
                    )

                    con.commit()
                    st.success("✅ Deleted successfully")

            except Exception as e:
                st.error(f"Delete Error: {e}")

    cur.close()
    con.close()