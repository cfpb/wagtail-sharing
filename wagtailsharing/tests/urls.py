from django.conf.urls import include, url

from wagtail.admin import urls as wagtailadmin_urls
from wagtailsharing import urls as wagtailsharing_urls


urlpatterns = [
    url(r"^admin/", include(wagtailadmin_urls)),
    url(r"", include(wagtailsharing_urls)),
]
