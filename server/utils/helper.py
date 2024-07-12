import json
import random
import string
import hashlib
from conf.config import Config as c
import base64
import io
import pyotp
import qrcode
import pymysql
from log import logger as l
import redis


def generate_random_string(length: int = 20) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def encrypt_password(password: str) -> str:
    return hashlib.md5(c.ENCRYPT_KEY.encode() + password.encode()).hexdigest()


def format_json_from_redis(data: str) -> dict:
    if not data:
        return None
    data = data.decode('utf-8')
    data = data.replace('\\"', '"')
    return json.loads(data)


def generate_qr_code(username: str) -> tuple[str, str]:
    secret_key = pyotp.random_base32()

    totp = pyotp.totp.TOTP(secret_key).provisioning_uri(
        name=username, issuer_name="devopsaurus")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(totp)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return secret_key, img_base64


def verify_otp(secret_key: str, otp: str) -> bool:
    totp = pyotp.TOTP(secret_key)
    return totp.verify(otp)


def connect_to_database(host: str, username: str, password: str, port: int = 3306):
    try:
        conn = pymysql.connect(host=host, user=username,
                               password=password, port=port)
        return conn
    except pymysql.MySQLError as e:
        l.error(f"Database connection error: {str(e)}")
        return None


def connect_to_redis(host: str, port: int, password: str, db: int = 0):
    try:
        conn = redis.Redis(host=host, port=port, password=password, db=db)
        return conn
    except redis.RedisError as e:
        l.error(f"Redis connection error: {str(e)}")
        return None
