from django.db import models
from django.forms.widgets import Select
from django.shortcuts import render

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from .settings import wagtail_jotform_settings
from .utils import JotFormAPI


def jot_form_choices():
    jot_form_data = []
    if wagtail_jotform_settings.API_URL and wagtail_jotform_settings.API_KEY:
        jotform = JotFormAPI()
        jotform.fetch_from_api()
        data = jotform.get_data()
        if "content" in data:
            for item in data["content"]:
                jot_form_data.append((item["id"], item["title"]))
    return jot_form_data


class EmbeddedFormPageAdminForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["form"].widget.choices = jot_form_choices()


class EmbeddedFormPage(RoutablePageMixin, Page):

    base_form_class = EmbeddedFormPageAdminForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        jot_form_choices()

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
