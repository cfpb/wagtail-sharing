from bs4 import BeautifulSoup
from django.http import Http404, HttpResponse
from django.test import RequestFactory, TestCase, override_settings
from mock import Mock, patch

from wagtail.tests.testapp.models import SimplePage
from wagtail.wagtailcore.models import Site
from wagtailsharing.views import ServeView


class TestServeViewGet(TestCase):
    def setUp(self):
        self.path = '/simple'
        self.request = RequestFactory().get(self.path)

    @override_settings(WAGTAILSHARING_REQUEST_CHECKS=[
        'wagtailsharing.tests.test_request_checks.UnsuccessfulRequestCheck',
    ])
    def test_checks_fail(self):
        with patch('wagtailsharing.views.wagtail_serve') as wagtail_serve:
            ServeView().get(self.request, self.path)
            wagtail_serve.assert_called_once_with(self.request, self.path)

    @override_settings(WAGTAILSHARING_REQUEST_CHECKS=[
        'wagtailsharing.tests.test_request_checks.SuccessfulRequestCheck',
    ])
    def test_checks_pass(self):
        with patch(
            'wagtailsharing.views.ServeView.serve_shared'
        ) as serve_shared:
            ServeView().get(self.request, self.path)
            serve_shared.assert_called_once_with(self.request, self.path)


class TestServeViewServeShared(TestCase):
    def setUp(self):
        default_site = Site.objects.get(is_default_site=True)
        self.root = default_site.root_page

        self.slug = 'simple'
        self.path = '/' + self.slug
        self.request = RequestFactory().get(self.path)
        self.request.site = default_site

    def create_draft_page(self, title):
        page = SimplePage(
            title=title,
            slug=self.slug,
            content='content',
            live=False
        )

        self.root.add_child(instance=page)
        return page

    def assert_title_matches(self, html, title):
        soup = BeautifulSoup(html, 'html.parser')
        self.assertEqual(soup.title.text.strip(), title)

    def test_single_draft_revision(self):
        self.create_draft_page(title='ABC')
        response = ServeView.serve_shared(self.request, self.path)
        self.assert_title_matches(response.content, 'ABC')

    def test_single_published_revision(self):
        page = self.create_draft_page(title='ABC')
        page.save_revision().publish()
        response = ServeView.serve_shared(self.request, self.path)
        self.assert_title_matches(response.content, 'ABC')

    def test_newer_draft_revision(self):
        page = self.create_draft_page(title='ABC')
        page.save_revision().publish()
        page.title = 'DEF'
        page.save_revision()
        response = ServeView.serve_shared(self.request, self.path)
        self.assert_title_matches(response.content, 'DEF')

    def test_even_newer_draft_revision(self):
        page = self.create_draft_page(title='ABC')
        page.save_revision().publish()
        page.title = 'DEF'
        page.save_revision()
        page.title = 'GHI'
        page.save_revision()
        response = ServeView.serve_shared(self.request, self.path)
        self.assert_title_matches(response.content, 'GHI')

    def test_latest_published_revision(self):
        page = self.create_draft_page(title='ABC')
        page.save_revision().publish()
        page.title = 'DEF'
        page.save_revision().publish()
        response = ServeView.serve_shared(self.request, self.path)
        self.assert_title_matches(response.content, 'DEF')

    def test_before_serve_page_hook_called(self):
        with patch(
            'wagtail.wagtailcore.hooks.get_hooks'
        ) as get_hooks:
            self.create_draft_page(title='ABC')
            ServeView.serve_shared(self.request, self.path)
            get_hooks.assert_called_once_with('before_serve_page')

    def test_before_serve_page_hook_returns_redirect(self):
        with patch(
            'wagtail.wagtailcore.hooks.get_hooks',
            return_value=[Mock(return_value=HttpResponse(status=999))]
        ):
            self.create_draft_page(title='ABC')
            response = ServeView.serve_shared(self.request, self.path)
            self.assertEqual(response.status_code, 999)


class TestServeViewGetRequestedPage(TestCase):
    def setUp(self):
        default_site = Site.objects.get(is_default_site=True)
        self.root = default_site.root_page

        self.slug = 'simple'
        self.path = '/' + self.slug
        self.request = RequestFactory().get(self.path)
        self.request.site = default_site

    def create_draft_page(self, title='test'):
        page = SimplePage(
            title=title,
            slug=self.slug,
            content='content',
            live=False
        )

        self.root.add_child(instance=page)
        return page

    def test_no_site_raises_404(self):
        del self.request.site
        with self.assertRaises(Http404):
            ServeView.get_requested_page(self.request, self.path)

    def test_null_site_raises_404(self):
        self.request.site = None
        with self.assertRaises(Http404):
            ServeView.get_requested_page(self.request, self.path)

    def test_nonexistent_route_raises_404(self):
        with self.assertRaises(Http404):
            ServeView.get_requested_page(self.request, self.path)

    def test_draft_page_returned(self):
        self.create_draft_page()
        page, _, __ = ServeView.get_requested_page(self.request, self.path)
        self.assertEquals(page.slug, self.slug)

    def test_published_page_returned(self):
        page = self.create_draft_page()
        page.save_revision().publish()
        page, _, __ = ServeView.get_requested_page(self.request, self.path)
        self.assertEquals(page.slug, self.slug)
