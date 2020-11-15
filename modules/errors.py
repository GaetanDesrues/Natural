import functools
import requests
from modules.log_file import getLog


class ConnecError(requests.exceptions.ConnectionError):
    def __init__(self, message="Connection Error"):
        super().__init__(message)


class HttpError(requests.HTTPError):
    def __init__(self, error):
        super().__init__(error)


def continuous_error(func):
    @functools.wraps(func)
    def wrapper_continuous_error(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            log.error(e)
            # raise  # DEBUG

    return wrapper_continuous_error


def checkError(e, reason):
    if isinstance(e, HttpError):
        raise HttpError(f"{reason}: {str(e)}")
    elif isinstance(e, ConnecError):
        raise ConnecError(f"{reason}: {str(e)}")
    else:
        raise e


log = getLog(__name__)
