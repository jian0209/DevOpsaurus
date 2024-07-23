from datetime import timedelta
import json
import time
from flask import Blueprint, request
from const import response
from log import logger as l
from model.user_model import User
from model.redis_init import redis_client
import const.const as const
from conf.config import Config as c
from utils.helper import encrypt_password, generate_random_string, format_json_from_redis, verify_otp, generate_qr_code
from utils.credential import check_admin_account
from model.db_init import db
from utils.logs import save_user_login_log, save_system_log
from utils.message import send_all_message
from utils.init import init_admin_account


user_api = Blueprint('user_api', __name__)


@user_api.route(f'/{const.VERSION_API}/{const.USER_API}/init_admin', methods=['POST'])
def init_admin():
    try:
        init_admin_account(c.INITIAL_USERNAME,
                           c.INITIAL_PASSWORD, c.INITIAL_EMAIL, True)
        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Init admin failed: {str(e)}")
        print(f"Init admin failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})


@user_api.route(f'/{const.VERSION_API}/{const.USER_API}/reset_admin', methods=['POST'])
def reset_admin():
    try:
        if request.remote_addr != "127.0.0.1":
            l.error(f"Reset admin failed, request from {request.remote_addr}")
            return response.get_response(response.FORBIDDEN)

        init_admin_account(c.INITIAL_USERNAME,
                           c.INITIAL_PASSWORD, c.INITIAL_EMAIL)

        print("Admin reset successfully!")
        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Reset admin failed: {str(e)}")
        print(f"Reset admin failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})


@user_api.route(f'/{const.VERSION_API}/{const.USER_API}/login', methods=['POST'])
def login():
    try:
        username = str(request.json.get("username", ""))
        password = str(request.json.get("password", ""))
        encrypted_password = encrypt_password(password)

        log_user_info = {
            "user_id": 0,
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
            log_user_info["user_id"] = user.id
            log_user_info["reason"] = "Password is incorrect"
            save_user_login_log(log_user_info)
            return response.get_response(response.INVALID_LOGIN_CREDENTIAL)

        if user.status == const.DISABLED:
            l.error(f"User {username} is disabled, login failed")
            log_user_info["user_id"] = user.id
            log_user_info["reason"] = "User is disabled"
            save_user_login_log(log_user_info)
            return response.get_response(response.INVALID_USER_STATUS)

        user_info = {
            "username": user.username,
            "step": const.LOGIN_WITH_PASSWORD_ONLY,
            "role": user.role
        }

        if user.mfa_status == const.ENABLED and not user.mfa_secret_key:
            # if user has enabled mfa but not set secret key
            # redirect to set secret key
            user_info["step"] = const.LOGIN_WITH_MFA_WITHOUT_SECRET_KEY
        elif user.mfa_status == const.ENABLED:
            # if user has enabled mfa and set secret key
            # redirect to mfa login
            user_info["step"] = const.LOGIN_WITH_MFA_WITH_SECRET_KEY
        elif user.is_password_force_reset == const.ENABLED:
            # if user has disabled mfa and need to reset password
            user_info["step"] = const.LOGIN_WITH_FORCE_RESET_PASSWORD
        else:
            # if user has disabled mfa and not need to reset password
            # generate token and write to redis
            token = generate_random_string(20)
            user_info["token"] = token
            user_redis = {
                "id": int(user.id),
                "username": str(user.username),
                "email": str(user.email),
                "group": str(user.group),
                "mfa_status": int(user.mfa_status),
                "role": int(user.role),
                "is_favourite": int(user.is_favourite),
                "status": int(user.status),
                "created_at": int(user.created_at)
            }
            if not redis_client.setex(f"{const.PROJECT_NAME}:{const.USER_TOKEN}:{token}", timedelta(days=1), json.dumps(user_redis)):
                l.error(f"Failed to write token to redis")
                return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})

            log_user_info["user_id"] = user.id
            l.info(f"User {username} user id {user.id} login successfully")
            log_user_info["status"] = 1
            log_user_info["reason"] = "Login Successfully"
            save_user_login_log(log_user_info)

        return response.get_response(response.SUCCESS, user_info)
    except Exception as e:
        l.error(f"Login failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@user_api.route(f'/{const.VERSION_API}/{const.USER_API}/get_mfa_img', methods=['POST'])
def get_mfa_img():
    try:
        username = str(request.json.get("username", ""))
        user = User.query.filter_by(username=username).first()
        if not user:
            l.error(f"User {username} not found")
            return response.get_response(response.USER_NOT_FOUND)

        secret_key, base_img = generate_qr_code(username)

        # update secret key to db
        user.mfa_secret_key = secret_key
        db.session.commit()

        return response.get_response(response.SUCCESS, {"img": base_img, "secret_key": secret_key})
    except Exception as e:
        l.error(f"get mfa img: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})


@user_api.route(f'/{const.VERSION_API}/{const.USER_API}/mfa_login', methods=['POST'])
def mfa_login():
    try:
        username = str(request.json.get("username", ""))
        mfa_token = str(request.json.get("mfa_token", ""))

        user = User.query.filter_by(username=username).first()
        if not user:
            l.error(f"User {username} not found")
            return response.get_response(response.USER_NOT_FOUND)

        return_data = {
            "step": const.LOGIN_WITH_PASSWORD_ONLY,
            "role": user.role
        }

        # get redis key for mfa time limit
        mfa_time = redis_client.get(
            f"{const.PROJECT_NAME}:{const.MFA_TIME}:{username}")

        if not mfa_time:
            mfa_time = 0
        if int(mfa_time) > 5:
            l.error(f"{username} MFA login failed, too many attempts")
            if not redis_client.set(f"{const.PROJECT_NAME}:{const.MFA_TIME}:{username}", int(mfa_time) + 1, ex=1800):
                l.error(f"Failed to write mfa time to redis")
                return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
            save_user_login_log({
                "id": user.id,
                "username": username,
                "last_login_time": int(time.time()),
                "last_login_ip": request.remote_addr,
                "user_agent": request.headers.get("User-Agent"),
                "status": 0,
                "reason": "MFA too many attempts: {mfa_time}"
            })
            return response.get_response(response.MFA_TOO_MANY_ATTEMPTS)

        # get secret key
        if not user.mfa_secret_key:
            l.error(f"User {username} has not set mfa secret key")
            return_data = {
                "username": user.username,
                "step": const.LOGIN_WITH_MFA_WITHOUT_SECRET_KEY,
                "role": user.role
            }
            return response.get_response(response.MFA_NOT_SET, return_data)

        # verify mfa token
        if verify_otp(user.mfa_secret_key, mfa_token):
            token = generate_random_string(20)
            return_data["token"] = token
            # generate token and write to redis
            user_redis = {
                "id": int(user.id),
                "username": str(user.username),
                "email": str(user.email),
                "group": str(user.group),
                "mfa_status": int(user.mfa_status),
                "role": int(user.role),
                "is_favourite": int(user.is_favourite),
                "status": int(user.status),
                "created_at": int(user.created_at)
            }
            if not redis_client.setex(f"{const.PROJECT_NAME}:{const.USER_TOKEN}:{token}", timedelta(days=1), json.dumps(user_redis)):
                l.error(f"Failed to write token to redis")
                return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
            redis_client.delete(
                f"{const.PROJECT_NAME}:{const.MFA_TIME}:{username}")
            if user.is_password_force_reset == const.ENABLED:
                return_data = {
                    "token": token,
                    "step": const.LOGIN_WITH_FORCE_RESET_PASSWORD,
                    "role": user.role
                }
            save_user_login_log({
                "id": user.id,
                "username": username,
                "last_login_time": int(time.time()),
                "last_login_ip": request.remote_addr,
                "user_agent": request.headers.get("User-Agent"),
                "status": 1,
                "reason": "Login Successfully"
            })
        else:
            l.error(f"{username}: MFA token is incorrect")
            if not redis_client.set(f"{const.PROJECT_NAME}:{const.MFA_TIME}:{username}", int(mfa_time) + 1, ex=1800):
                l.error(f"Failed to write mfa time to redis")
                return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
            save_user_login_log({
                "id": user.id,
                "username": username,
                "last_login_time": int(time.time()),
                "last_login_ip": request.remote_addr,
                "user_agent": request.headers.get("User-Agent"),
                "status": 0,
                "reason": "Login Failed with MFA token incorrect"
            })
            return response.get_response(response.INVALID_MFA_LOGIN)

        return response.get_response(response.SUCCESS, return_data)
    except Exception as e:
        l.error(f"MFA login failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})


@user_api.route(f'/{const.VERSION_API}/{const.USER_API}/reset_password', methods=['POST'])
def reset_password():
    try:

        username = str(request.json.get("username", ""))
        old_password = str(request.json.get("old_password", ""))
        new_password = str(request.json.get("new_password", ""))
        encrypted_password = encrypt_password(new_password)

        user = User.query.filter_by(username=username).first()
        if not user:
            l.error(f"User {username} not found")
            system_log_info = {
                "username": username,
                "role": "-",
                "action": "Reset Password",
                "source": "Settings",
                "description": f"User {username} failed to reset password, user not found",
                "created_at": int(time.time())
            }
            save_system_log(system_log_info)
            return response.get_response(response.USER_NOT_FOUND)

        # check old password
        if old_password != "" and user.password != encrypt_password(old_password):
            l.error(f"User {username} old password is incorrect")
            system_log_info = {
                "username": username,
                "role": user.role,
                "action": "Reset Password",
                "source": "Settings",
                "description": f"User {username} failed to reset password, old password is incorrect",
                "created_at": int(time.time())
            }
            save_system_log(system_log_info)
            return response.get_response(response.INVALID_OLD_PASSWORD)

        # set new password
        user.password = encrypted_password
        # disable force reset password
        user.is_password_force_reset = const.DISABLED
        db.session.commit()
        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Reset password failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})


@user_api.route(f'/{const.VERSION_API}/{const.USER_API}/logout', methods=['POST'])
def logout():
    try:
        token = str(request.headers.get("D-token"))

        user_info = format_json_from_redis(
            redis_client.get(f"{const.PROJECT_NAME}:{const.USER_TOKEN}:{token}"))
        if not user_info:
            l.error(f"Token {token} not found")
            return response.get_response(response.USER_NOT_FOUND)
        redis_client.delete(f"{const.PROJECT_NAME}:{const.USER_TOKEN}:{token}")

        log_user_info = {
            "user_id": user_info.get("id"),
            "username": user_info.get("username"),
            "last_login_time": int(time.time()),
            "last_login_ip": "-",
            "user_agent": request.headers.get("User-Agent"),
            "status": 1,
            "reason": "User Logged Out"
        }
        save_user_login_log(log_user_info)
        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Logout failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@user_api.route(f'/{const.VERSION_API}/{const.USER_API}/get_user_info', methods=['POST'])
def get_user_info():
    try:
        token = str(request.headers.get("D-token"))
        user_info = redis_client.get(
            f"{const.PROJECT_NAME}:{const.USER_TOKEN}:{token}")
        if not user_info:
            l.error(f"Token {token} not found")
            return response.get_response(response.USER_NOT_FOUND)

        return response.get_response(response.SUCCESS, format_json_from_redis(user_info))
    except Exception as e:
        l.error(f"Get user info failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@user_api.route(f'/{const.VERSION_API}/{const.USER_API}/add', methods=['POST'])
def add():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        username = str(request.json.get("username", ""))
        password = str(request.json.get("password", ""))
        email = str(request.json.get("email", ""))
        group = str(request.json.get("group", ""))
        role = int(request.json.get("role", 0))
        mfa_status = int(request.json.get("mfa_status", 0))
        is_password_force_reset = const.ENABLED
        encrypted_password = encrypt_password(password)

        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            l.error(f"User {username} already exists")
            return response.get_response(response.USER_EXISTED)

        # Add Information
        # unix timestamp
        time_now = int(time.time())
        status = c.ENABLED
        is_favourite = c.DISABLED

        # write to db
        user = User(username=username, password=encrypted_password, email=email, group=group,
                    role=role, is_favourite=is_favourite, mfa_status=mfa_status, status=status, created_at=time_now, is_password_force_reset=is_password_force_reset)

        db.session.add(user)
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} added User {username}")

        system_log_info = {
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Add User",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} added User {username}",
            "created_at": time_now
        }
        save_system_log(system_log_info)
        welcome_email_message = f"""
Dear {username},

Welcome to devopsaurus! We're thrilled to have you on board and look forward to seeing you thrive with us. Your account has been successfully created with the following details:

Username: {username}
Email: {email}
Group: {group}
Role: {role}
Url: {c.WEB_URL}

Please take a moment to login and update your password.

Best regards
"""
        send_all_message(welcome_email_message, email_to=email)

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Add user failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@user_api.route(f'/{const.VERSION_API}/{const.USER_API}/edit', methods=['POST'])
def edit_user():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        username = str(request.json.get("username", ""))
        password = str(request.json.get("password", None))
        if password != "None":
            encrypted_password = encrypt_password(password)
        else:
            encrypted_password = None
        email = str(request.json.get("email", ""))
        group = str(request.json.get("group", ""))
        role = int(request.json.get("role", 0))
        mfa_status = int(request.json.get("mfa_status", 0))
        is_password_force_reset = int(
            request.json.get("is_password_force_reset", 0))

        user = User.query.filter_by(username=username).first()
        if not user:
            l.error(f"User {username} not found")
            return response.get_response(response.USER_NOT_FOUND)

        if encrypted_password:
            user.password = encrypted_password
        user.email = email
        user.group = group
        user.role = role
        user.mfa_status = mfa_status
        user.is_password_force_reset = is_password_force_reset
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} edited User {username}")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Edit User",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} edited User {username}",
            "created_at": int(time.time())
        })

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Edit user failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})


