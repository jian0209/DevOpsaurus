from model.db_init import db


class Command(db.Model):
    __tablename__ = 'd_command'
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    host = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    ssh_key = db.Column(db.Text, nullable=False)
    ssh_port = db.Column(db.Integer, nullable=False)
    command = db.Column(db.Text, nullable=False)
    is_favourite = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    created_at = db.Column(db.Integer, default=0)
