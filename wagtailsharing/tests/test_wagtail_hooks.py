from unittest.mock import Mock

from django.conf import settings
from django.http import HttpResponse
from django.test import RequestFactory, TestCase, override_settings

from wagtail.models import Site

from wagtailsharing.models import SharingSite
from wagtailsharing.tests.helpers import create_draft_page
from wagtailsharing.tests.shareable_routable_testapp.models import TestPage
from wagtailsharing.wagtail_hooks import (
    add_sharing_banner,
    add_sharing_link,
    set_routed_by_wagtail_sharing,
    set_served_by_wagtail_sharing,
)


class TestAddSharingLink(TestCase):
    def setUp(self):
        self.default_site = Site.objects.get(is_default_site=True)
        self.user = Mock()

    def test_no_link_no_button(self):
        page = TestPage(title="title", slug="slug")
        links = add_sharing_link(page, self.user)
        self.assertFalse(list(links))

    def test_link_makes_button(self):
        SharingSite.objects.create(
            site=self.default_site, hostname="sharing.example.com", port=8080
        )
        page = create_draft_page(self.default_site, title="test")

        links = add_sharing_link(page, self.user)
        button = next(links)
        self.assertEqual(button.url, "http://sharing.example.com:8080/test/")
        self.assertIn(
            page.get_admin_display_title(), button.attrs["aria-label"]
        )


class TestAddSharingBanner(TestCase):
    def setUp(self):
        self.page = TestPage(title="title", slug="slug")

    def add_banner_to_response(self, content):
        response = HttpResponse(content=content)
        add_sharing_banner(self.page, response)
        return response

    @override_settings(WAGTAILSHARING_BANNER=False)
    def test_setting_false_no_banner_added(self):
        response = self.add_banner_to_response("<body>abcde</body>")
        self.assertNotContains(response, "wagtailsharing-banner")

    @override_settings(WAGTAILSHARING_BANNER=True)
    def test_setting_true_banner_is_added(self):
        response = self.add_banner_to_response("<body>abcde</body>")
        self.assertContains(response, "wagtailsharing-banner")

    @override_settings()
    def test_setting_not_defined_defaults_to_true_banner_is_added(self):
        del settings.WAGTAILSHARING_BANNER
        response = self.add_banner_to_response("<body>abcde</body>")
        self.assertContains(response, "wagtailsharing-banner")

    def test_no_body_in_response_content_banner_not_added(self):
        response = self.add_banner_to_response("abcde")
        self.assertNotContains(response, "wagtailsharing-banner")

    def test_body_not_first_tag_still_adds_banner(self):
        content = "<html><body>abcde</body></html>"
        response = self.add_banner_to_response(content)
        self.assertContains(response, "wagtailsharing-banner")

    def test_body_tag_uppercase_still_adds_banner(self):
        response = self.add_banner_to_response("<BODY>abcde</BODY>")
        self.assertContains(response, "wagtailsharing-banner")

    def test_body_with_attributes_still_adds_banner(self):
        content = '<body foo="foo" bar="bar">abcde</body>'
        response = self.add_banner_to_response(content)
        self.assertContains(response, "wagtailsharing-banner")

    def test_banner_leaves_links_alone(self):
        content = '<body>Link <a href="#">and</a> spaces</body>'
        response = self.add_banner_to_response(content)
        self.assertContains(response, '<a href="#">and</a>')

    def test_body_has_newlines_still_adds_banner(self):
        content = """<html><body

        >
        abcde</body></html>"""
        response = self.add_banner_to_response(content)
        self.assertContains(response, "wagtailsharing-banner")


class TestSetRoutedByWagtailSharing(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_set_routed_by_wagtail_sharing(self):
        request = self.factory.get("/an-url")
        set_routed_by_wagtail_sharing(request, "")
        self.assertTrue(request.routed_by_wagtail_sharing)


class TestSetServedByWagtailSharing(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_set_served_by_wagtail_sharing(self):
        request = self.factory.get("/an-url")
        set_served_by_wagtail_sharing(None, request, [], {})
        self.assertTrue(request.served_by_wagtail_sharing)
