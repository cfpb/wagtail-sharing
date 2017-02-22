from django.db import IntegrityError
from django.test import RequestFactory, TestCase
from wagtail.wagtailcore.models import Site

from wagtailsharing.models import SharingSite


class TestSharingSite(TestCase):
    def setUp(self):
        self.default_site = Site.objects.get(is_default_site=True)
        self.factory = RequestFactory()

    def create(self, **kwargs):
        return SharingSite.objects.create(site=self.default_site, **kwargs)

    def test_can_create(self):
        self.create(hostname='hostname', port=8000)

    def test_site_related_name_default_empty(self):
        with self.assertRaises(SharingSite.DoesNotExist):
            self.default_site.sharing_site

    def test_site_related_name(self):
        self.create(hostname='hostname', port=8000)
        self.assertIsNotNone(self.default_site.sharing_site)

    def test_str(self):
        site = self.create(hostname='hostname', port=8000)
        self.assertEqual(str(site), 'hostname:8000')

    def test_str_no_port(self):
        site = self.create(hostname='hostname')
        self.assertEqual(str(site), 'hostname')

    def test_uniqueness(self):
        self.create(hostname='hostname', port=1234)
        with self.assertRaises(IntegrityError):
            self.create(hostname='hostname', port=1234)

    def test_multiple_sharing_sites_not_allowed(self):
        self.create(hostname='hostname', port=1234)
        with self.assertRaises(IntegrityError):
            self.create(hostname='otherhost', port=5678)

    def test_find_for_request(self):
        sharing_site = self.create(hostname='hostname', port=1234)
        request = self.factory.get('/', HTTP_HOST='hostname', SERVER_PORT=1234)
        self.assertEqual(SharingSite.find_for_request(request), sharing_site)

    def test_find_for_request_no_sites(self):
        request = self.factory.get('/', HTTP_HOST='hostname', SERVER_PORT=1234)
        with self.assertRaises(SharingSite.DoesNotExist):
            SharingSite.find_for_request(request)

    def test_find_for_request_wrong_port(self):
        self.create(hostname='hostname', port=1234)
        request = self.factory.get('/', HTTP_HOST='hostname', SERVER_PORT=5678)
        with self.assertRaises(SharingSite.DoesNotExist):
            SharingSite.find_for_request(request)

    def test_find_for_request_hostname_keyerror(self):
        request = self.factory.get('/', SERVER_PORT=5678)
        del request.META['SERVER_NAME']

        with self.assertRaises(SharingSite.DoesNotExist):
            SharingSite.find_for_request(request)

    def test_root_url_port_80_http_no_port(self):
        site = SharingSite(hostname='test.hostname', port=80)
        self.assertEqual(site.root_url, 'http://test.hostname')

    def test_root_url_port_443_https(self):
        site = SharingSite(hostname='test.hostname', port=443)
        self.assertEqual(site.root_url, 'https://test.hostname')

    def test_root_url_other_port_http(self):
        site = SharingSite(hostname='test.hostname', port=1234)
        self.assertEqual(site.root_url, 'http://test.hostname:1234')
