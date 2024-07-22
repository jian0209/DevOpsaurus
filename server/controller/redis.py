import time
from flask import Blueprint, request
from const import response
from log import logger as l
from model.redis_model import Redis
import const.const as const
from utils.credential import check_admin_account, check_user_account
from utils.message import send_all_message
from model.db_init import db
from utils.logs import save_system_log
from utils.helper import connect_to_redis
import redis


redis_api = Blueprint('redis_api', __name__)


@redis_api.route(f'/{const.VERSION_API}/{const.REDIS_API}/add', methods=['POST'])
def add():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        name = str(request.json.get("name", ""))
        host = str(request.json.get("host", ""))
        port = int(request.json.get("port", 6379))
        auth = str(request.json.get("auth", ""))
        database = int(request.json.get("database", 0))
        get = str(request.json.get("get", ""))

        # Check if user already exists
        redis = Redis.query.filter_by(name=name).first()
        if redis:
            l.error(f"Redis name {name} already exists")
            return response.get_response(response.USER_EXISTED)

        # Add Information
        # unix timestamp
        time_now = int(time.time())
        status = 1

        # write to db
        add_redis = Redis(name=name, host=host, port=port, auth=auth, database=database, get=get, status=status,
                          created_at=time_now)

        db.session.add(add_redis)
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} added Redis {name}")

        system_log_info = {
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Add Redis",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} added Redis {name}",
            "created_at": time_now
        }
        save_system_log(system_log_info)
        send_all_message(f"{admin_info['username']} added Redis {name}")

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Add redis failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@redis_api.route(f'/{const.VERSION_API}/{const.REDIS_API}/edit', methods=['POST'])
def edit_redis():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        name = str(request.json.get("name", ""))
        host = str(request.json.get("host", ""))
        port = int(request.json.get("port", 6379))
        auth = str(request.json.get("auth", ""))
        database = int(request.json.get("database", 0))
        get = str(request.json.get("get", ""))

        redis = Redis.query.filter_by(name=name).first()
        if not redis:
            l.error(f"Redis {name} not found")
            return response.get_response(response.REDIS_NOT_FOUND)

        redis.host = host
        redis.port = port
        redis.auth = auth
        redis.database = database
        redis.get = get
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} edited Command {name}")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Edit Redis",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} edited Redis {name}",
            "created_at": int(time.time())
        })
        send_all_message(f"{admin_info['username']} edited Redis {name}")

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Edit redis failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})


@redis_api.route(f'/{const.VERSION_API}/{const.REDIS_API}/delete', methods=['POST'])
def delete_redis():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        name = str(request.json.get("name", ""))

        redis = Redis.query.filter_by(name=name).first()
        if not redis:
            l.error(f"Redis {name} not found")
            return response.get_response(response.REDIS_NOT_FOUND)

        db.session.delete(redis)
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} deleted Redis {name}")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Delete Redis",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} deleted Redis {name}",
            "created_at": int(time.time())
        })
        send_all_message(f"{admin_info['username']} deleted Redis {name}")

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Delete command failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@redis_api.route(f'/{const.VERSION_API}/{const.REDIS_API}/edit_status', methods=['POST'])
def edit_status_redis():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        name = str(request.json.get("name", ""))
        status = int(request.json.get("status", 0))
        status_name = "Enabled" if status == 1 else "Disabled"

        redis = Redis.query.filter_by(name=name).first()
        if not redis:
            l.error(f"Redis {name} not found")
            return response.get_response(response.REDIS_NOT_FOUND)

        redis.status = status
        db.session.commit()

        l.info(
            f"Admin: {admin_info['username']} edited Redis {name} status")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Edit Redis Status",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} edited Redis {name} status to {status_name}",
            "created_at": int(time.time())
        })

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Edit Command status failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@redis_api.route(f'/{const.VERSION_API}/{const.REDIS_API}/test', methods=['POST'])
def test_redis():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        host = str(request.json.get("host", ""))
        port = int(request.json.get("port", 6379))
        auth = str(request.json.get("auth", ""))

        try:
            conn = connect_to_redis(host, port, auth)
            conn.ping()
            conn.close()
        except Exception as e:
            l.error(f"Redis connection error: {str(e)}")
            return response.get_response(response.REDIS_CONN_ERROR)

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Test redis failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})


