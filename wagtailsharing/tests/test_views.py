from __future__ import absolute_import, unicode_literals

from django.http import Http404, HttpResponse
from django.test import RequestFactory, TestCase
from mock import patch

from wagtail.tests.utils import WagtailTestUtils
from wagtail.wagtailcore.models import Site

from wagtailsharing.models import SharingSite
from wagtailsharing.tests.helpers import create_draft_page
from wagtailsharing.views import ServeView


def before_serve_page(page, request, args, kwargs):
    return HttpResponse('before serve page hook')


def before_serve_shared_page(page, request, args, kwargs):
    page.title = 'hook changed title'


def after_serve_shared_page(page, response):
    response['test-hook-header'] = 'foo'


class TestServeView(WagtailTestUtils, TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.default_site = Site.objects.get(is_default_site=True)

    def make_request(self, path, method='get', **kwargs):
        request = getattr(self.factory, method)(path, **kwargs)
        request.site = self.default_site
        return request

    def create_sharing_site(self, hostname):
        SharingSite.objects.create(
            site=self.default_site,
            hostname=hostname
        )

    def assert_title_matches(self, response, title):
        self.assertContains(response, title)

    def test_no_sharing_site_exists_uses_wagtail_serve(self):
        request = self.make_request('/')
        with patch('wagtailsharing.views.wagtail_serve') as wagtail_serve:
            ServeView.as_view()(request, request.path)
            wagtail_serve.assert_called_once_with(request, request.path)

    def test_no_sharing_site_exists_post_uses_wagtail_serve(self):
        request = self.make_request('/', method='post')
        with patch('wagtailsharing.views.wagtail_serve') as wagtail_serve:
            ServeView.as_view()(request, request.path)
            wagtail_serve.assert_called_once_with(request, request.path)

    def test_sharing_site_post_uses_wagtail_serve(self):
        self.create_sharing_site(hostname='hostname')

        request = self.make_request('/', HTTP_HOST='hostname', method='post')
        with patch('wagtailsharing.views.wagtail_serve') as wagtail_serve:
            ServeView.as_view()(request, request.path)
            wagtail_serve.assert_called_once_with(request, request.path)

    def test_default_site_missing_page_raises_404(self):
        self.create_sharing_site(hostname='hostname')

        request = self.make_request('/missing/')
        with self.assertRaises(Http404):
            ServeView.as_view()(request, request.path)

    def test_sharing_site_missing_page_raises_404(self):
        self.create_sharing_site(hostname='hostname')

        request = self.make_request('/missing/', HTTP_HOST='hostname')
        with self.assertRaises(Http404):
            ServeView.as_view()(request, request.path)

    def test_default_site_unpublished_page_raises_404(self):
        self.create_sharing_site(hostname='hostname')
        create_draft_page(self.default_site, title='unpublished')

        request = self.make_request('/unpublished/')
        with self.assertRaises(Http404):
            ServeView.as_view()(request, request.path)

    def test_sharing_site_unpublished_page_returns_200(self):
        self.create_sharing_site(hostname='hostname')
        create_draft_page(self.default_site, title='draft')

        request = self.make_request('/draft/', HTTP_HOST='hostname')
        response = ServeView.as_view()(request, request.path)
        self.assertEqual(response.status_code, 200)

    def test_default_site_published_page_returns_200(self):
        self.create_sharing_site(hostname='hostname')
        page = create_draft_page(self.default_site, title='published')
        page.save_revision().publish()

        request = self.make_request('/published/')
        response = ServeView.as_view()(request, request.path)
        self.assertEqual(response.status_code, 200)

    def test_sharing_site_published_page_returns_200(self):
        self.create_sharing_site(hostname='hostname')
        page = create_draft_page(self.default_site, title='published')
        page.save_revision().publish()

        request = self.make_request('/published/', HTTP_HOST='hostname')
        response = ServeView.as_view()(request, request.path)
        self.assertEqual(response.status_code, 200)

    def test_default_site_draft_version_returns_published_version(self):
        self.create_sharing_site(hostname='hostname')
        page = create_draft_page(self.default_site, title='original')
        page.save_revision().publish()
        page.title = 'changed'
        page.save_revision()

        request = self.make_request('/original/')
        response = ServeView.as_view()(request, request.path)
        self.assert_title_matches(response, 'original')

    def test_sharing_site_draft_version_returns_draft_version(self):
        self.create_sharing_site(hostname='hostname')
        page = create_draft_page(self.default_site, title='original')
        page.save_revision().publish()
        page.title = 'changed'
        page.save_revision()

        request = self.make_request('/original/', HTTP_HOST='hostname')
        response = ServeView.as_view()(request, request.path)
        self.assert_title_matches(response, 'changed')

    def test_before_serve_page_hook_called(self):
        self.create_sharing_site(hostname='hostname')
        create_draft_page(self.default_site, title='page')

        with self.register_hook('before_serve_page', before_serve_page):
            request = self.make_request('/page/', HTTP_HOST='hostname')
            response = ServeView.as_view()(request, request.path)
            self.assertContains(response, 'before serve page hook')

    def test_before_serve_shared_page_hook_called(self):
        self.create_sharing_site(hostname='hostname')
        create_draft_page(self.default_site, title='page')

        with self.register_hook(
            'before_serve_shared_page',
            before_serve_shared_page
        ):
            request = self.make_request('/page/', HTTP_HOST='hostname')
            response = ServeView.as_view()(request, request.path)
            self.assertContains(response, 'hook changed title')

    def test_after_serve_shared_page_hook_called(self):
        self.create_sharing_site(hostname='hostname')
        create_draft_page(self.default_site, title='page')

        with self.register_hook(
            'after_serve_shared_page',
            after_serve_shared_page
        ):
            request = self.make_request('/page/', HTTP_HOST='hostname')
            response = ServeView.as_view()(request, request.path)
            self.assertEqual(response['test-hook-header'], 'foo')
