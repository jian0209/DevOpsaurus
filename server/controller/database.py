import time
from flask import Blueprint, request
from const import response
from log import logger as l
from model.database_model import Database
import const.const as const
from utils.credential import check_admin_account, check_user_account
from utils.message import send_all_message
from model.db_init import db
from utils.logs import save_system_log
from utils.helper import connect_to_database
from decimal import Decimal
from datetime import datetime


database_api = Blueprint('database_api', __name__)


@database_api.route(f'/{const.VERSION_API}/{const.DATABASE_API}/add', methods=['POST'])
def add():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        name = str(request.json.get("name", ""))
        host = str(request.json.get("host", ""))
        username = str(request.json.get("username", ""))
        password = str(request.json.get("password", ""))
        port = int(request.json.get("port", 3306))
        database = str(request.json.get("database", ""))
        table = str(request.json.get("table", ""))
        select = str(request.json.get("select", ""))
        parameter = str(request.json.get("parameter", ""))

        # Check if user already exists
        data_database = Database.query.filter_by(name=name).first()
        if data_database:
            l.error(f"Database name {name} already exists")
            return response.get_response(response.DATABASE_EXISTED)

        # Add Information
        time_now = int(time.time())
        status = 1

        # write to db
        add_database = Database(name=name, host=host, username=username, password=password, port=port,
                                database=database, table=table, select=select, parameter=parameter, status=status, created_at=time_now)

        db.session.add(add_database)
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} added Database {name}")

        system_log_info = {
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Add Database",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} added Database {name}",
            "created_at": time_now
        }
        save_system_log(system_log_info)
        send_all_message(f"{admin_info['username']} added Database {name}")

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Add Database failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@database_api.route(f'/{const.VERSION_API}/{const.DATABASE_API}/edit', methods=['POST'])
def edit_database():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        name = str(request.json.get("name", ""))
        host = str(request.json.get("host", ""))
        username = str(request.json.get("username", ""))
        password = str(request.json.get("password", ""))
        port = int(request.json.get("port", 3306))
        database = str(request.json.get("database", ""))
        table = str(request.json.get("table", ""))
        select = str(request.json.get("select", ""))
        parameter = str(request.json.get("parameter", ""))

        data_database = Database.query.filter_by(name=name).first()
        if not data_database:
            l.error(f"Database {name} not found")
            return response.get_response(response.DATABASE_NOT_FOUND)

        data_database.host = host
        data_database.username = username
        data_database.password = password
        data_database.port = port
        data_database.database = database
        data_database.table = table
        data_database.select = select
        data_database.parameter = parameter
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} edited Database {name}")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Edit Database",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} edited Database {name}",
            "created_at": int(time.time())
        })
        send_all_message(f"{admin_info['username']} edited Database {name}")

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Edit database failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})


