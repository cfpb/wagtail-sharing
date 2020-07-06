import re

from django.conf import settings
from django.template import loader
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from wagtail.admin import widgets as wagtailadmin_widgets
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks

from wagtailsharing.helpers import get_sharing_url
from wagtailsharing.models import SharingSite


class SharingSiteModelAdmin(ModelAdmin):
    model = SharingSite
    menu_icon = "site"
    menu_order = 603
    add_to_settings_menu = True
    list_display = ("site", "hostname", "port")


modeladmin_register(SharingSiteModelAdmin)


@hooks.register("register_page_listing_more_buttons")
def add_sharing_link(page, page_perms, is_parent=False):
    sharing_url = get_sharing_url(page)

    if sharing_url:
        yield wagtailadmin_widgets.Button(
            "View sharing link",
            sharing_url,
            attrs={
                "title": _("View shared revision of '{}'").format(
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

    html = force_text(response.content)
    body = re.search(r"(?i)<body.*?>", html)

    if body:
        endpos = body.end()

        banner_template_name = "wagtailsharing/banner.html"
        banner_template = loader.get_template(banner_template_name)

        banner_html = banner_template.render()
        banner_html = force_text(banner_html)

        content_with_banner = html[:endpos] + banner_html + html[endpos:]
        response.content = content_with_banner
