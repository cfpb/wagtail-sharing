from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from wagtailsharing.routers import get_router


class WagtailSharingAppConfig(AppConfig):
    name = "wagtailsharing"
    label = "wagtailsharing"
    verbose_name = _("Wagtail Sharing")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        get_router()
