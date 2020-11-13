from modules.db import add_guichet
from modules.log_file import getLog, LOG_LEVEL, LOG_FILE
from modules.parse import GouvParser
from modules.utils import make_request, test_response, make_mail, make_notif, now

log = getLog(__name__)
# log.info(f"This app logs at level logging.{LOG_LEVEL} to file://{LOG_FILE}")

# reservation = dict(
#     node="7736", guichets=["14510", "14520", "16456", "17481"], name="Reservation"
# )
# sur_reservation = dict(node="18131", guichets=["18826"], name="Sur Reservation")
#
#
# def test_all():
#     for tp in [reservation, sur_reservation]:
#         for p in tp["guichets"]:
#             r = make_request(
#                 tp["node"], {"planning": p, "nextButton": "Etape+suivante"}
#             )
#             test_response(r, tp["name"])
#
#
# def test_one():
#     r = make_request("7736", {"planning": 14510, "nextButton": "Etape+suivante"})
#     test_response(r, "Test_REservation")


if __name__ == "__main__":
    # make_mail({"label": "info"}, "Reservation")

    # test_all()
    # test_one()

    def on_success(dtype, infos):
        make_mail(infos, dtype.name)
        # make_notif(infos, dtype)

        status = dict(res=True, date=now(), reason=infos["label"], name=dtype.name)
        add_guichet(f"{dtype.node}_{infos['value']}", status=status)

    def on_failure(dtype, infos, reason):
        status = dict(res=False, date=now(), reason=str(reason), name=dtype.name)
        add_guichet(f"{dtype.node}_{infos['value']}", status=status)

    pp = GouvParser(on_success=on_success, on_failure=on_failure)
