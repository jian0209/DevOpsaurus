from model.db_init import db


class DockerService(db.Model):
    __tablename__ = 'd_docker_service'
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    status = db.Column(db.Integer, default=0)
    created_at = db.Column(db.Integer, default=0)
