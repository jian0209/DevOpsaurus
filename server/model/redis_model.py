from model.db_init import db


class User(db.Model):
    __tablename__ = 'd_user_info'
    id = db.Column(db.BIGINT, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(24))
    email = db.Column(db.String(50), default='')
    group = db.Column(db.String(50), default='')
    mfa_status = db.Column(db.Integer, default=0)
    role = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP)


def add_user(user_info=dict):
    user = User()
    user.username = user_info.get("username")
    user.password = user_info.get("password")
    user.email = user_info.get("email")
    user.group = user_info.get("group")
    user.mfa_status = user_info.get("mfa_status")
    user.role = user_info.get("role")
    user.status = user_info.get("status")
    user.created_at = user_info.get("created_at")
    db.session.add(user)
    db.session.commit()
    return user


def edit_user(user_info=dict):
    user = User.query.filter_by(username=user_info.get("username")).first()
    user.password = user_info.get("password")
    user.email = user_info.get("email")
    user.group = user_info.get("group")
    user.mfa_status = user_info.get("mfa_status")
    user.role = user_info.get("role")
    user.status = user_info.get("status")
    user.created_at = user_info.get("created_at")
    db.session.commit()
    return user


def delete_user(userId):
    user = User.query.filter_by(id=userId).first()
    db.session.delete(user)
    db.session.commit()
    return user


def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user


def get_user_list():
    user_list = User.query.all()
    return user_list
