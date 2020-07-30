from django.conf import settings
from django.conf.urls import url

from wagtail.core.urls import (
    serve_pattern,
    urlpatterns as wagtailcore_urlpatterns,
)
from wagtailsharing.views import ServeView, TokenServeView


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


if getattr(settings, "WAGTAILSHARING_TOKENIZE_URL", True):
    urlpatterns = [
        url(
            r"^share/([\w\.\-\_]+)/$",
            TokenServeView.as_view(),
            name="wagtail_serve",
        ),
    ]
else:
    urlpatterns = [
        re_path(serve_pattern, ServeView.as_view(), name="wagtail_serve")
        if urlpattern.name == "wagtail_serve"
        else urlpattern
        for urlpattern in wagtailcore_urlpatterns
    ]
