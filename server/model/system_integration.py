from model.db_init import db


class SystemIntegration(db.Model):
    __tablename__ = 'd_system_integration'
    id = db.Column(db.BIGINT, primary_key=True)
    is_email_allow = db.Column(db.Integer, default=0)
    is_telegram_allow = db.Column(db.Integer, default=0)
    is_slack_allow = db.Column(db.Integer, default=0)
    email_smtp_server = db.Column(db.String(50), default='')
    email_smtp_port = db.Column(db.Integer, default=0)
    email_smtp_username = db.Column(db.String(50), default='')
    email_smtp_password = db.Column(db.String(50), default='')
    email_from = db.Column(db.String(50), default='')
    email_helo = db.Column(db.String(50), default='')
    email_allow_ssl_tls = db.Column(db.Integer, default=0)
    email_allow_start_tls = db.Column(db.Integer, default=0)
    telegram_bot_token = db.Column(db.String(50), default='')
    telegram_chat_id = db.Column(db.String(50), default='')
    telegram_parse = db.Column(db.Integer, default=0)
    slack_bot_token = db.Column(db.String(50), default='')
    slack_channel = db.Column(db.String(50), default='')
    slack_token = db.Column(db.String(50), default='')
