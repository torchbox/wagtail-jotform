from django.conf import settings

DEFAULTS = {}


class WagtailJotFormSettings:
    def __getattr__(self, attr):
        django_settings = getattr(settings, "WAGTAIL_JOTFORM", {})

        try:
            # Check if present in user settings
            return django_settings[attr]
        except KeyError:
            return getattr(DEFAULTS, attr, None)


wagtail_jotform_settings = WagtailJotFormSettings()
