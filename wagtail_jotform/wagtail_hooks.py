from wagtail.core import hooks

import requests

from .models import EmbeddedFormPage
from .settings import wagtail_jotform_settings


@hooks.register("after_publish_page")
def do_after_publish_page(request, page):
    if isinstance(page, EmbeddedFormPage) and page.form:
        thank_you_url = page.full_url + page.specific.reverse_subpage(
            "embedded_form_thank_you"
        )

        params = (("apiKey", wagtail_jotform_settings.API_KEY),)
        form_properties = {
            "activeRedirect": "thankurl",
            "thankurl": f"{thank_you_url}",
        }
        properties = {}
        for key in form_properties:
            properties["properties[" + key + "]"] = form_properties[key]

        requests.post(
            f"{wagtail_jotform_settings.API_URL}/form/{page.form}/properties",
            params=params,
            data=properties,
        )
