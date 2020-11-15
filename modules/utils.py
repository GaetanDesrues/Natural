import requests
from modules.constants import headers
from modules.errors import ConnecError
from modules.fcm import send_notif
from modules.log_file import getLog


def make_request(url, data):
    try:
        return requests.post(url, headers=headers, data=data)
    except requests.exceptions.ConnectionError:
        raise ConnecError()


def make_notif(guichet):
    title = f"{guichet.name}: {guichet.label.lower()}"
    msg = f"{guichet.label}: {guichet.reason.lower()}"

    r = send_notif(title, msg)
    log.info(f"Notification sent: {r}")


log = getLog(__name__)