@database_api.route(f'/{const.VERSION_API}/{const.DATABASE_API}/delete', methods=['POST'])
def delete_database():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        name = str(request.json.get("name", ""))

        data_database = Database.query.filter_by(name=name).first()
        if not data_database:
            l.error(f"Database {name} not found")
            return response.get_response(response.DATABASE_NOT_FOUND)

        db.session.delete(data_database)
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} deleted Database {name}")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Delete Database",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} deleted Database {name}",
            "created_at": int(time.time())
        })
        send_all_message(f"{admin_info['username']} deleted Database {name}")

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Delete database failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@database_api.route(f'/{const.VERSION_API}/{const.DATABASE_API}/edit_status', methods=['POST'])
def edit_status_database():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        name = str(request.json.get("name", ""))
        status = int(request.json.get("status", 0))
        status_name = "Enabled" if status == 1 else "Disabled"

        data_database = Database.query.filter_by(name=name).first()
        if not data_database:
            l.error(f"Database {name} not found")
            return response.get_response(response.DATABASE_NOT_FOUND)

        data_database.status = status
        db.session.commit()

        l.info(
            f"Admin: {admin_info['username']} edited Database {name} status")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Edit Database Status",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} edited Database {name} status to {status_name}",
            "created_at": int(time.time())
        })

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Edit database status failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@database_api.route(f'/{const.VERSION_API}/{const.DATABASE_API}/get_databases', methods=['POST'])
def get_databases():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        host = str(request.json.get("host", ""))
        username = str(request.json.get("username", ""))
        port = int(request.json.get("port", 3306))
        password = str(request.json.get("password", ""))

        databases = tuple()
        database_list = []

        conn = connect_to_database(host, username, password, port)
        if conn is None:
            l.error(f"Error connecting to database")
            return response.get_response(response.DATABASE_CONN_ERROR)

        with conn.cursor() as cursor:
            cursor.execute("show databases")
            databases = cursor.fetchall()
            for database in databases:
                database_list.append(database[0])

        return response.get_response(response.SUCCESS, {"databases": database_list})

    except Exception as e:
        l.error(f"Get databases failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})


@database_api.route(f'/{const.VERSION_API}/{const.DATABASE_API}/get_tables', methods=['POST'])
def get_tables():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        host = str(request.json.get("host", ""))
        username = str(request.json.get("username", ""))
        port = int(request.json.get("port", 3306))
        password = str(request.json.get("password", ""))
        database = str(request.json.get("database", ""))

        table_list = []

        conn = connect_to_database(host, username, password, port)
        if conn is None:
            l.error(f"Error connecting to database")
            return response.get_response(response.DATABASE_CONN_ERROR)

        with conn.cursor() as cursor:
            query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{database}'"
            cursor.execute(query)
            tables = cursor.fetchall()
            table_list = [table[0] for table in tables]

        return response.get_response(response.SUCCESS, {"tables": table_list})

    except Exception as e:
        l.error(f"Get tables failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})


@database_api.route(f'/{const.VERSION_API}/{const.DATABASE_API}/list', methods=['POST'])
def get_list():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        data_database = Database.query.all()
        databases_list = []
        for database in data_database:
            databases_list.append({
                "id": database.id,
                "name": database.name,
                "host": database.host,
                "username": database.username,
                "password": database.password,
                "port": database.port,
                "database": database.database,
                "table": database.table,
                "select": database.select,
                "parameter": database.parameter,
                "status": database.status,
                "created_at": database.created_at * 1000
            })

        return response.get_response(response.SUCCESS, {"databases": databases_list})
    except Exception as e:
        l.error(f"Get database list failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@database_api.route(f'/{const.VERSION_API}/{const.DATABASE_API}/get_database_list', methods=['POST'])
def get_database_list():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, user_info = check_user_account(token, const.READER)

        if not is_allow:
            l.error(f"User {user_info.get('username')} is not Reader or above")
            return response.get_response(response.FORBIDDEN)

        data_database = Database.query.filter_by(status=1).all()
        databases_list = []
        for database in data_database:
            databases_list.append({
                "id": database.id,
                "name": database.name,
                "database": database.database,
                "table": database.table,
                "select": database.select,
                "parameter": database.parameter,
            })

        return response.get_response(response.SUCCESS, {"databases": databases_list})
    except Exception as e:
        l.error(f"Get database list failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@database_api.route(f'/{const.VERSION_API}/{const.DATABASE_API}/execute_query_to_get_data', methods=['POST'])
def execute_query_to_get_data():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, user_info = check_user_account(token, const.READER)

        if not is_allow:
            l.error(f"User {user_info.get('username')} is not Reader or above")
            return response.get_response(response.FORBIDDEN)

        database_id = int(request.json.get("database_id", 0))
        query = str(request.json.get("query", ""))
        # limit = int(request.json.get("limit", 100))

        data_database = Database.query.filter_by(id=database_id).first()
        if not data_database:
            l.error(f"Database {database_id} not found")
            return response.get_response(response.DATABASE_NOT_FOUND)

        conn = connect_to_database(
            data_database.host, data_database.username, data_database.password, data_database.port)
        if conn is None:
            l.error(f"Error connecting to database")
            return response.get_response(response.DATABASE_CONN_ERROR)

        l.info(f"Query: {query}")
        with conn.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            # get columns
            columns = [column[0] for column in cursor.description]

        result = []
        for rows_index, rows in enumerate(data):
            for row_index, row in enumerate(rows):
                if row_index == 0:
                    if isinstance(row, Decimal):
                        result.append({columns[row_index]: format(row, 'f')})
                    elif isinstance(row, datetime):
                        result.append({columns[row_index]: row.strftime(
                            "%Y-%m-%d %H:%M:%S")})
                    else:
                        result.append({columns[row_index]: row})
                else:
                    if isinstance(row, Decimal):
                        result[rows_index][columns[row_index]
                                           ] = format(row, 'f')
                    elif isinstance(row, datetime):
                        result[rows_index][columns[row_index]] = row.strftime(
                            "%Y-%m-%d %H:%M:%S")
                    else:
                        result[rows_index][columns[row_index]] = row

        system_log_info = {
            "username": user_info["username"],
            "role": user_info["role"],
            "action": "Execute Query",
            "source": "Database",
            "description": f"User: {user_info['username']} executed query on Database {data_database.name}",
            "created_at": int(time.time())
        }
        save_system_log(system_log_info)
        send_all_message(
            f"{user_info['username']} executed query on Database {data_database.name}")

        return response.get_response(response.SUCCESS, {"result": result, "columns": columns})
    except Exception as e:
        l.error(f"Execute query to get data failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass
