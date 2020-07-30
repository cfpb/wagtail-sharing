from django.conf import settings
from django.urls import re_path

from wagtail.urls import serve_pattern
from wagtail.urls import urlpatterns as wagtailcore_urlpatterns

from wagtailsharing.views import ServeView, TokenServeView


urlpatterns = [
    re_path(serve_pattern, ServeView.as_view(), name="wagtail_serve")
    if urlpattern.name == "wagtail_serve"
    else urlpattern
    for urlpattern in wagtailcore_urlpatterns
]

if getattr(settings, "WAGTAILSHARING_TOKENIZE_URL", False):
    share_path = getattr(settings, "WAGTAILSHARING_TOKEN_SHARE_PATH", "share")
    urlpatterns = wagtailcore_urlpatterns + [
        re_path(
            rf"^{share_path}/([\w\.\-\_]+)/$",
            TokenServeView.as_view(),
            name="wagtail_serve",
        )
    ]
else:
    urlpatterns = [
        re_path(serve_pattern, ServeView.as_view(), name="wagtail_serve")
        if urlpattern.name == "wagtail_serve"
        else urlpattern
        for urlpattern in wagtailcore_urlpatterns
    ]
