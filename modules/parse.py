from bs4 import BeautifulSoup
from modules.db import now, add_guichet, get_last_valid
from modules.guichet import RES, SRES, Guichet
from modules.log_file import getLog
from modules.utils import make_request, make_notif
from modules.errors import (
    continuous_error,
    HttpError,
    checkError,
)


def on_success(guichet):
    guichet.update(dict(res=True, last_valid=now(), date=now(), reason="Found one!"))
    make_notif(guichet)
    add_guichet(guichet)


def on_failure(guichet, reason):
    if isinstance(reason, HttpError):
        reason = "Server Error"
    guichet.update(dict(res=False, date=now(), reason=str(reason)))
    add_guichet(guichet)


class GouvParser:
    def __init__(self):
        self.parse_guichets()

        for guichet in self.guichets:
            self.parse_page_guichet(guichet)

    @continuous_error
    def parse_guichets(self):
        self.guichets, label, soup = [], None, None
        last_valids = get_last_valid()

        for dtype in [RES, SRES]:
            try:
                soup = safe_get_soup(dtype.get(1))
            except Exception as e:
                checkError(e, "No guichets")
            lines = soup.findAll("p", {"class": "Bligne"})

            label = "Guichet unique" if dtype is SRES else None
            for line in lines:
                if dtype is RES:
                    label = decode(line.find("label").text)

                g = Guichet(
                    dtype=dtype, planning=line.find("input").get("value"), label=label,
                )
                if last_valids is not None:
                    g.update(dict(last_valid=last_valids[f"{g.node}_{g.planning}"]))
                self.guichets.append(g)

    @continuous_error
    def parse_page_guichet(self, guichet):
        planning, label = guichet.planning, guichet.label
        soup = None
        try:
            soup = safe_get_soup(
                guichet.url,
                data={"planning": planning, "nextButton": "Etape+suivante"},
            )
        except Exception as e:
            on_failure(guichet, e)
            checkError(e, guichet.label)

        title = decode(soup.find(id="inner_Booking").find("h2").text)
        msg = decode(soup.find(id="FormBookingCreate").text)

        if title == RES.title and msg == RES.msg:
            log.warning(f"{label}: Checked but nope")
            on_failure(guichet, "Checked but nope")
        else:
            log.info(f"{label}: Found one!")
            log.info(f"title: {title}")
            log.info(f"msg: {msg}")
            on_success(guichet)


def safe_get_soup(url, data=None):
    r = make_request(url, data)

    soup = BeautifulSoup(r.text, "lxml")

    if r.status_code != 200:
        raise HttpError(f"{r.status_code} {r.reason}")

    return soup


def decode(html):
    return html.strip()


log = getLog(__name__)
