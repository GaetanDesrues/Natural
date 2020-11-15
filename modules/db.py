import pyrebase
from datetime import datetime
from modules.constants import db_config


def get_tokens():
    firebase = pyrebase.initialize_app(db_config)
    db = firebase.database()
    tokens_dict = db.child("tokens").get().val()
    tokens = [v for _, v in tokens_dict.items()]
    return tokens


def get_last_valid():
    firebase = pyrebase.initialize_app(db_config)
    db = firebase.database()
    last_valid_dict = db.child("guichets").get().val()
    if last_valid_dict is None:
        return
    last_valids = dict()
    for k, v in last_valid_dict.items():
        last_valids[k] = v.get("last_valid")
    return last_valids


def add_guichet(guichet):
    firebase = pyrebase.initialize_app(db_config)
    db = firebase.database()
    guichet.pop("url")
    key = f"{guichet.node}_{guichet.planning}"
    db.child("guichets").child(key).set(guichet)


def now():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


if __name__ == "__main__":
    pass
