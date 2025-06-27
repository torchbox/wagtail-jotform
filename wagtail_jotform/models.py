from django.core.cache import cache
from django.db import models
from django.forms.widgets import Select
from django.shortcuts import render

from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import RichTextField
from wagtail.models import Page

from .settings import wagtail_jotform_settings
from .utils import JotFormAPI


CHOICES_CACHE_KEY = "jot_form_choices"


def jot_form_choices():
    # Use a `None` check to allow empty choices to still be cached
    if (form_choices := cache.get(CHOICES_CACHE_KEY)) is None:

        form_choices = []
        if wagtail_jotform_settings.API_URL and wagtail_jotform_settings.API_KEY:
            jotform = JotFormAPI()
            jotform.fetch_from_api()
            data = jotform.get_data()
            if "content" in data:
                for item in data["content"]:
                    form_choices.append((item["id"], item["title"]))

        cache.set(CHOICES_CACHE_KEY, form_choices, timeout=300)

    return form_choices


class EmbeddedFormPageAdminForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["form"].widget.choices = jot_form_choices()


class EmbeddedFormPage(RoutablePageMixin, Page):

    base_form_class = EmbeddedFormPageAdminForm

    thank_you_template = "wagtail_jotform/thank_you.html"
    subpage_types = []

    introduction = models.TextField(blank=True)
    form = models.CharField(max_length=1000)
    thank_you_text = RichTextField(
        blank=True,
        help_text="Text displayed to the user on successful submission of the form",
    )

    @route(r"^thank-you/$", name="embedded_form_thank_you")
    def thank_you_page(self, request, *args, **kwargs):
        return render(request, self.thank_you_template, {"page": self})

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("form", widget=Select(choices=[])),
        FieldPanel("thank_you_text"),
    ]
