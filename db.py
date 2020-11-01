import pyrebase
from constants import db_config


def get_tokens():
    firebase = pyrebase.initialize_app(db_config)

    db = firebase.database()
    tokens_dict = db.get().val()["tokens"]
    tokens = [v for _, v in tokens_dict.items()]

    return tokens
