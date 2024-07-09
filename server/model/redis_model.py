from model.db_init import db


class Redis(db.Model):
    __tablename__ = 'd_redis'
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(50))
    host = db.Column(db.String(200))
    port = db.Column(db.Integer, default=6379)
    auth = db.Column(db.String(200), default='')
    database = db.Column(db.Integer, default=0)
    get = db.Column(db.String(200))
    status = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP)
