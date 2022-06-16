from unittest import mock

from django.conf import settings
from django.test import TestCase

from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.models import Page, Site
else:
    from wagtail.core.models import Page, Site

from requests.exceptions import Timeout

from ..models import EmbeddedFormPage
from ..settings import wagtail_jotform_settings
from ..utils import CantPullFromAPI, JotFormAPI
from ..wagtail_hooks import do_after_publish_page


class TestThankYouHook(TestCase):
    fixtures = ["test.json"]

    def setUp(self):
        self.default_site = Site.objects.get(is_default_site=True)
        self.homepage = Page.objects.get(url_path="/home/")
        self.embedded_form_page = self.homepage.add_child(
            instance=EmbeddedFormPage(
                title="Embedded Form Page", depth=3, slug="embeded-form-page", form="1"
            )
        )

    def test_bad_jotform_url_value(self):
        # The requests.post method here should fail if the jotform url
        # isn't valid
        with self.assertRaises(CantPullFromAPI):
            do_after_publish_page(request=None, page=self.embedded_form_page)

    def test_bad_page_instance(self):
        r = do_after_publish_page(request=None, page=self.homepage)
        self.assertEqual(r, None)


def mocked_fetch_data(url=None, headers=None, **params):
    return {
        "responseCode": 200,
        "message": "success",
        "content": [
            {
                "id": "202722038345045",
                "username": "Howbrook",
                "title": "An email form",
                "height": "539",
                "status": "ENABLED",
                "created_at": "2020-09-29 04:04:05",
                "updated_at": "2020-10-10 10:34:12",
                "last_submission": "2020-10-07 09:13:12",
                "new": "2",
                "count": "2",
                "type": "LEGACY",
                "url": "https://form.jotform.com/202722038345045",
            },
            {
                "id": "202721468649058",
                "username": "Howbrook",
                "title": "Name Form",
                "height": "539",
                "status": "ENABLED",
                "created_at": "2020-09-29 03:45:31",
                "updated_at": "2020-10-07 06:52:10",
                "last_submission": "2020-09-29 03:47:54",
                "new": "2",
                "count": "2",
                "type": "LEGACY",
                "url": "https://form.jotform.com/202721468649058",
            },
        ],
        "duration": "14ms",
        "resultSet": {"offset": 0, "limit": 20, "count": 2},
        "limit-left": 978,
    }


class TestUtils(TestCase):
    fixtures = ["test.json"]

    def setUp(self):
        self.expected_api_data = {
            "responseCode": 200,
            "message": "success",
            "content": [
                {
                    "id": "202722038345045",
                    "username": "Howbrook",
                    "title": "An email form",
                    "height": "539",
                    "status": "ENABLED",
                    "created_at": "2020-09-29 04:04:05",
                    "updated_at": "2020-10-10 10:34:12",
                    "last_submission": "2020-10-07 09:13:12",
                    "new": "2",
                    "count": "2",
                    "type": "LEGACY",
                    "url": "https://form.jotform.com/202722038345045",
                },
                {
                    "id": "202721468649058",
                    "username": "Howbrook",
                    "title": "Name Form",
                    "height": "539",
                    "status": "ENABLED",
                    "created_at": "2020-09-29 03:45:31",
                    "updated_at": "2020-10-07 06:52:10",
                    "last_submission": "2020-09-29 03:47:54",
                    "new": "2",
                    "count": "2",
                    "type": "LEGACY",
                    "url": "https://form.jotform.com/202721468649058",
                },
            ],
            "duration": "14ms",
            "resultSet": {"offset": 0, "limit": 20, "count": 2},
            "limit-left": 978,
        }

        self.default_site = Site.objects.get(is_default_site=True)
        self.homepage = Page.objects.get(url_path="/home/")
        self.embedded_form_page = self.homepage.add_child(
            instance=EmbeddedFormPage(
                title="Embedded Form Page", depth=3, slug="embeded-form-page", form="1"
            )
        )

    @mock.patch("wagtail_jotform.utils.fetch_data", side_effect=mocked_fetch_data)
    def test_fetch(self, mocked_fetch_data):
        # Test mocked data from jotform
        jotform = JotFormAPI()
        jotform.fetch_from_api()
        data = jotform.get_data()
        self.assertEqual(data, self.expected_api_data)

    @mock.patch("wagtail_jotform.utils.requests.get")
    @mock.patch("wagtail_jotform.utils.fetch_data", side_effect=mocked_fetch_data)
    def test_exceptions(self, mock_get, mocked_fetch_data):
        mock_get.side_effect = Timeout
        mock_get.raise_for_status.side_effect = Timeout
        with self.assertRaises(Timeout):
            jotform = JotFormAPI()
            jotform.fetch_from_api()


class TestSettings(TestCase):
    fixtures = ["test.json"]

    def setUp(self):
        self.default_site = Site.objects.get(is_default_site=True)
        self.homepage = Page.objects.get(url_path="/home/")
        self.embedded_form_page = self.homepage.add_child(
            instance=EmbeddedFormPage(
                title="Embedded Form Page", depth=3, slug="embeded-form-page", form="1"
            )
        )

    def test_settings(self):
        del settings.WAGTAIL_JOTFORM
        self.assertFalse(wagtail_jotform_settings.API_KEY)
        self.assertFalse(wagtail_jotform_settings.API_URL)
        self.assertFalse(wagtail_jotform_settings.LIMIT)

    def test_page_renders_with_bad_settings(self):
        response = self.client.get("/embeded-form-page/")
        self.assertTemplateUsed(response, "wagtail_jotform/embedded_form_page.html")
        self.assertEqual(response.render().status_code, 200)
