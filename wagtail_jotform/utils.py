import logging

import requests
from requests.exceptions import ConnectionError, HTTPError, MissingSchema, Timeout
from urllib3.exceptions import MaxRetryError

from .settings import wagtail_jotform_settings

logging.basicConfig(level=logging.CRITICAL)
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
    except MaxRetryError:
        logger.exception(f"MaxRetryError occured when fetching data from {url}")
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
    limit = getattr(wagtail_jotform_settings, "LIMIT", 50)
    api_url = getattr(wagtail_jotform_settings, "API_URL", "")
    api_key = getattr(wagtail_jotform_settings, "API_KEY", "")

    # Check if API_URL is set
    if not api_url:
        logger.error("API_URL is not set in settings.")
        return None
    # Check if API_URL starts with http
    if not api_url.startswith("http"):
        logger.error("API_URL must start with http or https.")
        return None
    # Check if API_KEY is set
    if not api_key:
        logger.error("API_KEY is not set in settings.")
        return None

    return fetch_data(f"{api_url}/user/forms?limit={limit}", {"APIKEY": api_key})


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
