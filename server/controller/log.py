import time
from flask import Blueprint, request
from const import response
from log import logger as l
from model.user_log_model import UserLog
from model.system_log_model import SystemLog
import const.const as const
from utils.credential import check_admin_account


log_api = Blueprint('log_api', __name__)


@log_api.route(f'/{const.VERSION_API}/{const.LOG_API}/list/<page>', methods=['POST'])
def get_list(page: str):
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        if page == "user":
            user_log = UserLog.query.all()
            user_log_list = []
            for log in user_log:
                user_log_list.append({
                    "id": log.id,
                    "user_id": log.user_id,
                    "username": log.username,
                    "last_login_time": log.last_login_time * 1000,
                    "last_login_ip": log.last_login_ip,
                    "user_agent": log.user_agent,
                    "status": log.status,
                    "reason": log.reason,
                })
            return response.get_response(response.SUCCESS, {"user_log": user_log_list})
        elif page == "system":
            system_log = SystemLog.query.all()
            system_log_list = []
            for log in system_log:
                system_log_list.append({
                    "id": log.id,
                    "username": log.username,
                    "role": log.role,
                    "action": log.action,
                    "source": log.source,
                    "description": log.description,
                    "created_at": log.created_at * 1000
                })
            return response.get_response(response.SUCCESS, {"system_log": system_log_list})

        return response.get_response(response.INVALID_PARAMETER)
    except Exception as e:
        l.error(f"Get redis list failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass
