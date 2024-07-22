import time
from flask import Blueprint, request
from const import response
from log import logger as l
from model.command_model import Command
import const.const as const
from utils.credential import check_admin_account, check_user_account
from utils.message import send_all_message
from model.db_init import db
from utils.logs import save_system_log
import paramiko
from io import StringIO


command_api = Blueprint('command_api', __name__)


@command_api.route(f'/{const.VERSION_API}/{const.COMMAND_API}/add', methods=['POST'])
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
        ssh_key = str(request.json.get("ssh_key", ""))
        ssh_port = int(request.json.get("ssh_port", 0))
        command_param = str(request.json.get("command", ""))

        # Check if user already exists
        command = Command.query.filter_by(name=name).first()
        if command:
            l.error(f"Command name {name} already exists")
            return response.get_response(response.USER_EXISTED)

        # Add Information
        # unix timestamp
        time_now = int(time.time())
        status = 1

        # write to db
        command = Command(name=name, host=host, username=username, ssh_key=ssh_key, ssh_port=ssh_port,
                          command=command_param, status=status, created_at=time_now)

        db.session.add(command)
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} added Command {name}")

        system_log_info = {
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Add Command",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} added Command {name}",
            "created_at": time_now
        }
        save_system_log(system_log_info)
        send_all_message(f"{admin_info['username']} added Command {name}")

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Add command failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@command_api.route(f'/{const.VERSION_API}/{const.COMMAND_API}/edit', methods=['POST'])
def edit_command():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        name = str(request.json.get("name", ""))
        host = str(request.json.get("host", ""))
        username = str(request.json.get("username", ""))
        ssh_key = str(request.json.get("ssh_key", ""))
        ssh_port = int(request.json.get("ssh_port", 0))
        command_param = str(request.json.get("command", ""))

        command = Command.query.filter_by(name=name).first()
        if not command:
            l.error(f"Command {name} not found")
            return response.get_response(response.COMMAND_NOT_FOUND)

        command.host = host
        command.username = username
        command.ssh_key = ssh_key
        command.ssh_port = ssh_port
        command.command = command_param
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} edited Command {name}")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Edit Command",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} edited Command {name}",
            "created_at": int(time.time())
        })
        send_all_message(f"{admin_info['username']} edited Command {name}")

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Edit command failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})


@command_api.route(f'/{const.VERSION_API}/{const.COMMAND_API}/delete', methods=['POST'])
def delete_command():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        name = str(request.json.get("name", ""))

        command = Command.query.filter_by(name=name).first()
        if not command:
            l.error(f"Command {name} not found")
            return response.get_response(response.COMMAND_NOT_FOUND)

        db.session.delete(command)
        db.session.commit()

        l.info(f"Admin: {admin_info['username']} deleted Command {name}")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Delete Command",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} deleted Command {name}",
            "created_at": int(time.time())
        })
        send_all_message(f"{admin_info['username']} deleted Command {name}")

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Delete command failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@command_api.route(f'/{const.VERSION_API}/{const.COMMAND_API}/edit_status', methods=['POST'])
def edit_status_command():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        name = str(request.json.get("name", ""))
        status = int(request.json.get("status", 0))
        status_name = "Enabled" if status == 1 else "Disabled"

        command = Command.query.filter_by(name=name).first()
        if not command:
            l.error(f"Command {name} not found")
            return response.get_response(response.COMMAND_NOT_FOUND)

        command.status = status
        db.session.commit()

        l.info(
            f"Admin: {admin_info['username']} edited Command {name} status")
        save_system_log({
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Edit Command Status",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} edited Command {name} status to {status_name}",
            "created_at": int(time.time())
        })
        send_all_message(
            f"{admin_info['username']} edited Command {name} status to {status_name}")

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Edit Command status failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@command_api.route(f'/{const.VERSION_API}/{const.COMMAND_API}/test', methods=['POST'])
def test_command():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        host = str(request.json.get("host", ""))
        username = str(request.json.get("username", ""))
        ssh_key = str(request.json.get("ssh_key", ""))
        ssh_port = int(request.json.get("ssh_port", 22))

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            key_file = StringIO(ssh_key)
            try:
                private_key = paramiko.Ed25519Key.from_private_key(key_file)
            except paramiko.SSHException:
                key_file.seek(0)
                private_key = paramiko.RSAKey.from_private_key(key_file)

            client.connect(hostname=host, port=ssh_port,
                           username=username, pkey=private_key)

            l.info("SSH connection successful!")

            # Close the connection
            client.close()
        except paramiko.AuthenticationException:
            l.error("Authentication failed, please verify your credentials.")
            return response.get_response(response.SSH_AUTH_ERROR)
        except paramiko.SSHException as sshException:
            l.error(f"Unable to establish SSH connection: {sshException}")
            return response.get_response(response.SSH_CONNECTION_ERROR)
        except Exception as e:
            l.error(f"Exception in connecting to the SSH server: {e}")
            return response.get_response(response.SSH_EXCEPTION)

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Test command failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})


