from django.test import RequestFactory, TestCase, modify_settings
from wagtail.wagtailcore.models import Site
from wagtailsharing.middleware import SiteMiddleware
from wagtailsharing.models import SharingSite

class TestSiteMiddleware(TestCase):
    def setUp(self):
        self.default_site = Site.objects.get(is_default_site=True)
        self.factory = RequestFactory()
        self.sharing_site = SharingSite.objects.create(
            site=self.default_site,
            hostname='hostname'
        )
        self.middleware = SiteMiddleware()

    def make_request(self):
        return self.factory.get('/', HTTP_HOST=self.sharing_site.hostname)

    def test_exception_thrown_when_no_site(self):
        request = self.make_request()
        with self.assertRaises(Exception):
            self.middleware.process_request(request)

    def test_site_is_set(self):
        request = self.make_request()
        request.site = None
        self.middleware.process_request(request)
        self.assertEqual(request.site, self.default_site)
