from model.db_init import db


class User(db.Model):
    __tablename__ = 'd_user_info'
    id = db.Column(db.BIGINT, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(32))
    email = db.Column(db.String(50), default='')
    group = db.Column(db.String(50), default='')
    mfa_status = db.Column(db.Integer, default=0)
    is_mfa_enable = db.Column(db.Integer, default='')
    is_password_force_reset = db.Column(db.Integer, default=0)
    role = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP)
