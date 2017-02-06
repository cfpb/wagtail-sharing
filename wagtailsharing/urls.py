from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from wagtail.wagtailcore.urls import (
    serve_pattern, urlpatterns as wagtailcore_urlpatterns
)

from wagtailsharing.views import ServeView


urlpatterns = [
    url(serve_pattern, ServeView.as_view(), name='wagtail_serve')
    if urlpattern.name == 'wagtail_serve' else urlpattern
    for urlpattern in wagtailcore_urlpatterns
]
