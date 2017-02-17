from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from wagtail.wagtailadmin import urls as wagtailadmin_urls

from wagtailsharing import urls as wagtailsharing_urls


urlpatterns = [
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'', include(wagtailsharing_urls)),
]
