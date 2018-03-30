from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

try:
    from wagtail.core.urls import (
        serve_pattern, urlpatterns as wagtailcore_urlpatterns
    )
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0
    from wagtail.wagtailcore.urls import (
        serve_pattern, urlpatterns as wagtailcore_urlpatterns
    )

from wagtailsharing.views import ServeView


urlpatterns = [
    url(serve_pattern, ServeView.as_view(), name='wagtail_serve')
    if urlpattern.name == 'wagtail_serve' else urlpattern
    for urlpattern in wagtailcore_urlpatterns
]
