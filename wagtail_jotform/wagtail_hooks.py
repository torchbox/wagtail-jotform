from django.conf import settings

from wagtail.core import hooks

import requests

from .models import EmbededFormPage


@hooks.register("after_publish_page")
def do_after_publish_page(request, page):
    if isinstance(page, EmbededFormPage) and page.form:
        thank_you_url = page.full_url + page.specific.reverse_subpage(
            "embeded_form_thank_you"
        )

        params = (("apiKey", settings.JOTFORM_API_KEY),)
        form_properties = {
            "activeRedirect": "thankurl",
            "thankurl": f"{thank_you_url}",
        }
        properties = {}
        for key in form_properties:
            properties["properties[" + key + "]"] = form_properties[key]

        requests.post(
            f"{settings.JOTFORM_API_URL}/form/{page.form}/properties",
            params=params,
            data=properties,
        )
