import re

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_gpa(gpa_str):
    try:
        gpa = float(gpa_str)
        if 0.0 <= gpa <= 4.0:
            return True
        return False
    except ValueError:
        return False
