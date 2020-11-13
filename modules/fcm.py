from pyfcm import FCMNotification
from .db import get_tokens
from .constants import API_KEY


def send_notif(message_title, message_body):
    push_service = FCMNotification(api_key=API_KEY)
    registration_ids = get_tokens()

    result = push_service.notify_multiple_devices(
        registration_ids=registration_ids,
        message_title=message_title,
        message_body=message_body,
    )

    return result
