from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShareableRoutableTestAppConfig(AppConfig):
    name = "wagtailsharing.tests.shareable_routable_testapp"
    label = "test_shareable_routable_testapp"
    verbose_name = _("Shareable-Routable Page Tests")
