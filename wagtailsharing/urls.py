from wagtail.core.urls import (
    serve_pattern,
    urlpatterns as wagtailcore_urlpatterns,
)

from wagtailsharing.views import ServeView


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


urlpatterns = [
    re_path(serve_pattern, ServeView.as_view(), name="wagtail_serve")
    if urlpattern.name == "wagtail_serve"
    else urlpattern
    for urlpattern in wagtailcore_urlpatterns
]
