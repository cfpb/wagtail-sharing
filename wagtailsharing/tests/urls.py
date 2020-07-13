from wagtail.admin import urls as wagtailadmin_urls

from wagtailsharing import urls as wagtailsharing_urls


try:
    from django.urls import include, re_path
except ImportError:
    from django.conf.urls import include, url as re_path


urlpatterns = [
    re_path(r"^admin/", include(wagtailadmin_urls)),
    re_path(r"", include(wagtailsharing_urls)),
]
