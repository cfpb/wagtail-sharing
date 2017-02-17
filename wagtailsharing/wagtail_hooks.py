from __future__ import absolute_import, unicode_literals

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from wagtailsharing.models import SharingSite


class SharingSiteModelAdmin(ModelAdmin):
    model = SharingSite
    menu_icon = 'site'
    menu_order = 603
    add_to_settings_menu = True
    list_display = ('wagtail_site', 'hostname', 'port')

modeladmin_register(SharingSiteModelAdmin)
