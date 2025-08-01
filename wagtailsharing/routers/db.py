from wagtail.models import Site
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from wagtailsharing.models import SharingSite
from wagtailsharing.routers import get_router_cls
from wagtailsharing.routers.base import RouterBase


class DatabaseHostRouter(RouterBase):
    def route(self, request, path):
        try:
            sharing_site = SharingSite.find_for_request(request)
        except SharingSite.DoesNotExist:
            return None, path

        return sharing_site.site, path

    def get_sharing_url(self, page):
        """Get a sharing URL for a page, if available."""
        url_parts = self._get_page_url_parts(page)

        if url_parts is None:
            return None

        site_id, root_url, page_path = url_parts

        site = Site.objects.get(id=site_id)

        try:
            sharing_site = site.sharing_site
        except SharingSite.DoesNotExist:
            return None

        return sharing_site.root_url + page_path


if get_router_cls() == ".".join(
    [DatabaseHostRouter.__module__, DatabaseHostRouter.__qualname__]
):

    class SharingSiteViewSet(SnippetViewSet):
        model = SharingSite
        icon = "site"
        menu_order = 603
        add_to_settings_menu = True
        list_display = ("site", "hostname", "port")

    register_snippet(SharingSiteViewSet)
