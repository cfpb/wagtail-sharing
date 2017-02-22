import wagtail.wagtailcore.urls

import wagtailsharing.urls

from django.conf.urls import url
from django.test import TestCase
from mock import patch


try:
    from importlib import reload
except ImportError:
    pass


class TestUrlPatterns(TestCase):
    def setUp(self):
        def test_view():
            pass  # pragma: no cover

        root_patterns = [
            url(r'^foo/$', url, name='foo'),
            url(r'^((?:[\w\-]+/)*)$', url, name='wagtail_serve'),
            url(r'^bar/$', url, name='bar'),
        ]

        self.patcher = patch.object(
            wagtail.wagtailcore.urls,
            'urlpatterns',
            root_patterns
        )
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

        reload(wagtailsharing.urls)
        self.urlpatterns = wagtailsharing.urls.urlpatterns

    def test_leaves_previous_urls_alone(self):
        self.assertEqual(self.urlpatterns[0].name, 'foo')
        self.assertEqual(self.urlpatterns[0].regex.pattern, r'^foo/$')

    def test_replaces_wagtail_serve(self):
        self.assertEqual(self.urlpatterns[1].name, 'wagtail_serve')
        self.assertEqual(self.urlpatterns[1].callback.__name__, 'ServeView')

    def test_leaves_later_urls_alone(self):
        self.assertEqual(self.urlpatterns[2].name, 'bar')
        self.assertEqual(self.urlpatterns[2].regex.pattern, r'^bar/$')
