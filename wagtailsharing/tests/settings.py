import os

from wagtail import VERSION as WAGTAIL_VERSION


ALLOWED_HOSTS = ["*"]

SECRET_KEY = "not needed"

ROOT_URLCONF = "wagtailsharing.tests.urls"

DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "DATABASE_ENGINE", "django.db.backends.sqlite3"
        ),
        "NAME": os.environ.get("DATABASE_NAME", "wagtailsharing.sqlite"),
        "USER": os.environ.get("DATABASE_USER", None),
        "PASSWORD": os.environ.get("DATABASE_PASS", None),
        "HOST": os.environ.get("DATABASE_HOST", None),
        "TEST": {"NAME": os.environ.get("DATABASE_NAME", None)},
    },
}


WAGTAIL_APPS = (
    "wagtail.contrib.forms",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.settings",
    "wagtail.test.routablepage" if WAGTAIL_VERSION >= (3, 0) else "wagtail.tests.routablepage",
    "wagtail.test.testapp" if WAGTAIL_VERSION >= (3, 0) else "wagtail.tests.testapp",
    "wagtail.admin",
    "wagtail" if WAGTAIL_VERSION >= (3, 0) else "wagtail.core",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.sites",
    "wagtail.users",
)

if WAGTAIL_VERSION >= (3, 0):
    WAGTAILADMIN_RICH_TEXT_EDITORS = {
        "default": {"WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea"},
        "custom": {"WIDGET": "wagtail.test.testapp.rich_text.CustomRichTextArea"},
    }
else:
    WAGTAILADMIN_RICH_TEXT_EDITORS = {
        "default": {"WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea"},
        "custom": {"WIDGET": "wagtail.tests.testapp.rich_text.CustomRichTextArea"},
    }

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

INSTALLED_APPS = (
    (
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.messages",
        "django.contrib.sessions",
        "django.contrib.staticfiles",
        "taggit",
    )
    + WAGTAIL_APPS
    + ("wagtailsharing", "wagtailsharing.tests.shareable_routable_testapp")
)

STATIC_URL = "/static/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
            "debug": True,
        },
    },
]

WAGTAIL_SITE_NAME = "Test Site"
