import wagtail.wagtailcore.urls

from django.conf.urls import url
from django.test import TestCase
from mock import patch


class TestUrlPatterns(TestCase):
    def setUp(self):
        self.patterns = [
            url(r'^foo/$', 'views.foo', name='foo'),
            url(r'^((?:[\w\-]+/)*)$', 'views.replace', name='wagtail_serve'),
            url(r'^bar/$', 'views.bar', name='bar'),
        ]

        self.patcher = patch.object(
            wagtail.wagtailcore.urls,
            'urlpatterns',
            self.patterns
        )
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_leaves_previous_urls_alone(self):
        from wagtailsharing.urls import urlpatterns
        self.assertEqual(urlpatterns[0].name, 'foo')
        self.assertEqual(urlpatterns[0].regex.pattern, r'^foo/$')

    def test_replaces_wagtail_serve(self):
        from wagtailsharing.urls import urlpatterns
        self.assertEqual(urlpatterns[1].name, 'wagtail_serve')
        self.assertEqual(urlpatterns[1].callback.func_name, 'ServeView')

    def test_leaves_later_urls_alone(self):
        from wagtailsharing.urls import urlpatterns
        self.assertEqual(urlpatterns[2].name, 'bar')
        self.assertEqual(urlpatterns[2].regex.pattern, r'^bar/$')
