from django.test import RequestFactory, SimpleTestCase

from wagtailsharing.helpers import (
    get_hostname_and_port_from_request,
    make_root_url,
    parse_host,
)


class GetHostnameAndPortFromRequestTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_request(self):
        request = self.factory.get("/", HTTP_HOST="example.com")
        self.assertEqual(
            get_hostname_and_port_from_request(request), ("example.com", 80)
        )

    def test_request_with_port(self):
        request = self.factory.get(
            "/", HTTP_HOST="example.com", SERVER_PORT=5678
        )
        self.assertEqual(
            get_hostname_and_port_from_request(request), ("example.com", 5678)
        )

    def test_request_without_hostname(self):
        request = self.factory.get("/")
        del request.META["SERVER_NAME"]
        self.assertEqual(
            get_hostname_and_port_from_request(request), (None, 80)
        )

    def test_request_without_port(self):
        request = self.factory.get("/", HTTP_HOST="example.com")
        del request.META["SERVER_PORT"]
        self.assertEqual(
            get_hostname_and_port_from_request(request), ("example.com", None)
        )


class MakeRootURLTests(SimpleTestCase):
    def test_make_root_url(self):
        for hostname, port, root_url in [
            ("example.com", 80, "http://example.com"),
            ("example.com", 443, "https://example.com"),
            ("example.com", 8000, "http://example.com:8000"),
        ]:
            with self.subTest(hostname=hostname, port=port, root_url=root_url):
                self.assertEqual(make_root_url(hostname, port), root_url)


class ParseHostTests(SimpleTestCase):
    def test_valid(self):
        for host, hostname, port in [
            ("example.com", "example.com", 80),
            ("http://example.com", "example.com", 80),
            ("https://example.com", "example.com", 443),
            ("example.com:443", "example.com", 443),
            ("localhost:8000", "localhost", 8000),
            ("subdomain.example.com", "subdomain.example.com", 80),
            ("http://example.com:8080", "example.com", 8080),
            ("https://example.com:8443", "example.com", 8443),
            ("192.168.1.1", "192.168.1.1", 80),
            ("192.168.1.1:3000", "192.168.1.1", 3000),
        ]:
            with self.subTest(host=host, hostname=hostname, port=port):
                self.assertEqual(parse_host(host), (hostname, port))

    def test_invalid(self):
        for host in [
            "http://",
            "https://",
            "http:///path",
            "",
            ":8080",
        ]:
            with self.subTest(host=host):
                with self.assertRaises(ValueError):
                    parse_host(host)
