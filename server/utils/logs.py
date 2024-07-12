from model.db_init import db
from model.user_log_model import UserLog
from model.system_log_model import SystemLog


def save_user_login_log(user_info: dict):
    user_id = user_info.get("user_id")
    username = user_info.get("username")
    last_login_time = user_info.get("last_login_time")
    last_login_ip = user_info.get("last_login_ip")
    user_agent = user_info.get("user_agent")
    status = user_info.get("status")
    reason = user_info.get("reason")

    logs_info = UserLog(user_id=user_id, username=username, last_login_time=last_login_time,
                        last_login_ip=last_login_ip, user_agent=user_agent, status=status, reason=reason)

    db.session.add(logs_info)
    db.session.commit()


def save_system_log(system_info: dict):
    username = system_info.get("username")
    role = system_info.get("role")
    action = system_info.get("action")
    source = system_info.get("source")
    description = system_info.get("description")
    created_at = system_info.get("created_at")

    logs_info = SystemLog(username=username, role=role, action=action,
                          source=source, description=description, created_at=created_at)

    db.session.add(logs_info)
    db.session.commit()
