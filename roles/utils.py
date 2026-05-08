import re

def validate_mobile(number):
    return number.isdigit() and len(number) == 10


def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


def validate_enrollment(enrol):
    return isinstance(enrol, int) and enrol > 0


def enrollment_exists(cur, enrol):
    cur.execute("SELECT 1 FROM student WHERE enrollment_no = ?", (enrol,))
    return cur.fetchone() is not None