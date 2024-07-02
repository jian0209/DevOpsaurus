from model.db_init import db
from model.user_log_model import UserLog
from model.system_log_model import SystemLog


def save_user_login_log(user_info: dict):
    user_id = user_info.get("id")
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


def save_system_log(log_info: dict):
    username = log_info.get("username")
    role = log_info.get("role")
    action = log_info.get("action")
    source = log_info.get("source")
    description = log_info.get("description")
    created_at = log_info.get("created_at")

    logs_info = SystemLog(username=username, role=role, action=action,
                          source=source, description=description, created_at=created_at)

    db.session.add(logs_info)
    db.session.commit()
