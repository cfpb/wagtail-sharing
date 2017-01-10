from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from wagtail.wagtailcore.urls import (
    serve_pattern, urlpatterns as wagtailcore_urlpatterns
)

from wagtailsharing import views


urlpatterns = [
    url(serve_pattern, views.serve, name='wagtail_serve')
    if urlpattern.name == 'wagtail_serve' else urlpattern
    for urlpattern in wagtailcore_urlpatterns
]
