from django.apps import apps
from django.core.checks import Error, register

from wagtail import VERSION as WAGTAIL_VERSION


if WAGTAIL_VERSION <= (5, 0):

    @register()
    def modeladmin_installed_check(app_configs, **kwargs):
        errors = []

        MODELADMIN_APP = "wagtail.contrib.modeladmin"
        if not apps.is_installed(MODELADMIN_APP):
            error_hint = "Is '{}' in settings.INSTALLED_APPS?".format(
                MODELADMIN_APP
            )

            errors.append(
                Error(
                    "wagtail-sharing requires the Wagtail ModelAdmin app.",
                    hint=error_hint,
                    id="wagtailsharing.E001",
                )
            )

        return errors
