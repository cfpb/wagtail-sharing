from __future__ import absolute_import, unicode_literals

try:
    from importlib import reload
except ImportError:
    pass

from django.conf.urls import url
from django.test import TestCase
from mock import patch

try:
    import wagtail.core.urls as wagtail_core_urls
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0
    import wagtail.wagtailcore.urls as wagtail_core_urls

import wagtailsharing.urls


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
            wagtail_core_urls,
            'urlpatterns',
            root_patterns
        )
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

        reload(wagtailsharing.urls)
        self.urlpatterns = wagtailsharing.urls.urlpatterns

    def test_leaves_previous_urls_alone(self):
        self.assertEqual(self.urlpatterns[0].name, 'foo')

    def test_replaces_wagtail_serve(self):
        self.assertEqual(self.urlpatterns[1].name, 'wagtail_serve')
        self.assertEqual(self.urlpatterns[1].callback.__name__, 'ServeView')

    def test_leaves_later_urls_alone(self):
        self.assertEqual(self.urlpatterns[2].name, 'bar')
