from uuid import uuid4


def generate_email_code():
    return str(uuid4())
