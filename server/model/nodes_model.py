from model.db_init import db


class Nodes(db.Model):
    __tablename__ = 'd_nodes'
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    group_name = db.Column(db.String(25), nullable=False)
    group_url = db.Column(db.String(500), nullable=False)
    target_url = db.Column(db.String(500), nullable=False)
    fetch_parameter = db.Column(db.String(200), nullable=True)
    is_favourite = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    created_at = db.Column(db.Integer, default=0)
