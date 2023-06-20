import re

email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
def validate_email_regex(email):
    return re.match(email_pattern, email) is not None
