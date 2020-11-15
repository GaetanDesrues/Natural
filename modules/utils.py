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
    # print(title, msg)

    r = send_notif(title, msg)
    log.info(f"Notification sent: {r}")


# def make_mail(url, context):
#     msg = f"Un guichet semble etre disponible en {context}, visit {url}"
#     log.info(msg)
#
#     message = "".join(
#         "From: Gaga <gaga@example.com>\n"
#         "To: <you@example.com>\n"
#         "Subject: Bonne nouvelle: un guichet est libre\n"
#         "\n"
#         f"{msg}\n"
#     )
#
#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#         server.login(from_address, password)
#         server.sendmail(
#             from_address, to_contact, message,
#         )
#         log.info("Mail envoye")


log = getLog(__name__)
