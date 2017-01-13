from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from wagtailsharing import urls as wagtailsharing_urls


urlpatterns = [
    url(r'', include(wagtailsharing_urls)),
]
