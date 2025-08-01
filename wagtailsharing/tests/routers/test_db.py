from django.test import RequestFactory, TestCase

from wagtail.models import Site

from wagtailsharing.models import SharingSite
from wagtailsharing.routers.db import DatabaseHostRouter
from wagtailsharing.tests.helpers import create_draft_page
from wagtailsharing.tests.shareable_routable_testapp.models import TestPage


class DatabaseHostRouterTests(TestCase):
    def setUp(self):
        self.router = DatabaseHostRouter()
        self.factory = RequestFactory()
        self.default_site = Site.objects.get(is_default_site=True)

    def test_route_with_sharing_site(self):
        SharingSite.objects.create(
            site=self.default_site, hostname="sharing.example.com", port=8080
        )

        request = self.factory.get(
            "/", HTTP_HOST="sharing.example.com", SERVER_PORT=8080
        )
        result = self.router.route(request, "/test/")

        self.assertEqual(result, (self.default_site, "/test/"))

    def test_route_without_sharing_site(self):
        request = self.factory.get(
            "/", HTTP_HOST="nonexistent.com", SERVER_PORT=8080
        )
        result = self.router.route(request, "/test/")

        self.assertEqual(result, (None, "/test/"))

    def test_get_sharing_url_with_sharing_site(self):
        SharingSite.objects.create(
            site=self.default_site, hostname="sharing.example.com", port=8080
        )
        page = create_draft_page(self.default_site, title="test-page")

        result = self.router.get_sharing_url(page)
        self.assertEqual(result, "http://sharing.example.com:8080/test-page/")

    def test_get_sharing_url_without_sharing_site(self):
        page = create_draft_page(self.default_site, title="test-page")

        result = self.router.get_sharing_url(page)
        self.assertIsNone(result)

    def test_get_sharing_url_unroutable_page(self):
        SharingSite.objects.create(
            site=self.default_site, hostname="sharing.example.com", port=8080
        )
        page = TestPage(title="title", slug="slug")

        result = self.router.get_sharing_url(page)
        self.assertIsNone(result)

    def test_get_sharing_url_published_page(self):
        SharingSite.objects.create(
            site=self.default_site, hostname="sharing.example.com", port=8080
        )
        page = create_draft_page(self.default_site, title="published")
        page.save_revision().publish()

        result = self.router.get_sharing_url(page)
        self.assertEqual(result, "http://sharing.example.com:8080/published/")

    def test_get_sharing_url_always_based_on_database_version(self):
        SharingSite.objects.create(
            site=self.default_site, hostname="sharing.example.com", port=8080
        )
        page = create_draft_page(self.default_site, title="initial")

        result = self.router.get_sharing_url(page)
        self.assertEqual(result, "http://sharing.example.com:8080/initial/")

        page.slug = "second"
        page.save_revision()
        result = self.router.get_sharing_url(page)
        self.assertEqual(result, "http://sharing.example.com:8080/initial/")

        page.slug = "third"
        page.save_revision().publish()
        result = self.router.get_sharing_url(page)
        self.assertEqual(result, "http://sharing.example.com:8080/third/")

        page.slug = "fourth"
        page.save_revision()
        result = self.router.get_sharing_url(page)
        self.assertEqual(result, "http://sharing.example.com:8080/third/")
