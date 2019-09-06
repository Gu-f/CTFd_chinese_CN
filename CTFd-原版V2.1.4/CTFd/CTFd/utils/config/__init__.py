from flask import current_app as app
from CTFd.utils import get_config
from CTFd.utils.modes import USERS_MODE, TEAMS_MODE
import time
import os


def ctf_name():
    name = get_config("ctf_name")
    return name if name else "CTFd"


def user_mode():
    return get_config("user_mode")


def is_users_mode():
    return user_mode() == USERS_MODE


def is_teams_mode():
    return user_mode() == TEAMS_MODE


def ctf_logo():
    return get_config("ctf_logo")


def ctf_theme():
    theme = get_config("ctf_theme")
    return theme if theme else ""


def is_setup():
    return get_config("setup")


def is_scoreboard_frozen():
    freeze = get_config("freeze")

    if freeze:
        freeze = int(freeze)
        if freeze < time.time():
            return True

    return False


def can_send_mail():
    return mailserver() or mailgun()


def get_mail_provider():
    if app.config.get("MAIL_SERVER") and app.config.get("MAIL_PORT"):
        return "smtp"
    if get_config("mail_server") and get_config("mail_port"):
        return "smtp"
    if app.config.get("MAILGUN_API_KEY") and app.config.get("MAILGUN_BASE_URL"):
        return "mailgun"
    if get_config("mailgun_api_key") and get_config("mailgun_base_url"):
        return "mailgun"


def mailgun():
    if app.config.get("MAILGUN_API_KEY") and app.config.get("MAILGUN_BASE_URL"):
        return True
    if get_config("mailgun_api_key") and get_config("mailgun_base_url"):
        return True
    return False


def mailserver():
    if app.config.get("MAIL_SERVER") and app.config.get("MAIL_PORT"):
        return True
    if get_config("mail_server") and get_config("mail_port"):
        return True
    return False


def get_themes():
    dir = os.path.join(app.root_path, "themes")
    return [
        name
        for name in os.listdir(dir)
        if os.path.isdir(os.path.join(dir, name)) and name != "admin"
    ]
