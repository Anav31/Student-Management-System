import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="anav",      # CHANGE IF NEEDED
        database="SMS_DOTNET",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def init_db():
    con = get_connection()
    cur = con.cursor()

    # ---------------- USERS TABLE ----------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(50) NOT NULL,
            role VARCHAR(20) NOT NULL
        )
    """)

    # ---------------- STUDENT TABLE ----------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student (
            registration_no VARCHAR(50),
            enrollment_no INT PRIMARY KEY,
            student_name VARCHAR(100),
            courses VARCHAR(200),
            dob DATE,
            gender VARCHAR(20),
            contact_no VARCHAR(20),
            postal_address VARCHAR(200),
            email_id VARCHAR(100),
            date_of_admission DATE,
            time_of_admission TIME
        )
    """)

    # ---------------- DEFAULT USERS (UPSERT) ----------------
    default_users = [
        ("admin", "dotnet@2026", "Admin"),
        ("teachers", "dotnet@t2026", "Teachers")
    ]

    for username, password, role in default_users:
        cur.execute("SELECT username FROM users WHERE username=%s", (username,))
        user = cur.fetchone()

        if user:
            # Update existing user
            cur.execute("""
                UPDATE users
                SET password=%s, role=%s
                WHERE username=%s
            """, (password, role, username))
        else:
            # Insert new user
            cur.execute("""
                INSERT INTO users (username, password, role)
                VALUES (%s, %s, %s)
            """, (username, password, role))

    return con, cur

# ---------------- AUTHENTICATION ----------------
def authenticate_user(username, password):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT * FROM users
        WHERE username=%s AND password=%s
    """, (username, password))

    user = cur.fetchone()
    con.close()
    return user
