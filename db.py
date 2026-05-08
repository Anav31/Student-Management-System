import sqlite3

# ---------------- CONNECTION ----------------
def get_connection():
    con = sqlite3.connect("SMS_DOTNET.db", check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


# ---------------- INITIALIZE DATABASE ----------------
def init_db():
    con = get_connection()
    cur = con.cursor()

    # ---------------- USERS TABLE ----------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # ---------------- STUDENT TABLE ----------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student (
            registration_no TEXT,
            enrollment_no INTEGER PRIMARY KEY,
            student_name TEXT,
            courses TEXT,
            dob TEXT,
            gender TEXT,
            contact_no TEXT,
            postal_address TEXT,
            email_id TEXT,
            date_of_admission TEXT,
            time_of_admission TEXT
        )
    """)

    # ---------------- DEFAULT USERS (UPSERT LOGIC) ----------------
    default_users = [
        ("admin", "dotnet@2026", "Admin"),
        ("teachers", "dotnet@t2026", "Teachers")
    ]

    for username, password, role in default_users:
        cur.execute("SELECT username FROM users WHERE username = ?", (username,))
        user = cur.fetchone()

        if user:
            cur.execute("""
                UPDATE users
                SET password = ?, role = ?
                WHERE username = ?
            """, (password, role, username))
        else:
            cur.execute("""
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
            """, (username, password, role))

    con.commit()
    return con, cur


# ---------------- AUTHENTICATION ----------------
def authenticate_user(username, password):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT * FROM users
        WHERE username = ? AND password = ?
    """, (username, password))

    user = cur.fetchone()
    con.close()

    return user