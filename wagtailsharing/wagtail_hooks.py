import re

from django.conf import settings
from django.template import loader
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from wagtail import hooks
from wagtail.admin import widgets as wagtailadmin_widgets
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from wagtailsharing.helpers import get_sharing_url
from wagtailsharing.models import SharingSite


class SharingSiteViewSet(SnippetViewSet):
    model = SharingSite
    icon = "site"
    menu_order = 603
    add_to_settings_menu = True
    list_display = ("site", "hostname", "port")


register_snippet(SharingSiteViewSet)


@hooks.register("register_page_header_buttons")
@hooks.register("register_page_listing_more_buttons")
def add_sharing_link(page, user, next_url=None, **kwargs):
    sharing_url = get_sharing_url(page)

    if sharing_url:
        yield wagtailadmin_widgets.Button(
            "View sharing link",
            sharing_url,
            icon_name="draft",
            attrs={
                "aria-label": _("View shared revision of '{}'").format(
                    page.get_admin_display_title()
                ),
            },
            priority=90,
        )


@hooks.register("after_serve_shared_page")
def add_sharing_banner(page, response):
    if not getattr(settings, "WAGTAILSHARING_BANNER", True):
        return

    if hasattr(response, "render") and callable(response.render):
        response.render()

    html = force_str(response.content)
    body = re.search(r"(?is)<body.*?>", html)

    if body:
        endpos = body.end()

        banner_template_name = "wagtailsharing/banner.html"
        banner_template = loader.get_template(banner_template_name)

        banner_html = banner_template.render()
        banner_html = force_str(banner_html)

        content_with_banner = html[:endpos] + banner_html + html[endpos:]
        response.content = content_with_banner


@hooks.register("before_route_page")
def set_routed_by_wagtail_sharing(request, path):
    request.routed_by_wagtail_sharing = True


@hooks.register("before_serve_shared_page")
def set_served_by_wagtail_sharing(page, request, args, kwargs):
    request.served_by_wagtail_sharing = True