@user_api.route(f'/{const.VERSION_API}/{const.USER_API}/delete', methods=['POST'])
def delete_user():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        username = str(request.json.get("username", ""))

        user = User.query.filter_by(username=username).first()
        if not user:
            l.error(f"User {username} not found")
            return response.get_response(response.USER_NOT_FOUND)

        db.session.delete(user)
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} deleted User {username}")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Delete User",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} deleted User {username}",
            "created_at": int(time.time())
        })
        send_all_message(f"{admin_info['username']} deleted User {username}")

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Delete user failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@user_api.route(f'/{const.VERSION_API}/{const.USER_API}/edit_favourite', methods=['POST'])
def edit_favourite():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        username = str(request.json.get("username", ""))
        is_favourite = int(request.json.get("is_favourite", 0))
        favourite_name = "Star" if is_favourite == 1 else "Un-star"

        user = User.query.filter_by(username=username).first()
        if not user:
            l.error(f"User {username} not found")
            return response.get_response(response.USER_NOT_FOUND)

        user.is_favourite = is_favourite
        db.session.commit()

        l.info(
            f"Admin: {admin_info['username']} edited User {username} status")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Edit User Favourite",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} {favourite_name} User {username}",
            "created_at": int(time.time())
        })

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Favourite user failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@user_api.route(f'/{const.VERSION_API}/{const.USER_API}/edit_status', methods=['POST'])
def edit_status_user():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        username = str(request.json.get("username", ""))
        status = int(request.json.get("status", 0))
        status_name = "Enabled" if status == 1 else "Disabled"

        user = User.query.filter_by(username=username).first()
        if not user:
            l.error(f"User {username} not found")
            return response.get_response(response.USER_NOT_FOUND)

        user.status = status
        db.session.commit()

        l.info(
            f"Admin: {admin_info['username']} edited User {username} status")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Edit User Status",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} edited User {username} status to {status_name}",
            "created_at": int(time.time())
        })

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Edit user status failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@user_api.route(f'/{const.VERSION_API}/{const.USER_API}/list', methods=['POST'])
def get_list():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        search_name = str(request.json.get("name", ""))
        if search_name != "None":
            users = User.query.filter(
                User.username.like(f"%{search_name}%")).all()
        else:
            users = User.query.all()
        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "group": user.group,
                "role": user.role,
                "mfa_status": user.mfa_status,
                "status": user.status,
                "is_password_force_reset": user.is_password_force_reset,
                "created_at": user.created_at * 1000
            })

        return response.get_response(response.SUCCESS, {"users": user_list})
    except Exception as e:
        l.error(f"Get user list failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass
