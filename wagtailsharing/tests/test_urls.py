from importlib import reload

from django.test import TestCase

from mock import patch
from wagtail.core import urls as wagtail_core_urls

import wagtailsharing.urls


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


class TestUrlPatterns(TestCase):
    def setUp(self):
        def test_view():
            pass  # pragma: no cover

        root_patterns = [
            re_path(r"^foo/$", re_path, name="foo"),
            re_path(r"^((?:[\w\-]+/)*)$", re_path, name="wagtail_serve"),
            re_path(r"^bar/$", re_path, name="bar"),
        ]

        self.patcher = patch.object(
            wagtail_core_urls, "urlpatterns", root_patterns
        )
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

        reload(wagtailsharing.urls)
        self.urlpatterns = wagtailsharing.urls.urlpatterns

    def test_leaves_previous_urls_alone(self):
        self.assertEqual(self.urlpatterns[0].name, "foo")

    def test_replaces_wagtail_serve(self):
        self.assertEqual(self.urlpatterns[1].name, "wagtail_serve")
        self.assertEqual(self.urlpatterns[1].callback.__name__, "ServeView")

    def test_leaves_later_urls_alone(self):
        self.assertEqual(self.urlpatterns[2].name, "bar")
