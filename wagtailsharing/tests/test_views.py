from __future__ import absolute_import, unicode_literals

from django.http import Http404, HttpResponse
from django.test import RequestFactory, TestCase, override_settings
from mock import Mock, patch

from wagtail.wagtailcore.models import Site

from wagtailsharing.models import SharingSite
from wagtailsharing.tests.helpers import create_draft_page
from wagtailsharing.views import ServeView


class TestServeView(TestCase):
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

        with patch(
            'wagtail.wagtailcore.hooks.get_hooks'
        ) as get_hooks:
            request = self.make_request('/page/', HTTP_HOST='hostname')
            ServeView.as_view()(request, request.path)
            get_hooks.assert_called_once_with('before_serve_page')

    def test_before_serve_page_hook_returns_redirect(self):
        self.create_sharing_site(hostname='hostname')
        create_draft_page(self.default_site, title='page')

        with patch(
            'wagtail.wagtailcore.hooks.get_hooks',
            return_value=[Mock(return_value=HttpResponse(status=999))]
        ):
            request = self.make_request('/page/', HTTP_HOST='hostname')
            response = ServeView.as_view()(request, request.path)
            self.assertEqual(response.status_code, 999)

    @override_settings(WAGTAILSHARING_BANNER=False)
    def test_no_banner_setting(self):
        response = Mock(content='<body>abcde</body>')
        response = ServeView.postprocess_response(response)
        self.assertEqual(response.content, '<body>abcde</body>')

    def test_banner_setting_no_body(self):
        response = Mock(content='abcde')
        response = ServeView.postprocess_response(response)
        self.assertEqual(response.content, 'abcde')

    def test_banner_setting_modified_body(self):
        response = Mock(content='<body>abcde</body>')
        response = ServeView.postprocess_response(response)
        self.assertIn('wagtailsharing-banner', response.content)

    def test_banner_setting_modified_body_not_first_tag(self):
        response = Mock(content='<html><body>abcde</body></html>')
        response = ServeView.postprocess_response(response)
        self.assertIn('wagtailsharing-banner', response.content)

    def test_banner_setting_modified_body_uppercase(self):
        response = Mock(content='<BODY>abcde</BODY>')
        response = ServeView.postprocess_response(response)
        self.assertIn('wagtailsharing-banner', response.content)

    def test_banner_setting_modified_body_with_attributes(self):
        response = Mock(content='<body foo="foo" bar="bar">abcde</body>')
        response = ServeView.postprocess_response(response)
        self.assertIn('wagtailsharing-banner', response.content)

    def test_banner_leaves_links_alone(self):
        response = Mock(content='<body>Link <a href="#">and</a> spaces</body>')
        response = ServeView.postprocess_response(response)
        self.assertIn('<a href="#">and</a>', response.content)
