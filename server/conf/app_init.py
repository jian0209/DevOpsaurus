from flask_cors import CORS
from flask import Flask, abort
from flask import request
from conf import config
from const import response
from controller.health import health_api
from controller.user import user_api
from log import logger as l
from model.db_init import db
from model.redis_init import redis_client

import json

# init app
app = Flask(__name__)
app.config.from_object(config.Config)
app.register_blueprint(health_api)
app.register_blueprint(user_api)

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
    l.info(
        "request url: {url}, method: {method}, format: {format}, body: {body}".format(
            url=request.url, method=request.method, format=request.content_type, body=str(
                request.data)
        ))
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