@command_api.route(f'/{const.VERSION_API}/{const.COMMAND_API}/list', methods=['POST'])
def get_list():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        search_name = str(request.json.get("name", ""))
        if search_name != "None":
            commands = Command.query.filter(
                Command.name.like(f"%{search_name}%")).all()
        else:
            commands = Command.query.all()
        command_list = []
        for command in commands:
            command_list.append({
                "id": command.id,
                "name": command.name,
                "host": command.host,
                "username": command.username,
                "ssh_key": command.ssh_key,
                "ssh_port": command.ssh_port,
                "command": command.command,
                "status": command.status,
                "created_at": command.created_at * 1000
            })

        return response.get_response(response.SUCCESS, {"commands": command_list})
    except Exception as e:
        l.error(f"Get command list failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@command_api.route(f'/{const.VERSION_API}/{const.COMMAND_API}/command_list', methods=['POST'])
def get_command_list():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, user_info = check_user_account(token, const.EDITOR)

        if not is_allow:
            l.error(f"User {user_info.get('username')} is not Editor")
            return response.get_response(response.FORBIDDEN)

        search_name = str(request.json.get("name", ""))
        if search_name != "None":
            commands = Command.query.filter(
                Command.name.like(f"%{search_name}%")).filter_by(status=1).all()
        else:
            commands = Command.query.filter_by(status=1).all()
        command_list = []
        for command in commands:
            command_list.append({
                "id": command.id,
                "name": command.name,
                "host": command.host,
                "command": command.command
            })

        return response.get_response(response.SUCCESS, {"commands": command_list})
    except Exception as e:
        l.error(f"Get command list failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@command_api.route(f'/{const.VERSION_API}/{const.COMMAND_API}/execute', methods=['POST'])
def execute():
    try:
        token = str(request.headers.get("D-token"))
        is_allow, user_info = check_user_account(token, const.EDITOR)

        if not is_allow:
            l.error(f"User {user_info.get('username')} is not Editor")
            return response.get_response(response.FORBIDDEN)

        command_id = int(request.json.get("id", 0))
        execute_command = str(request.json.get("command", ""))

        command_details = Command.query.filter_by(id=command_id).first()
        if not command_details:
            l.error(f"Command not found")
            return response.get_response(response.COMMAND_NOT_FOUND)

        host = command_details.host
        username = command_details.username
        ssh_key = command_details.ssh_key
        ssh_port = command_details.ssh_port
        # execute_command = '''curl --request POST '127.0.0.1:9614/blockScan/start' --header 'Content-Type: application/json' --data-raw '{"currencyType":"ftm_scan_block"}' '''
        l.info(f"Execute Command: {execute_command}")

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            key_file = StringIO(ssh_key)
            try:
                private_key = paramiko.Ed25519Key.from_private_key(key_file)
            except paramiko.SSHException:
                key_file.seek(0)
                private_key = paramiko.RSAKey.from_private_key(key_file)

            client.connect(hostname=host, port=ssh_port,
                           username=username, pkey=private_key)

            l.info(f"{user_info.get('username')} Start Execute Command")

            _stdin, stdout, _stderr = client.exec_command(execute_command)
            output = stdout.read().decode("utf-8").strip().split('\n')
            error = _stderr.read().decode("utf-8").strip().split('\n')
            l.info(f"Output: {output}")
            l.info(f"Error: {error}")
            client.close()
        except paramiko.AuthenticationException:
            l.error("Authentication failed, please verify your credentials.")
            return response.get_response(response.SSH_AUTH_ERROR)
        except paramiko.SSHException as sshException:
            l.error(f"Unable to establish SSH connection: {sshException}")
            return response.get_response(response.SSH_CONNECTION_ERROR)
        except Exception as e:
            l.error(f"Exception in connecting to the SSH server: {e}")
            return response.get_response(response.SSH_EXCEPTION)

        system_log_info = {
            "username": user_info["username"],
            "role": user_info["role"],
            "action": "Execute Command",
            "source": "Command",
            "description": f"User: {user_info['username']} execute Command {command_details.name}",
            "created_at": int(time.time())
        }
        save_system_log(system_log_info)
        send_all_message(
            f"{user_info['username']} execute Command {command_details.name}")

        return response.get_response(response.SUCCESS, {"output": output, "error": error, "command": execute_command})

    except Exception as e:
        l.error(f"Get command list failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass
