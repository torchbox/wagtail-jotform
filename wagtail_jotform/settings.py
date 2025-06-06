from django.conf import settings

DEFAULTS = {"LIMIT": 50}  # Default limit for JotForm API requests


class WagtailJotFormSettings:
    def __getattr__(self, attr):
        django_settings = getattr(settings, "WAGTAIL_JOTFORM", {})

        try:
            # Check if present in user settings
            return django_settings[attr]
        except (KeyError, AttributeError):
            # Use the DEFAULTS dictionary directly
            return DEFAULTS.get(attr)


wagtail_jotform_settings = WagtailJotFormSettings()
