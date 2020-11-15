from pyfcm import FCMNotification
from modules.db import get_tokens
from modules.constants import API_KEY


def send_notif(message_title, message_body):
    push_service = FCMNotification(api_key=API_KEY)
    # registration_ids = get_tokens()
    registration_ids = [
        "cs34A8A8QGm4kjPbQClEkW:APA91bFBhWGaoXwR0167EI0bir1Mq3hkz4--n7tc7blZgS-5HR0PXeB6JiyhzHwauN8Fya-t-PUgJgiK4CrpTjWpB5k34ZAmIk7hN3_DppIPiPlFF7QeQJXjimcvN1w04N5Zwqr8_J_U"
    ]

    result = push_service.notify_multiple_devices(
        registration_ids=registration_ids,
        message_title=message_title,
        message_body=message_body,
    )

    return result
