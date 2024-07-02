from datetime import timedelta
import json
import time
from flask import Blueprint, request
from const import response
from log import logger as l
from model.user_model import User
from model.redis_init import redis_client
from const.const import USER_API, VERSION_API, USER_TOKEN, PROJECT_NAME, ADMIN, ENABLED, DISABLED
from utils.helper import encrypt_password, generate_random_string, format_json_from_redis
from model.db_init import db
from utils.logs import save_user_login_log, save_system_log


user_api = Blueprint('user_api', __name__)


@user_api.route(f'/{VERSION_API}/{USER_API}/init_admin', methods=['POST'])
def init_admin():
    try:
        username = "admin"
        password = "admin"
        encrypted_password = encrypt_password(password)
        email = "admin@admin.admin"
        group = "admin"
        role = ADMIN
        mfa_status = 0
        is_mfa_enable = 0
        is_password_force_reset = 0
        status = 1
        created_at = int(time.time())

        isExisted = User.query.filter_by(username="admin").first()
        if isExisted:
            l.info(f"Admin is already initiated")
            return response.get_response(response.SUCCESS)

        user = User(username=username, password=encrypted_password, email=email, group=group,
                    role=role, mfa_status=mfa_status, is_mfa_enable=is_mfa_enable, is_password_force_reset=is_password_force_reset, status=status, created_at=created_at)
        db.session.add(user)
        db.session.commit()
        l.info("Initiated admin")
        print("Done Initiation")
        return response.get_response(response.SUCCESS)
    finally:
        pass


@user_api.route(f'/{VERSION_API}/{USER_API}/login', methods=['POST'])
def login():
    try:
        username = str(request.json.get("username"))
        password = str(request.json.get("password"))
        encrypted_password = encrypt_password(password)

        log_user_info = {
            "id": None,
            "username": username,
            "last_login_time": int(time.time()),
            "last_login_ip": request.remote_addr,
            "user_agent": request.headers.get("User-Agent"),
            "status": 0,
            "reason": ""
        }

        user = User.query.filter_by(username=username).first()
        if not user:
            l.error(f"User {username} not found, login failed")
            log_user_info["reason"] = "User not found"
            save_user_login_log(log_user_info)
            return response.get_response(response.USER_NOT_FOUND)

        if user.password != encrypted_password:
            l.error(f"User {username} password is incorrect, login failed")
            log_user_info["id"] = user.id
            log_user_info["reason"] = "Password is incorrect"
            save_user_login_log(log_user_info)
            return response.get_response(response.INVALID_LOGIN_CREDENTIAL)

        if user.status == DISABLED:
            l.error(f"User {username} is disabled, login failed")
            log_user_info["id"] = user.id
            log_user_info["reason"] = "User is disabled"
            save_user_login_log(log_user_info)
            return response.get_response(response.INVALID_USER_STATUS)

        # generate token and write to redis
        token = generate_random_string(20)
        user_redis = {
            "id": int(user.id),
            "username": str(user.username),
            "email": str(user.email),
            "group": str(user.group),
            "mfa_status": int(user.mfa_status),
            "role": int(user.role),
            "status": int(user.status),
            "created_at": int(user.created_at)
        }
        if not redis_client.setex(f"{PROJECT_NAME}:{USER_TOKEN}:{token}", timedelta(days=1), json.dumps(user_redis)):
            l.error(f"Failed to write token to redis")
            return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION)

        # generate user info and return
        user_info = {
            "username": user.username,
            "email": user.email,
            "group": user.group,
            "mfa_status": user.mfa_status,
            "step": 0,
            "role": user.role,
            "status": user.status,
            "created_at": user.created_at
        }
        if user.is_password_force_reset == ENABLED:
            user_info["step"] = 1
        if user_info["step"] != 1 and user.is_mfa_enable == ENABLED:
            user_info["step"] = 2

        log_user_info["id"] = user.id
        log_user_info["status"] = 1
        log_user_info["reason"] = "Login success"
        save_user_login_log(log_user_info)

        return response.get_response(response.SUCCESS, token)
    finally:
        pass


@user_api.route('/{VERSION_API}/{USER_API}/logout', methods=['POST'])
def logout():
    try:
        token = str(request.headers.get("D-token"))

        user_info = format_json_from_redis(
            redis_client.get(f"{PROJECT_NAME}:{USER_TOKEN}:{token}"))
        if not user_info:
            l.error(f"Token {token} not found")
            return response.get_response(response.USER_NOT_FOUND)
        redis_client.delete(f"{PROJECT_NAME}:{USER_TOKEN}:{token}")

        log_user_info = {
            "id": user_info.get("id"),
            "username": user_info.get("username"),
            "last_login_time": int(time.time()),
            "last_login_ip": None,
            "user_agent": request.headers.get("User-Agent"),
            "status": 1,
            "reason": "User Logged Out"
        }
        save_user_login_log(log_user_info)
        return response.get_response(response.SUCCESS)
    finally:
        pass


@user_api.route(f'/{VERSION_API}/{USER_API}/get_user_info', methods=['POST'])
def get_user_info():
    try:
        token = str(request.headers.get("D-token"))
        user_info = redis_client.get(f"{PROJECT_NAME}:{USER_TOKEN}:{token}")
        if not user_info:
            l.error(f"Token {token} not found")
            return response.get_response(response.USER_NOT_FOUND)

        return response.get_response(response.SUCCESS, format_json_from_redis(user_info))
    finally:
        pass


@user_api.route(f'/{VERSION_API}/{USER_API}/add', methods=['POST'])
def add():
    submitted_admin_token = str(request.headers.get("D-token"))

    username = str(request.json.get("username"))
    password = str(request.json.get("password"))
    email = str(request.json.get("email"))
    group = str(request.json.get("group"))
    role = int(request.json.get("role"))
    mfa_status = int(request.json.get("mfa_status"))
    is_mfa_enable = int(request.json.get("is_mfa_enable"))
    is_password_force_reset = int(
        request.json.get("is_password_force_reset"))
    encrypted_password = encrypt_password(password)

    # read from redis
    admin_token = format_json_from_redis(redis_client.get(
        f"{PROJECT_NAME}:{USER_TOKEN}:{submitted_admin_token}"))
    # verify admin
    if not admin_token:
        l.error(f"Admin {submitted_admin_token} not found")
        return response.get_response(response.USER_NOT_FOUND)

    if admin_token.get("role") != ADMIN:
        l.error(f"Admin {admin_token.get('username')} is not admin")
        return response.get_response(response.FORBIDDEN)

    # Check if user already exists
    user = User.query.filter_by(username=username).first()
    if user:
        l.error(f"User {username} already exists")
        return response.get_response(response.USER_EXISTED)

    # Add Information
    # unix timestamp
    time_now = int(time.time())
    status = 1

    # write to db
    user = User(username=username, password=encrypted_password, email=email, group=group,
                role=role, mfa_status=mfa_status, status=status, created_at=time_now, is_mfa_enable=is_mfa_enable, is_password_force_reset=is_password_force_reset)

    db.session.add(user)
    db.session.commit()

    l.info(f"Admin: {admin_token['username']} added User {username}")

    system_log_info = {
        "username": admin_token["username"],
        "role": admin_token["role"],
        "action": "Add User",
        "source": "User",
        "description": f"Admin: {admin_token['username']} added User {username}",
        "created_at": time_now
    }
    save_system_log(system_log_info)

    return response.get_response(response.SUCCESS)
