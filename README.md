[![CircleCI](https://circleci.com/gh/kevinhowbrook/wagtail-jotform.svg?style=shield&circle)](https://circleci.com/gh/kevinhowbrook/wagtail-jotform)
[![Maintainability](https://api.codeclimate.com/v1/badges/726c28a95738c509885c/maintainability)](https://codeclimate.com/github/kevinhowbrook/wagtail-jotform/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/726c28a95738c509885c/test_coverage)](https://codeclimate.com/github/kevinhowbrook/wagtail-jotform/test_coverage)

# Wagtail Jotform

Embedable [Jotform](https://www.jotform.com) forms for Wagtail pages.

Wagtail Jotform works by providing a new `EmbeddedFormPage` page type with a form choice field. Values for this form field are populated from the Jotform API.

## Installation

Install from [pypi](https://pypi.org/project/wagtail-jotform/):

```
pip install wagtail-jotform
```

## Configuration

You will need an API key from Jotform. Add the following variables to your settings:

```python
WAGTAIL_JOTFORM = {
    "API_KEY": "somekey",
    "API_URL": "https://api.jotform.com",
}
```

If your Jotform account is in [EU safe mode](https://www.jotform.com/eu-safe-forms/), your `JOTFORM_API_URL` should be `https://eu-api.jotform.com`.

Add the following to your `INSTALLED_APPS` in settings, and note that `wagtail_jotform` depends on `routable_page`:

```python
INSTALLED_APPS = [
    ...
    "wagtail_jotform",
    "wagtail.contrib.routable_page",
]
```

## Thank you page

Thank you pages work via Wagtail's [RoutablePageMixin](https://docs.wagtail.io/en/latest/reference/contrib/routablepage.html).

When a form is created, the Jotform `thankurl` is set with your created form's thank you page URL, e.g. `https://mysite.com/formpage/thank-you`. When the form is submitted, the user will be redirected accordingly and be show the 'thank you' data specified on on the form page added.

## Overriding templates

Wagtail Jotform has two templates:

```
embedded_form_page.html
thank_you.html
```

You can override these templates in your project by adding them in the following location:

```
your_project_root/
  templates/
    wagtail_jotform/
        embed_form_page.html
        thank_you.html
```

## Tests

```
coverage run ./runtest.py
coverage report
```
