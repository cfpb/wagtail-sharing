from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from . import checks  # noqa F401


class WagtailSharingAppConfig(AppConfig):
    name = "wagtailsharing"
    label = "wagtailsharing"
    verbose_name = _("Wagtail Sharing")
