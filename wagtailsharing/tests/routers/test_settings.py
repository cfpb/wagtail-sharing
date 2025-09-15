from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory, TestCase, override_settings

from wagtail.models import Site

from wagtailsharing.routers.settings import SettingsHostRouter
from wagtailsharing.tests.helpers import create_draft_page
from wagtailsharing.tests.shareable_routable_testapp.models import TestPage


@override_settings(WAGTAILSHARING_HOST="https://sharing.example.com")
class SettingsHostRouterTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_sharing_hostnames(self):
        self.assertEqual(
            SettingsHostRouter().hostnames_and_ports,
            [("sharing.example.com", 443)],
        )

    def test_get_sharing_hostname_not_configured(self):
        with override_settings():
            del settings.WAGTAILSHARING_HOST
            with self.assertRaises(ImproperlyConfigured):
                SettingsHostRouter()

    def test_route_matching_hostname(self):
        request = self.factory.get(
            "/", HTTP_HOST="sharing.example.com", SERVER_PORT="443"
        )
        result = SettingsHostRouter().route(request, "/test/")

        default_site = Site.objects.get(is_default_site=True)
        self.assertEqual(result, (default_site, "/test/"))

    def test_route_non_matching_hostname(self):
        request = self.factory.get("/", HTTP_HOST="other.example.com")
        result = SettingsHostRouter().route(request, "/test/")

        self.assertEqual(result, (None, "/test/"))

    def test_get_sharing_url_with_setting(self):
        default_site = Site.objects.get(is_default_site=True)
        page = create_draft_page(default_site, title="test-page")

        result = SettingsHostRouter().get_sharing_url(page)
        self.assertEqual(result, "https://sharing.example.com/test-page/")

    def test_get_sharing_url_unroutable_page(self):
        page = TestPage(title="title", slug="slug")

        result = SettingsHostRouter().get_sharing_url(page)
        self.assertIsNone(result)

    def test_get_sharing_url_published_page(self):
        default_site = Site.objects.get(is_default_site=True)
        page = create_draft_page(default_site, title="published")
        page.save_revision().publish()

        result = SettingsHostRouter().get_sharing_url(page)
        self.assertEqual(result, "https://sharing.example.com/published/")

    def test_get_sharing_url_always_based_on_database_version(self):
        default_site = Site.objects.get(is_default_site=True)
        page = create_draft_page(default_site, title="initial")

        result = SettingsHostRouter().get_sharing_url(page)
        self.assertEqual(result, "https://sharing.example.com/initial/")

        page.slug = "second"
        page.save_revision()
        result = SettingsHostRouter().get_sharing_url(page)
        self.assertEqual(result, "https://sharing.example.com/initial/")

        page.slug = "third"
        page.save_revision().publish()
        result = SettingsHostRouter().get_sharing_url(page)
        self.assertEqual(result, "https://sharing.example.com/third/")

        page.slug = "fourth"
        page.save_revision()
        result = SettingsHostRouter().get_sharing_url(page)
        self.assertEqual(result, "https://sharing.example.com/third/")


@override_settings(
    WAGTAILSHARING_HOST=[
        "https://sharing.example.com",
        "http://sharing2.example.com:8080",
    ]
)
class MultipleHostsSettingsRouterTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_sharing_hostnames(self):
        self.assertEqual(
            SettingsHostRouter().hostnames_and_ports,
            [("sharing.example.com", 443), ("sharing2.example.com", 8080)],
        )

    @override_settings(
        WAGTAILSHARING_HOST="http://foo.com:8000,http://bar.com:8081"
    )
    def test_sharing_hostnames_string(self):
        self.assertEqual(
            SettingsHostRouter().hostnames_and_ports,
            [("foo.com", 8000), ("bar.com", 8081)],
        )

    def test_route_matching_hosts(self):
        for host, port in [
            ("sharing.example.com", "443"),
            ("sharing2.example.com", "8080"),
        ]:
            request = self.factory.get("/", HTTP_HOST=host, SERVER_PORT=port)
            result = SettingsHostRouter().route(request, "/test/")

            default_site = Site.objects.get(is_default_site=True)
            self.assertEqual(result, (default_site, "/test/"))

    def test_route_non_matching_hostname(self):
        request = self.factory.get("/", HTTP_HOST="other.example.com")
        result = SettingsHostRouter().route(request, "/test/")

        self.assertEqual(result, (None, "/test/"))

    def test_get_sharing_url_uses_first_host(self):
        default_site = Site.objects.get(is_default_site=True)
        page = create_draft_page(default_site, title="test-page")

        result = SettingsHostRouter().get_sharing_url(page)
        self.assertEqual(result, "https://sharing.example.com/test-page/")
