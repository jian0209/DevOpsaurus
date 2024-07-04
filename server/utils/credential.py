import const.const as const
from utils.helper import format_json_from_redis
from model.redis_init import redis_client
from log import logger as l


def check_admin_account(token: str) -> tuple[bool, dict]:
    admin_info = format_json_from_redis(redis_client.get(
        f"{const.PROJECT_NAME}:{const.USER_TOKEN}:{token}"))
    if not admin_info:
        l.error(f"Token {token} not found")
        return False

    if admin_info.get("role") != const.ADMIN:
        l.error(f"Admin {admin_info.get('username')} is not admin")
        return False
    return True, admin_info


def check_user_account(token: str) -> tuple[bool, dict]:
    user_info = format_json_from_redis(redis_client.get(
        f"{const.PROJECT_NAME}:{const.USER_TOKEN}:{token}"))
    if not user_info:
        l.error(f"Token {token} not found")
        return False

    return True, user_info
