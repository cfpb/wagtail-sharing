from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from wagtail.models import Site

from wagtailsharing.helpers import (
    get_hostname_and_port_from_request,
    make_root_url,
    parse_host,
)
from wagtailsharing.routers.base import RouterBase


class SettingsHostRouter(RouterBase):
    SETTING = "WAGTAILSHARING_HOST"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not hasattr(settings, self.SETTING):
            raise ImproperlyConfigured(
                f"settings.{self.SETTING} is not defined"
            )

        host_setting = getattr(settings, self.SETTING)

        self.hostname, self.port = parse_host(host_setting)

    def route(self, request, path):
        hostname, port = get_hostname_and_port_from_request(request)

        if (hostname, port) != (self.hostname, self.port):
            return None, path

        return Site.objects.get(is_default_site=True), path

    def get_sharing_url(self, page):
        """Get a sharing URL for a page using the sharing hostname setting."""
        url_parts = self._get_page_url_parts(page)

        if url_parts is None:
            return None

        site_id, root_url, page_path = url_parts

        sharing_root_url = make_root_url(self.hostname, self.port)

        return f"{sharing_root_url}{page_path}"