@redis_api.route(f'/{const.VERSION_API}/{const.REDIS_API}/list', methods=['POST'])
def get_list():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        search_name = str(request.json.get("name", ""))
        if search_name != "None":
            redis_all = Redis.query.filter(
                Redis.name.like(f"%{search_name}%")).all()
        else:
            redis_all = Redis.query.all()
        redis_list = []
        for redis in redis_all:
            redis_list.append({
                "id": redis.id,
                "name": redis.name,
                "host": redis.host,
                "port": redis.port,
                "auth": redis.auth,
                "database": redis.database,
                "get": redis.get,
                "status": redis.status,
                "created_at": redis.created_at * 1000
            })

        return response.get_response(response.SUCCESS, {"redis": redis_list})
    except Exception as e:
        l.error(f"Get redis list failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@redis_api.route(f'/{const.VERSION_API}/{const.REDIS_API}/get_redis_list', methods=['POST'])
def get_redis_list():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, user_info = check_user_account(token, const.READER)

        if not is_allow:
            l.error(f"User {user_info.get('username')} is not Reader or above")
            return response.get_response(response.FORBIDDEN)

        search_name = str(request.json.get("name", ""))
        if search_name != "None":
            redis_all = Redis.query.filter(
                Redis.name.like(f"%{search_name}%")).filter_by(status=1).all()
        else:
            redis_all = Redis.query.filter_by(status=1).all()

        redis_list = []
        for redis in redis_all:
            redis_list.append({
                "name": redis.name,
                "id": redis.id,
                "get": redis.get,
            })

        return response.get_response(response.SUCCESS, {"redis": redis_list})
    except Exception as e:
        l.error(f"Get redis list failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@redis_api.route(f'/{const.VERSION_API}/{const.REDIS_API}/get_redis_result', methods=['POST'])
def get_redis_result():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, user_info = check_user_account(token, const.READER)

        if not is_allow:
            l.error(f"User {user_info.get('username')} is not Reader or above")
            return response.get_response(response.FORBIDDEN)

        get_key = str(request.json.get("get_key", ""))
        redis_id = str(request.json.get("id", ""))

        redis_detail = Redis.query.filter_by(id=redis_id).first()
        if not redis_detail:
            l.error(f"Redis {redis_id} not found")
            return response.get_response(response.REDIS_NOT_FOUND)

        return_result = {}

        conn = connect_to_redis(
            redis_detail.host, redis_detail.port, redis_detail.auth, redis_detail.database)
        if conn is None:
            l.error(f"Redis connection error")
            return response.get_response(response.REDIS_CONN_ERROR)

        try:
            get_result = conn.get(get_key)
            l.info(f"Get Redis {redis_detail.name} value: {get_result}")
            return_result["result"] = get_result.decode(
            ) if get_result else "nil"
        except Exception as e:
            l.error(f"Redis get error: {str(e)}")
            return_result["result"] = "nil"
        finally:
            conn.close()

        return response.get_response(response.SUCCESS, {"redis": return_result})
    except Exception as e:
        l.error(f"Get redis list failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@redis_api.route(f'/{const.VERSION_API}/{const.REDIS_API}/set_redis_value', methods=['POST'])
def set_redis_value():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, user_info = check_user_account(token, const.EDITOR)

        if not is_allow:
            l.error(f"User {user_info.get('username')} is not Writer or above")
            return response.get_response(response.FORBIDDEN)

        redis_id = int(request.json.get("id", 0))
        get_key = str(request.json.get("get_key", ""))
        value = str(request.json.get("value", ""))

        redis = Redis.query.filter_by(id=redis_id).first()
        if not redis:
            l.error(f"Redis {redis_id} not found")
            return response.get_response(response.REDIS_NOT_FOUND)

        conn = connect_to_redis(redis.host, redis.port,
                                redis.auth, redis.database)
        if conn is None:
            l.error(f"Redis connection error")
            return response.get_response(response.REDIS_CONN_ERROR)

        try:
            conn.set(get_key, value)
        except Exception as e:
            l.error(f"Redis set error: {str(e)}")
            return response.get_response(response.REDIS_SET_ERROR)
        finally:
            conn.close()

        system_log_info = {
            "username": user_info["username"],
            "role": user_info["role"],
            "action": "Set Redis Value",
            "source": "Redis",
            "description": f"User: {user_info['username']} set Redis {redis.name} value to {value}",
            "created_at": int(time.time())
        }
        save_system_log(system_log_info)
        send_all_message(
            f"{user_info['username']} set Redis {redis.name} value to {value}")

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Set redis failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass
