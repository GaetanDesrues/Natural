import requests
from bs4 import BeautifulSoup

from modules.log_file import getLog
from modules.utils import (
    make_request,
    BadGateway502,
    NoneSoup,
    continuous_error,
    HttpError,
)

DEBUG = 0


class BRes:
    BASE_URL = "https://www.haute-garonne.gouv.fr/booking/create/{node}/{page}"
    title = "Vérification de disponibilité"
    msg = "Il n'existe plus de plage horaire libre pour votre demande de rendez-vous. Veuillez recommencer ultérieurement."

    def __init__(self, name, node):
        self.name, self.node = name, node

    def get(self, p):
        return BRes.BASE_URL.format(node=self.node, page=p)


RES = BRes("Reservation", 7736)
SRES = BRes("Sur Reservation", 18131)


class GouvParser:
    def __init__(self, on_success, on_failure):
        self.on_success = on_success
        self.on_failure = on_failure

        self.parse_guichets()
        self.parse_surreservation()

        for infos in self.infos_guichets:
            self.parse_page_guichet(infos)

        for infos in self.infos_surreservation:
            self.parse_page_surreservation(infos)

    @continuous_error
    def parse_guichets(self):
        self.infos_guichets = []
        soup = safe_get_soup("No guichets right now", RES.get(1), "_guichets")

        lines = soup.findAll("p", {"class": "Bligne"})

        for line in lines:
            self.infos_guichets.append(
                dict(
                    value=line.find("input").get("value"),
                    label=decode(line.find("label").text),
                )
            )

    @continuous_error
    def parse_surreservation(self):
        self.infos_surreservation = []
        soup = safe_get_soup(
            "No surreservation right now", SRES.get(1), "_surreservation"
        )

        lines = soup.findAll("p", {"class": "Bligne"})

        for line in lines:
            self.infos_surreservation.append(
                dict(
                    value=line.find("input").get("value"),
                    label="Guichet unique",  # decode(line.find("label").text)
                )
            )

    @continuous_error
    def parse_page_guichet(self, infos):
        value, label = infos.get("value"), infos.get("label")

        try:
            soup = safe_get_soup(
                label,
                RES.get(1),
                f"_guichet_{value}",
                data={"planning": value, "nextButton": "Etape+suivante"},
            )
        except Exception as e:
            self.on_failure(RES, infos, e)
            raise e

        title = decode(soup.find(id="inner_Booking").find("h2").text)
        msg = decode(soup.find(id="FormBookingCreate").text)

        if title == RES.title and msg == RES.msg:
            log.warning(f"{label} -- Checked but nope")
            self.on_failure(RES, infos, f"{label} -- Checked but nope")
        else:
            log.info(f"{label} -- Found one!")
            self.on_success(RES, infos)

    @continuous_error
    def parse_page_surreservation(self, infos):
        value, label = infos.get("value"), infos.get("label")

        try:
            soup = safe_get_soup(
                label,
                SRES.get(1),
                f"_surreservation_{value}",
                data={"planning": value, "nextButton": "Etape+suivante"},
            )
        except Exception as e:
            self.on_failure(RES, infos, e)
            raise e

        title = decode(soup.find(id="inner_Booking").find("h2").text)
        msg = decode(soup.find(id="FormBookingCreate").text)

        if title == SRES.title and msg == SRES.msg:
            log.warning(f"{label} -- Checked but nope")
            self.on_failure(SRES, infos, f"{label} -- Checked but nope")
        else:
            log.info(f"{label} -- Found one!")
            self.on_success(SRES, infos)


def safe_get_soup(label, url, n, data=None):
    r = make_request(url, data, label=label)

    soup = BeautifulSoup(r.text, "lxml")

    if soup is None:
        raise NoneSoup(label)

    if r.status_code != 200:
        raise HttpError(f"{r.status_code} {r.reason}", label)

    return soup


# def get_page(url, n, data=None, download=not DEBUG):
#     # if download:
#     req = make_request(url, data)
#     # with open(f"data/page{n}.html", "w") as f:
#     #     f.write(req.text)
#     # with open(f"data/page{n}.html", "r") as f:
#     #     te = f.read()
#     return req


def decode(html):
    return html.strip()


log = getLog(__name__)

# if __name__ == "__main__":
#
#     def on_success(dtype, infos):
#         print(f"{dtype}: {infos}")
#
#     pp = GouvParser(on_success=on_success)
