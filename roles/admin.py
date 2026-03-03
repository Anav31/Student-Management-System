import streamlit as st
import pandas as pd
from datetime import date, datetime
from db import get_connection


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
                try:
                    cur.execute("""
                        INSERT INTO student VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        reg, enrol, name, course, dob, gender,
                        contact, address, email,
                        datetime.now().date(),
                        datetime.now().time()
                    ))
                    con.commit()
                    st.success("✅ Student added successfully")
                except Exception as e:
                    st.error(e)

    # ---------------- SHOW STUDENTS ----------------
    elif menu == "Show Students":
        st.header("📋 All Students")
        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()
        st.dataframe(pd.DataFrame(rows))

    # ---------------- SEARCH STUDENT ----------------
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

        enrol = st.number_input("Enrollment No", step=1)

        if st.button("Fetch"):
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

        # SHOW FORM ONLY IF DATA EXISTS
        if st.session_state.get("show_form", False):

            student = st.session_state.student

            # SAFE COURSE INDEX
            db_course = student["courses"]

            if db_course in course_list:
                course_index = course_list.index(db_course)
            else:
                course_index = 0   # fallback safe option

            with st.form("update_form"):

                name = st.text_input("Name", student["student_name"])

                course = st.selectbox(
                    "Course",
                    course_list,
                    index=course_index
                )

                contact = st.text_input("Contact", student["contact_no"])
                address = st.text_area("Address", student["postal_address"])
                email = st.text_input("Email", student["email_id"])

                submitted = st.form_submit_button("Update")

                if submitted:
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


    # ---------------- DELETE STUDENT ----------------
    elif menu == "Delete Student":
        st.header("🗑️ Delete Student")

        enrol = st.number_input("Enrollment No", step=1)

        if st.button("Delete"):
            cur.execute("DELETE FROM student WHERE enrollment_no=%s", (enrol,))
            con.commit()
            st.success("✅ Deleted successfully")

    con.close()
