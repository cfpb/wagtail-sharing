from django.apps import apps
from django.core.checks import Error
from django.test import SimpleTestCase, override_settings

from wagtailsharing.checks import modeladmin_installed_check


class TestModelAdminInstalledCheck(SimpleTestCase):
    @override_settings(
        INSTALLED_APPS=["wagtail.contrib.modeladmin", "wagtailsharing"]
    )
    def test_check_passes_if_modeladmin_installed(self):
        self.assertFalse(modeladmin_installed_check(apps.get_app_configs()))

    @override_settings(INSTALLED_APPS=["wagtailsharing"])
    def test_check_fails_if_modeladmin_not_installed(self):
        errors = modeladmin_installed_check(apps.get_app_configs())
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], Error)
        self.assertEqual(errors[0].id, "wagtailsharing.E001")
