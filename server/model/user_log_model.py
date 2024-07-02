from model.db_init import db


class UserLog(db.Model):
    __tablename__ = 'd_login_log'
    id = db.Column(db.BIGINT, primary_key=True)
    user_id = db.Column(db.BIGINT)
    username = db.Column(db.String(50))
    last_login_time = db.Column(db.Integer)
    last_login_ip = db.Column(db.String(15))
    user_agent = db.Column(db.String(200))
    status = db.Column(db.Integer)
    reason = db.Column(db.String(200))
