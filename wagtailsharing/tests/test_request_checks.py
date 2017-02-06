from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase, override_settings

from wagtailsharing.request_checks import (
    HostnameRequestCheck, LoggedInUserRequestCheck, StaffUserRequestCheck,
    verify_sharing_request
)


class SuccessfulRequestCheck(object):
    def verify_request(self, request):
        return True


class UnsuccessfulRequestCheck(object):
    def verify_request(self, request):
        return False


class TestVerifySharingRequest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(WAGTAILSHARING_REQUEST_CHECKS=[])
    def test_no_checks(self):
        request = self.factory.get('/')
        self.assertFalse(verify_sharing_request(request))

    @override_settings(WAGTAILSHARING_REQUEST_CHECKS=[
        'wagtailsharing.tests.test_request_checks.SuccessfulRequestCheck',
    ])
    def test_check_succeeds(self):
        request = self.factory.get('/')
        self.assertTrue(verify_sharing_request(request))

    @override_settings(WAGTAILSHARING_REQUEST_CHECKS=[
        'wagtailsharing.tests.test_request_checks.UnsuccessfulRequestCheck',
    ])
    def test_check_fails(self):
        request = self.factory.get('/')
        self.assertFalse(verify_sharing_request(request))

    @override_settings(WAGTAILSHARING_REQUEST_CHECKS=[
        'wagtailsharing.tests.test_request_checks.SuccessfulRequestCheck',
        'wagtailsharing.tests.test_request_checks.UnsuccessfulRequestCheck',
    ])
    def test_only_one_check_succeeds(self):
        request = self.factory.get('/')
        self.assertTrue(verify_sharing_request(request))


class TestLoggedInUserRequestCheck(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.check = LoggedInUserRequestCheck()

    def test_no_user_not_verified(self):
        request = self.factory.get('/')
        self.assertFalse(self.check.verify_request(request))

    def test_anonymous_user_not_verified(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        self.assertFalse(self.check.verify_request(request))

    def test_logged_in_user_verified(self):
        request = self.factory.get('/')
        request.user = User(username='someone')
        self.assertTrue(self.check.verify_request(request))


class TestStaffUserRequestCheck(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.check = StaffUserRequestCheck()

    def test_no_user_not_verified(self):
        request = self.factory.get('/')
        self.assertFalse(self.check.verify_request(request))

    def test_anonymous_user_not_verified(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        self.assertFalse(self.check.verify_request(request))

    def test_nonstaff_user_not_verified(self):
        request = self.factory.get('/')
        request.user = User(username='someone')
        self.assertFalse(self.check.verify_request(request))

    def test_staff_user_verified(self):
        request = self.factory.get('/')
        request.user = User(username='someone', is_staff=True)
        self.assertTrue(self.check.verify_request(request))


@override_settings(WAGTAILSHARING_HOSTNAME='hostname.test:1234')
class TestHostnameRequestCheck(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.check = HostnameRequestCheck()

    def test_no_specified_hostname_not_verified(self):
        request = self.factory.get('/')
        self.assertFalse(self.check.verify_request(request))

    def test_valid_hostname_and_port_verified(self):
        request = self.factory.get(
            '/',
            SERVER_NAME='hostname.test',
            SERVER_PORT='1234'
        )
        self.assertTrue(self.check.verify_request(request))

    def test_invalid_port_not_verified(self):
        request = self.factory.get('/', SERVER_NAME='hostname.test')
        self.assertFalse(self.check.verify_request(request))

    def test_invalid_hostname_not_verified(self):
        request = self.factory.get('/', SERVER_PORT='1234')
        self.assertFalse(self.check.verify_request(request))
