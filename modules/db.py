import pyrebase
from modules.constants import db_config
from modules.utils import now


def get_tokens():
    firebase = pyrebase.initialize_app(db_config)
    db = firebase.database()
    tokens_dict = db.child("tokens").get().val()
    tokens = [v for _, v in tokens_dict.items()]
    return tokens


def add_guichet(key, status):
    firebase = pyrebase.initialize_app(db_config)
    db = firebase.database()
    db.child("guichets").child(key).set(status)


if __name__ == "__main__":

    status = dict(res=False, date=now(), reason="Error")
    add_guichet("7736_1234", status)
