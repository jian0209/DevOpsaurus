from flask_cors import CORS
from flask import Flask
from flask import request
from conf import config
from const import response
from controller.health import health_api
from controller.user import user_api
from controller.settings import setting_api
from controller.command import command_api
from controller.database import database_api
from controller.nodes import nodes_api
from controller.redis import redis_api
from controller.log import log_api
from log import logger as l
from model.db_init import db
from model.redis_init import redis_client
# from apscheduler.schedulers import Scheduler

import json

# init app
app = Flask(__name__)
app.config.from_object(config.Config)
app.register_blueprint(health_api)
app.register_blueprint(user_api)
app.register_blueprint(setting_api)
app.register_blueprint(command_api)
app.register_blueprint(database_api)
app.register_blueprint(nodes_api)
app.register_blueprint(redis_api)
app.register_blueprint(log_api)

CORS(app, methods=["POST"], supports_credentials=True, max_age=600)

# init db
db.init_app(app)
# init redis
redis_client.init_app(app)
if not redis_client.ping():
    l.error("ping redis error! ")
    exit(1)


@app.errorhandler(404)
def page_not_found(e):
    l.error(str(e))
    return response.get_response(response.PAGE_NOT_FOUND)


@app.errorhandler(415)
def unsupported_media_type(e):
    l.error(str(e))
    return response.get_response(response.UNSUPPORTED_MEDIA_TYPE)


@app.errorhandler(403)
def forbidden(e):
    l.error(str(e))
    return response.get_response(response.FORBIDDEN)


@app.errorhandler(Exception)
def catch_all_exception(e):
    l.error(str(e))
    return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION)


@app.before_request
def before_request():
    if request.form:
        request_body = json.dumps(request.form)
        l.info("request url: {url}, method: {method}, format: form, body: {body}".format(
            url=request.url, method=request.method, body=request_body))
    elif request.json:
        request_body = json.dumps(request.json)
        l.info("request url: {url}, method: {method}, format: json, body: {body}".format(
            url=request.url, method=request.method, body=request_body))
    else:
        pass
