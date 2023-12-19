import os


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

DEBUG = True

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
    "wagtail.contrib.routable_page",
    "wagtail.contrib.settings",
    "wagtail.test.routablepage",
    "wagtail.admin",
    "wagtail",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.sites",
    "wagtail.snippets",
    "wagtail.users",
)

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

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

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

WAGTAILADMIN_BASE_URL = "http://localhost:8000"
