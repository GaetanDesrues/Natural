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


class Guichet(dict):
    def __init__(self, dtype, label, **kwargs):
        super().__init__(**kwargs)
        self.update(
            dict(
                url=dtype.get(1),
                name=dtype.name,
                node=dtype.node,
                label=label.replace(" (Haute-Garonne)", ""),
            )
        )

    def __getattr__(self, item):
        return self.get(item)
