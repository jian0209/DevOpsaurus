SUCCESS = 0
INVALID_PARAMETER = 1001
EXISTED_IP = 1002
INVALID_IP = 1003
PROD_CHANGE_ERROR = 1004
PRE_CHANGE_ERROR = 1005
USER_NOT_FOUND = 1006
USER_EXISTED = 1007
INVALID_LOGIN_CREDENTIAL = 1008
INVALID_USER_STATUS = 1009

SYSTEM_INTERNAL_EXCEPTION = 9001
PAGE_NOT_FOUND = 9002
UNSUPPORTED_MEDIA_TYPE = 9003
FORBIDDEN = 9004

response_const = {
    0: "Success",
    1001: "Invalid parameter",
    1002: "Existed ip",
    1003: "Invalid ip",
    1004: "Currently is in production env",
    1005: "Currently is in pre env",
    1006: "User not found",
    1007: "User existed",
    1008: "Invalid username or password",
    1009: "Find your account is disabled, please contact admin to enable it.",

    9001: "System internal exception",
    9002: "Page not found",
    9003: "Unsupported media type",
    9004: "403 Forbidden"
}


def get_response(code, data=dict()):
    return {"code": code, "msg": response_const.get(code), "data": data}
