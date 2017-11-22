from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.http import HttpResponse
from django.test import TestCase, override_settings
from mock import Mock, patch
from wagtail.tests.testapp.models import SimplePage

from wagtailsharing.wagtail_hooks import add_sharing_banner, add_sharing_link


class TestAddSharingLink(TestCase):
    def setUp(self):
        self.page = SimplePage(title='title', slug='slug', content='content')
        self.page_perms = Mock()

    def test_no_link_no_button(self):
        with patch(
            'wagtailsharing.wagtail_hooks.get_sharing_url',
            return_value=None
        ):
            links = add_sharing_link(self.page, self.page_perms)
            self.assertFalse(list(links))

    def check_link_makes_button(self):
        url = 'http://test.domain/slug/'
        with patch(
            'wagtailsharing.wagtail_hooks.get_sharing_url',
            return_value=url
        ):
            links = add_sharing_link(self.page, self.page_perms)
            button = next(links)
            self.assertEqual(button.url, url)
            self.assertIn(self.page.title, button.attrs['title'])

    def test_link_makes_button(self):
        self.check_link_makes_button()

    def test_link_no_admin_display_title(self):
        try:
            delattr(self.page, 'get_admin_display_title')
        except AttributeError:
            pass

        self.check_link_makes_button()

    def test_link_admin_display_title(self):
        if not hasattr(self.page, 'get_admin_display_title'):
            self.page.get_admin_display_title = lambda: self.page.title

        self.check_link_makes_button()


class TestAddSharingBanner(TestCase):
    def setUp(self):
        self.page = SimplePage(title='title', slug='slug', content='content')

    def add_banner_to_response(self, content):
        response = HttpResponse(content=content)
        add_sharing_banner(self.page, response)
        return response

    @override_settings(WAGTAILSHARING_BANNER=False)
    def test_setting_false_no_banner_added(self):
        response = self.add_banner_to_response('<body>abcde</body>')
        self.assertNotContains(response, 'wagtailsharing-banner')

    @override_settings(WAGTAILSHARING_BANNER=True)
    def test_setting_true_banner_is_added(self):
        response = self.add_banner_to_response('<body>abcde</body>')
        self.assertContains(response, 'wagtailsharing-banner')

    @override_settings()
    def test_setting_not_defined_defaults_to_true_banner_is_added(self):
        del settings.WAGTAILSHARING_BANNER
        response = self.add_banner_to_response('<body>abcde</body>')
        self.assertContains(response, 'wagtailsharing-banner')

    def test_no_body_in_response_content_banner_not_added(self):
        response = self.add_banner_to_response('abcde')
        self.assertNotContains(response, 'wagtailsharing-banner')

    def test_body_not_first_tag_still_adds_banner(self):
        content = '<html><body>abcde</body></html>'
        response = self.add_banner_to_response(content)
        self.assertContains(response, 'wagtailsharing-banner')

    def test_body_tag_uppercase_still_adds_banner(self):
        response = self.add_banner_to_response('<BODY>abcde</BODY>')
        self.assertContains(response, 'wagtailsharing-banner')

    def test_body_with_attributes_still_adds_banner(self):
        content = '<body foo="foo" bar="bar">abcde</body>'
        response = self.add_banner_to_response(content)
        self.assertContains(response, 'wagtailsharing-banner')

    def test_banner_leaves_links_alone(self):
        content = '<body>Link <a href="#">and</a> spaces</body>'
        response = self.add_banner_to_response(content)
        self.assertContains(response, '<a href="#">and</a>')
