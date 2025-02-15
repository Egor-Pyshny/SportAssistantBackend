import hashlib
import os
from uuid import uuid4


def generate_sid() -> str:
    random_part = uuid4()
    data = f"{os.getenv('SECRET_KEY')}{random_part}"
    binary_hash = hashlib.sha256(data.encode("utf-8")).digest()
    hex_hash = binary_hash.hex()
    return hex_hash
