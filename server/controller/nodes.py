import time
from flask import Blueprint, request
from const import response
from log import logger as l
from model.nodes_model import Nodes
import const.const as const
from utils.credential import check_admin_account
from model.db_init import db
from utils.logs import save_system_log
from utils.helper import connect_to_database


nodes_api = Blueprint('nodes_api', __name__)


@nodes_api.route(f'/{const.VERSION_API}/{const.NODES_API}/add', methods=['POST'])
def add():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        name = str(request.json.get("name", ""))
        group_name = str(request.json.get("group_name", ""))
        group_url = str(request.json.get("group_url", ""))
        target_url = str(request.json.get("target_url", ""))
        fetch_parameter = str(request.json.get("fetch_parameter", ""))

        # Check if user already exists
        nodes = Nodes.query.filter_by(name=name).first()
        if nodes:
            l.error(f"Nodes name {name} already exists")
            return response.get_response(response.NODES_EXISTED)

        # Add Information
        time_now = int(time.time())
        status = 1

        # write to db
        add_node = Nodes(name=name, group_name=group_name, group_url=group_url, fetch_parameter=fetch_parameter,
                         target_url=target_url, status=status, created_at=time_now)

        db.session.add(add_node)
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} added Nodes {name}")

        system_log_info = {
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Add Nodes",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} added Nodes {name}",
            "created_at": time_now
        }
        save_system_log(system_log_info)

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Add Nodes failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION)
    finally:
        pass


@nodes_api.route(f'/{const.VERSION_API}/{const.NODES_API}/edit', methods=['POST'])
def edit_node():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        name = str(request.json.get("name", ""))
        group_name = str(request.json.get("group_name", ""))
        group_url = str(request.json.get("group_url", ""))
        target_url = str(request.json.get("target_url", ""))
        fetch_parameter = str(request.json.get("fetch_parameter", ""))

        node = Nodes.query.filter_by(name=name).first()
        if not node:
            l.error(f"Node {name} not found")
            return response.get_response(response.NODES_NOT_FOUND)

        node.group_name = group_name
        node.group_url = group_url
        node.target_url = target_url
        node.fetch_parameter = fetch_parameter
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} edited Node {name}")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Edit Node",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} edited Database {name}",
            "created_at": int(time.time())
        })

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Edit Node failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION)


@nodes_api.route(f'/{const.VERSION_API}/{const.NODES_API}/delete', methods=['POST'])
def delete_node():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        name = str(request.json.get("name", ""))

        node = Nodes.query.filter_by(name=name).first()
        if not node:
            l.error(f"Node {name} not found")
            return response.get_response(response.NODES_NOT_FOUND)

        db.session.delete(node)
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} deleted Node {name}")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Delete Node",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} deleted Node {name}",
            "created_at": int(time.time())
        })

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Delete nodes failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION)
    finally:
        pass


@nodes_api.route(f'/{const.VERSION_API}/{const.NODES_API}/edit_status', methods=['POST'])
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

        node = Nodes.query.filter_by(name=name).first()
        if not node:
            l.error(f"Node {name} not found")
            return response.get_response(response.NODES_NOT_FOUND)

        node.status = status
        db.session.commit()

        l.info(
            f"Admin: {admin_info['username']} edited Node {name} status")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Edit Node Status",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} edited Node {name} status to {status_name}",
            "created_at": int(time.time())
        })

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Edit node status failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION)
    finally:
        pass


@nodes_api.route(f'/{const.VERSION_API}/{const.NODES_API}/list', methods=['POST'])
def get_list():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        nodes = Nodes.query.all()
        nodes_list = []
        for node in nodes:
            nodes_list.append({
                "id": node.id,
                "name": node.name,
                "group_name": node.group_name,
                "group_url": node.group_url,
                "target_url": node.target_url,
                "fetch_parameter": node.fetch_parameter,
                "status": node.status,
                "created_at": node.created_at * 1000
            })

        return response.get_response(response.SUCCESS, {"nodes": nodes_list})
    except Exception as e:
        l.error(f"Get nodes list failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION)
    finally:
        pass
