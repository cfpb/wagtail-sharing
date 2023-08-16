from django.test import TestCase

from wagtail.models import Site

from wagtailsharing.helpers import get_sharing_url
from wagtailsharing.models import SharingSite
from wagtailsharing.tests.helpers import create_draft_page
from wagtailsharing.tests.shareable_routable_testapp.models import TestPage


class TestGetSharingUrl(TestCase):
    def setUp(self):
        self.default_site = Site.objects.get(is_default_site=True)

    def create_sharing_site(self, hostname):
        SharingSite.objects.create(site=self.default_site, hostname=hostname)

    def test_unroutable_page_no_sharing_site_returns_none(self):
        page = TestPage(title="title", slug="slug")
        self.assertIsNone(get_sharing_url(page))

    def test_unroutable_page_sharing_site_returns_none(self):
        self.create_sharing_site(hostname="hostname")
        page = TestPage(title="title", slug="slug")
        self.assertIsNone(get_sharing_url(page))

    def test_draft_page_no_sharing_site_returns_none(self):
        page = create_draft_page(self.default_site, title="draft")
        self.assertIsNone(get_sharing_url(page))

    def test_draft_page_sharing_site_returns_url(self):
        self.create_sharing_site(hostname="hostname")
        page = create_draft_page(self.default_site, title="draft")
        self.assertEqual(get_sharing_url(page), "http://hostname/draft/")

    def test_published_page_no_sharing_site_returns_none(self):
        page = create_draft_page(self.default_site, title="published")
        page.save_revision().publish()
        self.assertIsNone(get_sharing_url(page))

    def test_published_page_sharing_site_returns_url(self):
        self.create_sharing_site(hostname="hostname")
        page = create_draft_page(self.default_site, title="published")
        page.save_revision().publish()
        self.assertEqual(get_sharing_url(page), "http://hostname/published/")

    def test_url_always_based_on_database_version(self):
        self.create_sharing_site(hostname="hostname")
        page = create_draft_page(self.default_site, title="initial")
        self.assertEqual(get_sharing_url(page), "http://hostname/initial/")

        page.slug = "second"
        page.save_revision()
        self.assertEqual(get_sharing_url(page), "http://hostname/initial/")

        page.slug = "third"
        page.save_revision().publish()
        self.assertEqual(get_sharing_url(page), "http://hostname/third/")

        page.slug = "fourth"
        page.save_revision()
        self.assertEqual(get_sharing_url(page), "http://hostname/third/")
