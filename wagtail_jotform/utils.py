import logging

import requests
from requests.exceptions import ConnectionError, HTTPError, MissingSchema, Timeout

from .settings import wagtail_jotform_settings

logger = logging.getLogger(__name__)


class CantPullFromAPI(Exception):
    pass


def fetch_data(url, headers=None, **params):
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
    except Timeout:
        logger.exception(f"Timeout error occurred when fetching data from {url}")
        raise CantPullFromAPI(f"Error occured when fetching data from {url}")
    except (HTTPError, ConnectionError):
        logger.exception(f"HTTP/ConnectionError occured when fetching data from {url}")
        raise CantPullFromAPI(f"Error occured when fetching data from {url}")
    except MissingSchema as e:
        logger.exception(f"HTTP/ConnectionError occured when fetching data: {e}")
        raise CantPullFromAPI(f"Error occured when fetching data from {url}")
    except Exception:
        logger.exception(f"Exception occured when fetching data from {url}")
        raise CantPullFromAPI(f"Error occured when fetching data from {url}")
    else:
        return response.json()


def fetch_jotform_data():

    headers = {"APIKEY": wagtail_jotform_settings.API_KEY}
    url = f"{wagtail_jotform_settings.API_URL}/user/forms"

    return fetch_data(url, headers)


class _BaseContentAPI:
    def __init__(self, func):
        self.func = func

    def fetch_from_api(self):
        try:
            data = self.func()
        except CantPullFromAPI:
            pass
        else:
            return data

    def get_data(self):
        data = self.fetch_from_api()
        if data is not None:
            return data
        return {}


class JotFormAPI(_BaseContentAPI):
    def __init__(self):
        super().__init__(fetch_jotform_data)


def parse_jotform_data(data):
    return data
