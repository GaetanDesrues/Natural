import smtplib
import ssl
from datetime import datetime

import requests
from .constants import from_address, password, to_contact, headers
from .log_file import getLog

URL = "https://www.haute-garonne.gouv.fr/booking/create/{}/1"
phrase = "Il n'existe plus de plage horaire libre pour votre demande de rendez-vous. Veuillez recommencer ultérieurement."


def make_request(url, data, label=None):
    try:
        return requests.post(url, headers=headers, data=data)
    except requests.exceptions.ConnectionError:
        raise ConnecError(label, url)
        # log.error(f"ConnectionError for {url!r}")


def test_response(r, context):
    if r is None:
        # log.error(f"Internal python error")
        return

    if r.status_code == 502:
        log.error(f"Error 502: {r.url}")
        return

    elif r.status_code == 503:
        log.error(f"Error 503: {r.url}")
        return

    elif phrase in r.text:
        log.debug(f"Ok but no rdv dispo ({r.url})")  # , r.text)

    else:
        log.critical(r.text)
        make_mail(r.url, context)
        make_notif(r.url, context)


def make_mail(url, context):
    msg = f"Un guichet semble etre disponible en {context}, visit {url}"
    log.info(msg)

    message = "".join(
        "From: Gaga <gaga@example.com>\n"
        "To: <you@example.com>\n"
        "Subject: Bonne nouvelle: un guichet est libre\n"
        "\n"
        f"{msg}\n"
    )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(from_address, password)
        server.sendmail(
            from_address, to_contact, message,
        )
        log.info("Mail envoye")


def make_notif(url, context):
    title = f"{context}: un guichet semble libre"
    msg = f"Un guichet semble etre disponible en {context}"
    print(msg)

    # r = send_notif(title, msg)

    # log.info(f"Notification sent: {r}")


class BadGateway502(Exception):
    def __init__(
        self,
        label=None,
        message="BadGateway502: The server returned an invalid or incomplete response.",
    ):
        self.message = message
        if label is not None:
            self.message = f"{label} -- {self.message}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class ConnecError(requests.exceptions.ConnectionError):
    def __init__(self, label, url, message="ConnectionError"):
        self.url = url
        self.message = f"{label} -- {message}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"  # {self.url!r}."


class NoneSoup(Exception):
    def __init__(self, label=None, message="NoneSoup: Soup is None"):
        self.message = message
        if label is not None:
            self.message = f"{label} -- {self.message}"
        super().__init__(self.message)


class HttpError(requests.HTTPError):
    def __init__(self, code, label=""):
        self.m = f"{label} -- {code}"
        super().__init__(self.m)


import functools


def continuous_error(func):
    @functools.wraps(func)
    def wrapper_continuous_error(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            log.error(e)

    return wrapper_continuous_error


def now():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


log = getLog(__name__)
