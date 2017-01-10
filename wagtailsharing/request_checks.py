from __future__ import unicode_literals

from django.conf import settings
from django.utils.module_loading import import_string


def verify_sharing_request(request):
    checks = getattr(settings, 'WAGTAILSHARING_REQUEST_CHECKS', [])

    for check in checks:
        check_cls = import_string(check)
        if check_cls().verify_request(request):
            return True


class LoggedInUserRequestCheck(object):
    def verify_request(self, request):
        return request.user.is_authenticated()


class StaffUserRequestCheck(object):
    def verify_request(self, request):
        return request.user.is_authenticated() and request.user.is_staff


class HostnameRequestCheck(object):
    def verify_request(self, request):
        sharing_hostname = getattr(settings, 'WAGTAILSHARING_HOSTNAME', None)
        return sharing_hostname and sharing_hostname == request.get_host()
