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
ADMIN_TOKEN_NOT_FOUND = 1010
MFA_DISABLED = 1011
MFA_NOT_SET = 1012
INVALID_MFA_LOGIN = 1013
MFA_TOO_MANY_ATTEMPTS = 1014
INVALID_OLD_PASSWORD = 1015
COMMAND_EXISTED = 1016
COMMAND_NOT_FOUND = 1017
SSH_AUTH_ERROR = 1018
SSH_CONNECTION_ERROR = 1019
SSH_EXCEPTION = 1020
DATABASE_EXISTED = 1021
DATABASE_NOT_FOUND = 1022
DATABASE_CONN_ERROR = 1023
NODES_EXISTED = 1024
NODES_NOT_FOUND = 1025
REDIS_EXISTED = 1026
REDIS_NOT_FOUND = 1027
REDIS_CONN_ERROR = 1028

SYSTEM_INTERNAL_EXCEPTION = 9001
PAGE_NOT_FOUND = 9002
UNSUPPORTED_MEDIA_TYPE = 9003
FORBIDDEN = 9004
BAD_REQUEST = 9005

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
    1010: "Admin token not found",
    1011: "Your MFA is disabled, please contact admin to enable it.",
    1012: "Your MFA is not set, please set it now.",
    1013: "Invalid MFA code",
    1014: "MFA too many attempts, please try again 30 minutes later.",
    1015: "Invalid old password",
    1016: "Command name existed",
    1017: "Command not found",
    1018: "SSH authentication error",
    1019: "SSH connection error",
    1020: "SSH exception",
    1021: "Database name existed",
    1022: "Database not found",
    1023: "Database connection failed",
    1024: "Nodes existed",
    1025: "Nodes not found",
    1026: "Redis existed",
    1027: "Redis not found",
    1028: "Redis connection failed",

    9001: "System internal exception",
    9002: "Page not found",
    9003: "Unsupported media type",
    9004: "403 Forbidden",
    9005: "400 Bad request"
}


def get_response(code, data=dict()):
    return {"code": code, "msg": response_const.get(code), "data": data}
