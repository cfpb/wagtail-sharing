from django.db import IntegrityError
from django.test import RequestFactory, TestCase

from wagtail.models import Site

from wagtailsharing.models import SharingSite
from wagtailsharing.tests.shareable_routable_testapp.models import (
    RoutableTestPage,
    ShareableRoutableTestPage,
)


class TestSharingSite(TestCase):
    def setUp(self):
        self.default_site = Site.objects.get(is_default_site=True)
        self.factory = RequestFactory()

    def create(self, **kwargs):
        return SharingSite.objects.create(site=self.default_site, **kwargs)

    def test_can_create(self):
        self.create(hostname="hostname", port=8000)

    def test_site_related_name_default_empty(self):
        with self.assertRaises(SharingSite.DoesNotExist):
            self.default_site.sharing_site

    def test_site_related_name(self):
        self.create(hostname="hostname", port=8000)
        self.assertIsNotNone(self.default_site.sharing_site)

    def test_str(self):
        site = self.create(hostname="hostname", port=8000)
        self.assertEqual(str(site), "hostname:8000")

    def test_str_no_port(self):
        site = self.create(hostname="hostname")
        self.assertEqual(str(site), "hostname")

    def test_uniqueness(self):
        self.create(hostname="hostname", port=1234)
        with self.assertRaises(IntegrityError):
            self.create(hostname="hostname", port=1234)

    def test_multiple_sharing_sites_not_allowed(self):
        self.create(hostname="hostname", port=1234)
        with self.assertRaises(IntegrityError):
            self.create(hostname="otherhost", port=5678)

    def test_find_for_request(self):
        sharing_site = self.create(hostname="hostname", port=1234)
        request = self.factory.get("/", HTTP_HOST="hostname", SERVER_PORT=1234)
        self.assertEqual(SharingSite.find_for_request(request), sharing_site)

    def test_find_for_request_no_sites(self):
        request = self.factory.get("/", HTTP_HOST="hostname", SERVER_PORT=1234)
        with self.assertRaises(SharingSite.DoesNotExist):
            SharingSite.find_for_request(request)

    def test_find_for_request_wrong_port(self):
        self.create(hostname="hostname", port=1234)
        request = self.factory.get("/", HTTP_HOST="hostname", SERVER_PORT=5678)
        with self.assertRaises(SharingSite.DoesNotExist):
            SharingSite.find_for_request(request)

    def test_find_for_request_hostname_keyerror(self):
        request = self.factory.get("/", SERVER_PORT=5678)
        del request.META["SERVER_NAME"]

        with self.assertRaises(SharingSite.DoesNotExist):
            SharingSite.find_for_request(request)

    def test_find_for_request_no_server_port(self):
        request = self.factory.get("/")
        del request.META["SERVER_PORT"]

        with self.assertRaises(SharingSite.DoesNotExist):
            SharingSite.find_for_request(request)

    def test_root_url_port_80_http_no_port(self):
        site = SharingSite(hostname="test.hostname", port=80)
        self.assertEqual(site.root_url, "http://test.hostname")

    def test_root_url_port_443_https(self):
        site = SharingSite(hostname="test.hostname", port=443)
        self.assertEqual(site.root_url, "https://test.hostname")

    def test_root_url_other_port_http(self):
        site = SharingSite(hostname="test.hostname", port=1234)
        self.assertEqual(site.root_url, "http://test.hostname:1234")


class TestShareableRoutablePage(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.default_site = Site.objects.get(is_default_site=True)
        self.sharing_site = SharingSite.objects.create(
            site=self.default_site,
            hostname="sharinghostname",
            port=1234,
        )

        self.root_page = self.default_site.root_page
        self.routable_page = RoutableTestPage(
            title="Routable page", text="Published text", live=True
        )

        self.shareable_routable_page = ShareableRoutableTestPage(
            title="Shareable routable page", text="Published text", live=True
        )

        self.root_page.add_child(instance=self.routable_page)
        self.routable_page.text = "Draft text"
        self.draft_revision = self.routable_page.save_revision()

        self.root_page.add_child(instance=self.shareable_routable_page)
        self.shareable_routable_page.text = "Shareable draft text"
        self.draft_revision = self.shareable_routable_page.save_revision()

    def test_route_not_sharing(self):
        plain_response = self.client.get("/routable-page/")
        self.assertContains(plain_response, "Published text")

        shareable_response = self.client.get("/shareable-routable-page/")
        self.assertContains(shareable_response, "Published text")

    def test_route_with_sharing(self):
        # Request from the sharing site
        plain_response = self.client.get(
            "/routable-page/",
            HTTP_HOST="sharinghostname",
            SERVER_PORT=1234,
        )
        self.assertContains(plain_response, "Published text")

        shareable_response = self.client.get(
            "/shareable-routable-page/",
            HTTP_HOST="sharinghostname",
            SERVER_PORT=1234,
        )
        self.assertContains(shareable_response, "Shareable draft text")
