import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


SECRET_KEY = "not so secret"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}

INSTALLED_APPS = [
    "wagtail.contrib.styleguide",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.frontend_cache",
    "wagtail.contrib.settings",
    "wagtail.contrib.table_block",
    "wagtail.contrib.forms",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.admin",
    "wagtail.images",
    "wagtail",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    # Add your app here
    "wagtail_jotform.tests.testapp",
    "wagtail_jotform",
]


MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.legacy.sitemiddleware.SiteMiddleware",
]

ROOT_URLCONF = "wagtail_jotform.tests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": ["wagtail_jotform/templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

WAGTAIL_SITE_NAME = "Wagtail Form Embeds"
USE_TZ = True

WAGTAIL_JOTFORM = {
    "API_KEY": "somekey",
    "API_URL": "https://wagtail-jotform.com",
    "LIMIT": 50,
}

WAGTAILADMIN_BASE_URL = "http://localhost:8000"

STATIC_URL = "/static/"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
