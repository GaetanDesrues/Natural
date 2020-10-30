import requests
import smtplib, ssl
from log_file import getLog, LOG_LEVEL, LOG_FILE
from constants import from_address, password, to_contact, headers

log = getLog(__name__)
log.info(f"This app logs at level logging.{LOG_LEVEL} to file://{LOG_FILE}")

reservation = dict(node="7736", guichets=["14510", "14520", "16456", "17481"], name="Reservation")
sur_reservation = dict(node="18131", guichets=["18826"], name="Sur Reservation")

URL = "https://www.haute-garonne.gouv.fr/booking/create/{}/1"
phrase = "Il n'existe plus de plage horaire libre pour votre demande de rendez-vous. Veuillez recommencer ultérieurement."


def test_all():
    for tp in [reservation, sur_reservation]:
        for p in tp["guichets"]:
            r = make_request(tp["node"], {"planning": p, "nextButton": "Etape+suivante"})
            test_response(r, tp["name"])


def make_request(node, data):
    try:
        # log.info(URL.format(node))
        return requests.post(URL.format(node), headers=headers, data=data)
    except Exception as e:
        log.error(f"Error for {URL.format(node)!r}", e)


def test_response(r, context):
    if r is None:
        return

    if r.status_code == 502:
        log.error(f"Error 502: {r.url}")
        return

    if phrase in r.text:
        log.debug(f"Ok but no rdv dispo ({r.url})")#, r.text)
    else:
        # log.info(r.text)
        make_mail(r.url, context)


def make_mail(url, context):
    msg = f"Un guichet semble etre disponible en {context}, visit {url}"
    log.info(msg)

    message = ''.join(
        'From: Gaga <gaga@example.com>\n'
        'To: <you@example.com>\n'
        'Subject: Bonne nouvelle: un guichet est libre\n'
        '\n'
        f'{msg}\n'
    )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(from_address, password)
        server.sendmail(
            from_address,
            to_contact,
            message,
        )
        log.info("Mail envoye")



if __name__=="__main__":
    test_all()
