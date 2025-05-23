import os


class Config(object):
    HOST = "0.0.0.0"
    PORT = 9001
    DEBUG = os.getenv("DEBUG", True)

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    REDIS_URL = f"redis://{os.getenv('REDIS_USERNAME', '')}:{os.getenv('REDIS_AUTH', 'V1dwT1UyRnJNVFpYVkVaT1ZrVnNObFJyVWxaTlp6MDk=')}@{os.getenv('REDIS_HOST', '192.168.10.21')}:{os.getenv('REDIS_PORT', '6379')}/0"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DATABASE_USERNAME','devops')}:{os.getenv('DATABASE_PASSWORD','123456')}@{os.getenv('DATABASE_URL','192.168.10.21')}:{os.getenv('DATABASE_PORT','3306')}/{os.getenv('DATABASE_NAME','devopsaurus')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_PRE_PING = True

    LOG_PATH = os.getenv(
        "LOG_PATH", "/Users/nicholas/Desktop/my-project/note/DevOpsaurus/server/logs/")

    ENCRYPT_KEY = os.getenv("ENCRYPT_KEY", "devopsaurus")
    INITIAL_USERNAME = os.getenv("INITIAL_USERNAME", "admin")
    INITIAL_PASSWORD = os.getenv("INITIAL_PASSWORD", "admin")
    INITIAL_EMAIL = os.getenv("INITIAL_EMAIL", "admin@asd.asd")

    WEB_URL = os.getenv("WEB_URL", "http://localhost:3000")
