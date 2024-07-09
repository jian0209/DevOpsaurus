from model.db_init import db


class Database(db.Model):
    __tablename__ = 'd_database'
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    host = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    port = db.Column(db.Integer, nullable=False, default=3306)
    database = db.Column(db.String(50), nullable=False)
    table = db.Column(db.String(50), nullable=False)
    parameter = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Integer, default=0)
    created_at = db.Column(db.Integer, default=0)
