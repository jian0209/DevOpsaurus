# base
PROJECT_NAME = "DevOpsaurus"
VERSION = "1.0.0"
VERSION_API = "api/v1"

# api key
USER_API = "user"
REDIS_API = "redis"
NODES_API = "nodes"
DATABASE_API = "database"
COMMAND_API = "command"
SETTING_API = "settings"
LOG_API = "log"

# redis key
USER_TOKEN = "user_token"
MFA_TIME = "mfa_time"

# user role
VISITOR = 0
READER = 1
EDITOR = 2
ADMIN = 3

ROLES = {
    VISITOR: "visitor",
    READER: "reader",
    EDITOR: "editor",
    ADMIN: "admin"
}

# status
ENABLED = 1
DISABLED = 0

# user login step
LOGIN_WITH_PASSWORD_ONLY = 0
LOGIN_WITH_MFA_WITHOUT_SECRET_KEY = 1
LOGIN_WITH_MFA_WITH_SECRET_KEY = 2
LOGIN_WITH_FORCE_RESET_PASSWORD = 3
