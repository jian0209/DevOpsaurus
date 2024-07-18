import time
from flask import Blueprint, request
from const import response
from log import logger as l
import const.const as const
from utils.credential import check_admin_account
from model.db_init import db
from utils.logs import save_system_log
from model.system_integration import SystemIntegration
from utils.message import send_email, send_slack, send_telegram


setting_api = Blueprint('setting_api', __name__)


@setting_api.route(f'/{const.VERSION_API}/{const.SETTING_API}/init', methods=['POST'])
def init_setting():
    try:
        system_integration = SystemIntegration.query.first()
        if system_integration is None:
            system_integration = SystemIntegration(
                id=1,
                is_email_allow=0,
                is_telegram_allow=0,
                is_slack_allow=0,
                email_smtp_server=None,
                email_smtp_port=None,
                email_smtp_username=None,
                email_smtp_password=None,
                email_from=None,
                email_helo=None,
                email_allow_ssl_tls=None,
                email_allow_start_tls=None,
                telegram_bot_token=None,
                telegram_chat_id=None,
                telegram_parse=None,
                slack_bot_token=None,
                slack_channel=None,
                slack_token=None
            )
            db.session.add(system_integration)
            db.session.commit()

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Init Integration failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})


@setting_api.route(f'/{const.VERSION_API}/{const.SETTING_API}/get/<page>', methods=['POST'])
def get_setting(page: str):
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        system_integration = SystemIntegration.query.first()
        if page == "integration":
            return response.get_response(response.SUCCESS, {
                "email": system_integration.is_email_allow,
                "telegram": system_integration.is_telegram_allow,
                "slack": system_integration.is_slack_allow
            })
        elif page == "email":
            return response.get_response(response.SUCCESS, {
                "smtp_server": system_integration.email_smtp_server,
                "smtp_port": system_integration.email_smtp_port,
                "smtp_username": system_integration.email_smtp_username,
                "smtp_password": system_integration.email_smtp_password,
                "email_from": system_integration.email_from,
                "email_helo": system_integration.email_helo,
                "email_allow_ssl_tls": system_integration.email_allow_ssl_tls,
                "email_allow_start_tls": system_integration.email_allow_start_tls
            })
        elif page == "telegram":
            return response.get_response(response.SUCCESS, {
                "bot_token": system_integration.telegram_bot_token,
                "chat_id": system_integration.telegram_chat_id,
                "parse": system_integration.telegram_parse if system_integration.telegram_parse else 0
            })
        elif page == "slack":
            return response.get_response(response.SUCCESS, {
                "bot_token": system_integration.slack_bot_token,
                "channel": system_integration.slack_channel,
                "token": system_integration.slack_token
            })
        else:
            return response.get_response(response.BAD_REQUEST)
    except Exception as e:
        l.error(f"Get Integration failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@setting_api.route(f'/{const.VERSION_API}/{const.SETTING_API}/save/<page>', methods=['POST'])
def save_integration(page: str):
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        system_integration = SystemIntegration.query.first()

        if page == "integration":
            email = int(request.json.get("email", 0))
            telegram = int(request.json.get("telegram", 0))
            slack = int(request.json.get("slack", 0))

            system_integration.is_email_allow = email
            system_integration.is_telegram_allow = telegram
            system_integration.is_slack_allow = slack

        elif page == "email":
            smtp_server = str(request.json.get("smtp_server", ""))
            smtp_port = int(request.json.get("smtp_port", 0))
            smtp_username = str(request.json.get("smtp_username", ""))
            smtp_password = str(request.json.get("smtp_password", ""))
            email_from = str(request.json.get("email_from", ""))
            email_helo = str(request.json.get("email_helo", ""))
            email_allow_ssl_tls = int(
                request.json.get("email_allow_ssl_tls", 0))
            email_allow_start_tls = int(
                request.json.get("email_allow_start_tls", 0))

            system_integration.email_smtp_server = smtp_server
            system_integration.email_smtp_port = smtp_port
            system_integration.email_smtp_username = smtp_username
            system_integration.email_smtp_password = smtp_password
            system_integration.email_from = email_from
            system_integration.email_helo = email_helo
            system_integration.email_allow_ssl_tls = email_allow_ssl_tls
            system_integration.email_allow_start_tls = email_allow_start_tls

        elif page == "telegram":
            bot_token = str(request.json.get("bot_token", ""))
            chat_id = str(request.json.get("chat_id", ""))
            parse = int(request.json.get("parse", 0))

            system_integration.telegram_bot_token = bot_token
            system_integration.telegram_chat_id = chat_id
            system_integration.telegram_parse = parse

        elif page == "slack":
            bot_token = str(request.json.get("bot_token", ""))
            channel = str(request.json.get("channel", ""))
            token = str(request.json.get("token", ""))

            system_integration.slack_bot_token = bot_token
            system_integration.slack_channel = channel
            system_integration.slack_token = token

        db.session.commit()

        system_log_info = {
            "username": admin_info["username"],
            "role": admin_info["role"],
            "action": "Save Integration",
            "source": "Settings",
            "description": f"Admin: {admin_info['username']} saved new {page}",
            "created_at": int(time.time())
        }
        save_system_log(system_log_info)

        return response.get_response(response.SUCCESS)
    except Exception as e:
        l.error(f"Save Integration failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass


@setting_api.route(f'/{const.VERSION_API}/{const.SETTING_API}/test/<page>', methods=['POST'])
def test_integration(page):
    try:
        token = str(request.headers.get("D-token"))
        is_allow, admin_info = check_admin_account(token)

        if not is_allow:
            l.error(f"Admin {admin_info.get('username')} is not admin")
            return response.get_response(response.FORBIDDEN)

        if page == "email":
            smtp_server = str(request.json.get("smtp_server", ""))
            smtp_port = int(request.json.get("smtp_port", 0))
            smtp_username = str(request.json.get("smtp_username", ""))
            smtp_password = str(request.json.get("smtp_password", ""))
            email_from = str(request.json.get("email_from", ""))
            email_to = str(request.json.get("email_to", ""))
            email_helo = str(request.json.get("email_helo", ""))
            email_allow_ssl_tls = int(
                request.json.get("email_allow_ssl_tls", 0))
            email_allow_start_tls = int(
                request.json.get("email_allow_start_tls", 0))

            send_email(server=smtp_server,
                       port=smtp_port, username=smtp_username, password=smtp_password, email_from=email_from, email_helo=email_helo, email_to=email_to, subject="Test Email", body="This is a test email from DevOpsaurus.", ssl_tls=email_allow_ssl_tls, start_tls=email_allow_start_tls)
            return response.get_response(response.SUCCESS)
        elif page == "telegram":
            bot_token = str(request.json.get("bot_token", ""))
            chat_id = str(request.json.get("chat_id", ""))
            parse = int(request.json.get("markdown", 0))

            send_telegram(bot_token=bot_token, chat_id=chat_id,
                          parse=parse, message="This is a test message from DevOpsaurus.")
            return response.get_response(response.SUCCESS)
        elif page == "slack":
            bot_token = str(request.json.get("bot_token", ""))
            channel = str(request.json.get("channel", ""))
            token = str(request.json.get("token", ""))

            send_slack(bot_token=bot_token, channel=channel,
                       token=token, message="This is a test message from DevOpsaurus.")
            return response.get_response(response.SUCCESS)
        else:
            return response.get_response(response.BAD_REQUEST)

    except Exception as e:
        l.error(f"Test Integration failed: {str(e)}")
        return response.get_response(response.SYSTEM_INTERNAL_EXCEPTION, {"msg": str(e)})
    finally:
        pass
