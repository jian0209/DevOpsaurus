class Config(object):
    HOST = "0.0.0.0"
    PORT = "9001"
    DEBUG = True
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    REDIS_URL = "redis://:V1dwT1UyRnJNVFpYVkVaT1ZrVnNObFJyVWxaTlp6MDk=@192.168.10.21:6379/0"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://devops:123456@192.168.10.21:3306/devopsaurus"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_PRE_PING = True
    LOG_PATH = "/Users/tecstation/Desktop/nicholas/DevOpsaurus/server/logs/"
    ENCRYPT_KEY = "1234567890abcdef"

    IP_WHITE_LIST = ["127.0.0.1"]
