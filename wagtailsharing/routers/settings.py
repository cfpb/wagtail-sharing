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

        hosts = getattr(settings, self.SETTING)

        if isinstance(hosts, str):
            hosts = hosts.split(",")

        self.hostnames_and_ports = list(map(parse_host, hosts))

    def route(self, request, path):
        hostname, port = get_hostname_and_port_from_request(request)

        for hostname_and_port in self.hostnames_and_ports:
            if (hostname, port) == hostname_and_port:
                return Site.objects.get(is_default_site=True), path

        return None, path

    def get_sharing_url(self, page):
        """Get a sharing URL for a page using the sharing hostname setting."""
        url_parts = self._get_page_url_parts(page)

        if url_parts is None:
            return None

        site_id, root_url, page_path = url_parts

        sharing_root_url = make_root_url(*(self.hostnames_and_ports[0]))

        return f"{sharing_root_url}{page_path}"
