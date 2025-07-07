from django.test import TestCase, override_settings

from wagtailsharing.routers import get_router, get_router_cls
from wagtailsharing.routers.db import DatabaseHostRouter


class GetRouterClsTests(TestCase):
    def test_default_router_class(self):
        self.assertEqual(
            get_router_cls(),
            "wagtailsharing.routers.db.DatabaseHostRouter",
        )

    @override_settings(WAGTAILSHARING_ROUTER="custom.router.CustomRouter")
    def test_custom_router_class(self):
        self.assertEqual(get_router_cls(), "custom.router.CustomRouter")


class GetRouterTests(TestCase):
    def test_get_router_returns_instance(self):
        router = get_router()
        self.assertIsInstance(router, DatabaseHostRouter)
