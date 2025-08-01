from django.test import RequestFactory, TestCase

from wagtail.models import Site

from wagtailsharing.routers.base import RouterBase


class RouterBaseTests(TestCase):
    def test_route_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            RouterBase().route(RequestFactory().get("/"), "/")

    def test_get_sharing_url_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            RouterBase().get_sharing_url(
                Site.objects.get(is_default_site=True).root_page
            )
