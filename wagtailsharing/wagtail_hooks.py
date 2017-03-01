from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin import widgets as wagtailadmin_widgets
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.wagtailcore import hooks

from wagtailsharing.helpers import get_sharing_url
from wagtailsharing.models import SharingSite


class SharingSiteModelAdmin(ModelAdmin):
    model = SharingSite
    menu_icon = 'site'
    menu_order = 603
    add_to_settings_menu = True
    list_display = ('site', 'hostname', 'port')


modeladmin_register(SharingSiteModelAdmin)


@hooks.register('register_page_listing_more_buttons')
def add_sharing_link(page, page_perms, is_parent=False):
    sharing_url = get_sharing_url(page)

    if sharing_url:
        if hasattr(page, 'get_admin_display_title'):
            title = page.get_admin_display_title()
        else:
            title = page.title

        yield wagtailadmin_widgets.Button(
            'View sharing link',
            sharing_url,
            attrs={
                'title': _("View shared revision of '{}'").format(title),
            },
            priority=90
        )
