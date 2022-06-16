import logging

from wagtail import VERSION as WAGTAIL_VERSION

import requests

from .models import EmbeddedFormPage
from .settings import wagtail_jotform_settings
from .utils import CantPullFromAPI

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import hooks
else:
    from wagtail.core import hooks


@hooks.register("after_publish_page")
def do_after_publish_page(request, page):
    if not isinstance(page, EmbeddedFormPage) or not page.form:
        return
    thank_you_url = page.full_url + page.specific.reverse_subpage(
        "embedded_form_thank_you"
    )

    params = (("apiKey", wagtail_jotform_settings.API_KEY),)
    form_properties = {
        "activeRedirect": "thankurl",
        "thankurl": f"{thank_you_url}",
    }
    properties = {f"properties[{key}]": form_properties[key] for key in form_properties}

    try:
        requests.post(
            f"{wagtail_jotform_settings.API_URL}/form/{page.form}/properties",
            params=params,
            data=properties,
            timeout=10,
        )
    except Exception as e:
        raise CantPullFromAPI("Cant post") from e
