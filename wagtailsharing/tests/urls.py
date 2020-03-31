from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from wagtailsharing import urls as wagtailsharing_urls


try:
    from wagtail.admin import urls as wagtailadmin_urls
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0
    from wagtail.wagtailadmin import urls as wagtailadmin_urls


urlpatterns = [
    url(r"^admin/", include(wagtailadmin_urls)),
    url(r"", include(wagtailsharing_urls)),
]
