from flask import Blueprint
from const import response
from log import logger as l

health_api = Blueprint('health_api', __name__)


@health_api.route('/v1/health', methods=['GET'])
def health():
    return response.get_response(response.SUCCESS)
