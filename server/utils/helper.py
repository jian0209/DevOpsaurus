import json
import random
import string
import hashlib
from conf.config import Config as c


def generate_random_string(length: int = 20) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def encrypt_password(password: str) -> str:
    return hashlib.md5(c.ENCRYPT_KEY.encode() + password.encode()).hexdigest()


def format_json_from_redis(data: str) -> dict:
    data = data.decode('utf-8')
    data = data.replace('\\"', '"')
    return json.loads(data)
