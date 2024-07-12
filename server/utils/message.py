import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from log import logger as l
import requests
from model.system_integration import SystemIntegration


def send_email(server: str, port: int, username: str, password: str, email_from: str, email_helo: str, email_to: str, subject: str, body: str, ssl_tls: bool = False, start_tls: bool = False):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = formataddr((email_helo, email_from))
    msg['To'] = email_to
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    try:
        if ssl_tls:
            # Create SSL connection
            server = smtplib.SMTP_SSL(server, port)
        else:
            # Create non-SSL connection
            server = smtplib.SMTP(server, port)

        # Start TLS if required
        if start_tls and not ssl_tls:
            server.starttls()

        # Login to the server
        server.login(username, password)

        # Send the email
        server.sendmail(email_from, email_to, msg.as_string())

        # Quit the server
        server.quit()

        l.info(f"Email sent successfully to {email_to}")
    except Exception as e:
        l.error(f"Failed to send email. Error: {e}")


def send_telegram(bot_token: str, chat_id: str, parse: bool, message: str):
    if parse:
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=markdown'
    else:
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
    requests.post(url=url, headers={
                  'Content-Type': 'application/json;charset=utf-8'})


def send_slack(bot_token: str, channel: str, token: str, message: str):
    url = f'https://hooks.slack.com/services/{bot_token}/{channel}/{token}'
    data = {
        "text": message
    }
    requests.post(url=url, json=data, headers={
                  'Content-Type': 'application/json;charset=utf-8'})


def send_all_message(message: str, email_to: str = None):
    system_integration = SystemIntegration.query.filter_by().first()

    is_send_email = system_integration.is_email_allow
    is_send_telegram = system_integration.is_telegram_allow
    is_send_slack = system_integration.is_slack_allow

    if is_send_email and email_to is not None:
        send_email(server=system_integration.email_smtp_server,
                   port=system_integration.email_smtp_port, username=system_integration.email_smtp_username, password=system_integration.email_smtp_password, email_from=system_integration.email_from, email_helo=system_integration.email_helo, email_to=email_to, subject="DevOpsaurus Notification", body=message, ssl_tls=system_integration.email_allow_ssl_tls, start_tls=system_integration.email_allow_start_tls)

    if is_send_telegram and email_to is None:
        send_telegram(bot_token=system_integration.telegram_bot_token, chat_id=system_integration.telegram_chat_id,
                      parse=system_integration.telegram_parse, message=message)

    if is_send_slack and email_to is None:
        send_slack(bot_token=system_integration.slack_bot_token, channel=system_integration.slack_channel,
                   token=system_integration.slack_token, message=message)
