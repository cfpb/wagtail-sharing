from __future__ import absolute_import, unicode_literals

from django.db import IntegrityError
from django.http import Http404
from django.test import RequestFactory, TestCase, override_settings

try:
    from wagtail.core.models import Site
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0
    from wagtail.wagtailcore.models import Site

from wagtailsharing.models import SharingSite
from wagtailsharing.tests.sharingtestapp.models import (
    ShareableRoutablePageModel
)


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

    def test_find_for_request_no_server_port(self):
        request = self.factory.get('/')
        del request.META['SERVER_PORT']

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


class TestShareableRoutablePageMixin(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.default_site = Site.objects.get(is_default_site=True)
        self.home_page = self.default_site.root_page
        self.routable_page = self.home_page.add_child(
            instance=ShareableRoutablePageModel(
                title="Routable Page",
                live=False,
            )
        )

    def test_route_on_sharing_site(self):
        SharingSite.objects.create(
            site=self.default_site, hostname='hostname', port=1234
        )
        request = self.factory.get(
            self.routable_page.url + 'subpage-url/',
            HTTP_HOST='hostname',
            SERVER_PORT=1234
        )
        route_result = self.routable_page.route(request, ['subpage-url'])
        self.assertEqual(route_result.page, self.routable_page)
        self.assertEqual(route_result.args[0], self.routable_page.subpage_url)

    @override_settings(APPEND_SLASH=False)
    def test_route_on_sharing_site_no_append_slash(self):
        SharingSite.objects.create(
            site=self.default_site, hostname='hostname', port=1234
        )
        request = self.factory.get(
            self.routable_page.url + 'subpage-url-without-slash',
            HTTP_HOST='hostname',
            SERVER_PORT=1234
        )
        route_result = self.routable_page.route(
            request, ['subpage-url-without-slash']
        )
        self.assertEqual(route_result.page, self.routable_page)
        self.assertEqual(
            route_result.args[0],
            self.routable_page.subpage_url_without_slash
        )

    def test_route_on_sharing_site_no_route(self):
        SharingSite.objects.create(
            site=self.default_site, hostname='hostname', port=1234
        )
        request = self.factory.get(
            self.routable_page.url + 'not-a-subpage-url/',
            HTTP_HOST='hostname',
            SERVER_PORT=1234
        )
        with self.assertRaises(Http404):
            self.routable_page.route(request, ['not-a-subpage-url'])

    def test_route_not_on_sharing_site(self):
        SharingSite.objects.create(
            site=self.default_site, hostname='test.hostname', port=1234
        )
        request = self.factory.get(
            self.routable_page.url + 'subpage-url/',
            HTTP_HOST='hostname',
            SERVER_PORT=1234
        )
        with self.assertRaises(Http404):
            self.routable_page.route(request, ['subpage-url'])

    def test_published_routable_page(self):
        self.routable_page.live = True
        self.routable_page.save()
        SharingSite.objects.create(
            site=self.default_site, hostname='test.hostname', port=1234
        )
        request = self.factory.get(
            self.routable_page.url + 'subpage-url/',
            HTTP_HOST='hostname',
            SERVER_PORT=1234
        )
        route_result = self.routable_page.route(request, ['subpage-url'])
        self.assertEqual(route_result.page, self.routable_page)
        self.assertEqual(route_result.args[0], self.routable_page.subpage_url)
