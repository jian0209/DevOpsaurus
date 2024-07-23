import time
from model.user_model import User
from utils.helper import encrypt_password
from const import const
from log import logger as l
from model.db_init import db


def init_admin_account(username: str, password: str, email: str, is_init: bool = False) -> bool:
    admin_id = 1
    encrypted_password = encrypt_password(password)
    group = "admin"
    role = const.ADMIN
    mfa_status = const.DISABLED
    is_password_force_reset = const.DISABLED
    status = const.ENABLED
    is_favourite = const.DISABLED
    created_at = int(time.time())

    is_existed = User.query.filter_by(username=username).first()

    user = User(id=admin_id, username=username, password=encrypted_password, email=email, group=group,
                role=role, mfa_status=mfa_status, is_password_force_reset=is_password_force_reset, is_favourite=is_favourite, status=status, created_at=created_at)

    if not is_init and is_existed:
        l.info(f"Delete existed {username}")
        db.session.delete(is_existed)
        db.session.commit()

        db.session.add(user)
        db.session.commit()
        l.info(f"Initiated {username}")
        return True

    if is_existed:
        l.info(f"{username} is already initiated")
        return True

    l.info(f"Start Initiating {username}")
    db.session.add(user)
    db.session.commit()
    l.info(f"Initiated {username}")

    return True
