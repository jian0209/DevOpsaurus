import logging
from datetime import date
from logging.handlers import TimedRotatingFileHandler
from conf import config

logger = logging.getLogger(__name__)
handler = TimedRotatingFileHandler(config.Config.LOG_PATH + "api_server-{date}.log".format(
    date=str(date.today())), when="D", interval=1, backupCount=7)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)-7s (%(filename)s:%(lineno)d) - %(message)s', '%Y-%m-%d %H:%M:%S')

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
