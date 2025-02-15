from enum import Enum


class TTL(Enum):
    session_ttl = 24 * 60 * 60
    email_code_ttl = 10 * 60
    reset_password_code_ttl = 10 * 60
