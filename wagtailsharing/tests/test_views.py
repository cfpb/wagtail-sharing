from unittest.mock import patch

from django.http import Http404, HttpResponse
from django.test import RequestFactory, TestCase

from wagtail.models import Site
from wagtail.test.utils import WagtailTestUtils

from wagtailsharing.models import SharingSite
from wagtailsharing.tests.helpers import (
    create_draft_page,
    create_draft_routable_page,
)
from wagtailsharing.views import ServeView


def before_hook_returns_http_response(*args):
    return HttpResponse("returned by hook")


def before_hook_changes_page_title(page, request, args, kwargs):
    page.title = "hook changed title"


def after_hook_returns_http_response(page, response):
    return HttpResponse("returned by hook")


def after_hook_sets_response_header(page, response):
    response["test-hook-header"] = "foo"


class TestServeView(WagtailTestUtils, TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.default_site = Site.objects.get(is_default_site=True)

    def make_request(self, path, method="get", **kwargs):
        return getattr(self.factory, method)(path, **kwargs)

    def create_sharing_site(self, hostname):
        SharingSite.objects.create(site=self.default_site, hostname=hostname)

    def assert_title_matches(self, response, title):
        self.assertContains(response, title)

    def test_no_sharing_site_exists_uses_wagtail_serve(self):
        request = self.make_request("/")
        with patch("wagtailsharing.views.wagtail_serve") as wagtail_serve:
            ServeView.as_view()(request, request.path)
            wagtail_serve.assert_called_once_with(request, request.path)

    def test_no_sharing_site_exists_post_uses_wagtail_serve(self):
        request = self.make_request("/", method="post")
        with patch("wagtailsharing.views.wagtail_serve") as wagtail_serve:
            ServeView.as_view()(request, request.path)
            wagtail_serve.assert_called_once_with(request, request.path)

    def test_sharing_site_post_uses_wagtail_serve(self):
        self.create_sharing_site(hostname="hostname")

        request = self.make_request("/", HTTP_HOST="hostname", method="post")
        with patch("wagtailsharing.views.wagtail_serve") as wagtail_serve:
            ServeView.as_view()(request, request.path)
            wagtail_serve.assert_called_once_with(request, request.path)

    def test_default_site_missing_page_raises_404(self):
        self.create_sharing_site(hostname="hostname")

        request = self.make_request("/missing/")
        with self.assertRaises(Http404):
            ServeView.as_view()(request, request.path)

    def test_sharing_site_missing_page_raises_404(self):
        self.create_sharing_site(hostname="hostname")

        request = self.make_request("/missing/", HTTP_HOST="hostname")
        with self.assertRaises(Http404):
            ServeView.as_view()(request, request.path)

    def test_default_site_unpublished_page_raises_404(self):
        self.create_sharing_site(hostname="hostname")
        create_draft_page(self.default_site, title="unpublished")

        request = self.make_request("/unpublished/")
        with self.assertRaises(Http404):
            ServeView.as_view()(request, request.path)

    def test_sharing_site_unpublished_page_returns_200(self):
        self.create_sharing_site(hostname="hostname")
        create_draft_page(self.default_site, title="draft")

        request = self.make_request("/draft/", HTTP_HOST="hostname")
        response = ServeView.as_view()(request, request.path)
        self.assertEqual(response.status_code, 200)

    def test_default_site_published_page_returns_200(self):
        self.create_sharing_site(hostname="hostname")
        page = create_draft_page(self.default_site, title="published")
        page.save_revision().publish()

        request = self.make_request("/published/")
        response = ServeView.as_view()(request, request.path)
        self.assertEqual(response.status_code, 200)

    def test_sharing_site_published_page_returns_200(self):
        self.create_sharing_site(hostname="hostname")
        page = create_draft_page(self.default_site, title="published")
        page.save_revision().publish()

        request = self.make_request("/published/", HTTP_HOST="hostname")
        response = ServeView.as_view()(request, request.path)
        self.assertEqual(response.status_code, 200)

    def test_default_site_draft_version_returns_published_version(self):
        self.create_sharing_site(hostname="hostname")
        page = create_draft_page(self.default_site, title="original")
        page.save_revision().publish()
        page.title = "changed"
        page.save_revision()

        request = self.make_request("/original/")
        response = ServeView.as_view()(request, request.path)
        self.assert_title_matches(response, "original")

    def test_sharing_site_draft_version_returns_draft_version(self):
        self.create_sharing_site(hostname="hostname")
        page = create_draft_page(self.default_site, title="original")
        page.save_revision().publish()
        page.title = "changed"
        page.save_revision()

        request = self.make_request("/original/", HTTP_HOST="hostname")
        response = ServeView.as_view()(request, request.path)
        self.assert_title_matches(response, "changed")

    def test_before_serve_page_hook_called(self):
        self.create_sharing_site(hostname="hostname")
        create_draft_page(self.default_site, title="page")

        with self.register_hook(
            "before_serve_page", before_hook_returns_http_response
        ):
            request = self.make_request("/page/", HTTP_HOST="hostname")
            response = ServeView.as_view()(request, request.path)
            self.assertContains(response, "returned by hook")

    def test_before_serve_shared_page_hook_called(self):
        self.create_sharing_site(hostname="hostname")
        create_draft_page(self.default_site, title="page")

        with self.register_hook(
            "before_serve_shared_page", before_hook_changes_page_title
        ):
            request = self.make_request("/page/", HTTP_HOST="hostname")
            response = ServeView.as_view()(request, request.path)
            self.assertContains(response, "hook changed title")

    def test_before_serve_shared_page_hook_returns_http_response(self):
        self.create_sharing_site(hostname="hostname")
        create_draft_page(self.default_site, title="page")

        with self.register_hook(
            "before_serve_shared_page", before_hook_returns_http_response
        ):
            request = self.make_request("/page/", HTTP_HOST="hostname")
            response = ServeView.as_view()(request, request.path)
            self.assertContains(response, "returned by hook")

    def test_after_serve_shared_page_hook_called(self):
        self.create_sharing_site(hostname="hostname")
        create_draft_page(self.default_site, title="page")

        with self.register_hook(
            "after_serve_shared_page", after_hook_sets_response_header
        ):
            request = self.make_request("/page/", HTTP_HOST="hostname")
            response = ServeView.as_view()(request, request.path)
            self.assertEqual(response["test-hook-header"], "foo")

    def test_after_serve_shared_page_hook_returns_http_response(self):
        self.create_sharing_site(hostname="hostname")
        create_draft_page(self.default_site, title="page")

        with self.register_hook(
            "after_serve_shared_page", after_hook_returns_http_response
        ):
            request = self.make_request("/page/", HTTP_HOST="hostname")
            response = ServeView.as_view()(request, request.path)
            self.assertContains(response, "returned by hook")

    def test_routable_page_index_route(self):
        self.create_sharing_site(hostname="hostname")
        create_draft_routable_page(self.default_site, title="routable")

        request = self.make_request("/routable/", HTTP_HOST="hostname")
        response = ServeView.as_view()(request, request.path)
        self.assertEqual(response.status_code, 200)

    def test_routable_page_sub_route(self):
        self.create_sharing_site(hostname="hostname")
        create_draft_routable_page(self.default_site, title="routable")

        request = self.make_request(
            "/routable/archive/year/2000/", HTTP_HOST="hostname"
        )
        response = ServeView.as_view()(request, request.path)
        self.assertContains(response, "ARCHIVE BY YEAR: 2000")

    def test_before_route_page_hook_called(self):
        self.create_sharing_site(hostname="sharinghostname")
        create_draft_page(self.default_site, title="page")

        with self.register_hook(
            "before_route_page", before_hook_returns_http_response
        ):
            request = self.make_request("/page/", HTTP_HOST="sharinghostname")
            response = ServeView.as_view()(request, request.path)
            self.assertContains(response, "returned by hook")
