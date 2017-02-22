from django.test import TestCase
from mock import Mock, patch
from wagtail.tests.testapp.models import SimplePage

from wagtailsharing.wagtail_hooks import add_sharing_link


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

    def test_link_makes_button(self):
        url = 'http://test.domain/slug/'
        with patch(
            'wagtailsharing.wagtail_hooks.get_sharing_url',
            return_value=url
        ):
            links = add_sharing_link(self.page, self.page_perms)
            button = next(links)
            self.assertEqual(button.url, url)
