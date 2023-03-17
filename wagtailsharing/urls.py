from django.urls import re_path

from wagtail.urls import serve_pattern
from wagtail.urls import urlpatterns as wagtailcore_urlpatterns

from wagtailsharing.views import ServeView


urlpatterns = [
    re_path(serve_pattern, ServeView.as_view(), name="wagtail_serve")
    if urlpattern.name == "wagtail_serve"
    else urlpattern
    for urlpattern in wagtailcore_urlpatterns
]
