from model.db_init import db


class SystemLog(db.Model):
    __tablename__ = 'd_system_log'
    id = db.Column(db.BIGINT, primary_key=True)
    username = db.Column(db.String(50))
    role = db.Column(db.Integer)
    action = db.Column(db.String(200))
    source = db.Column(db.String(200))
    description = db.Column(db.String(200))
    created_at = db.Column(db.Integer)
