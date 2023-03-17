from django.conf import settings
from django.urls import include, re_path

from wagtail.admin import urls as wagtailadmin_urls

from wagtailsharing import urls as wagtailsharing_urls


urlpatterns = [
    re_path(r"^admin/", include(wagtailadmin_urls)),
    re_path(r"", include(wagtailsharing_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
