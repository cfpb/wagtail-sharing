from django.db import models
from django.http import HttpResponse

from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.contrib.routable_page.models import RoutablePageMixin, route


if WAGTAIL_VERSION >= (3, 0):
    from wagtail.models import Page
else:
    from wagtail.core.models import Page

from wagtailsharing.models import ShareableRoutablePageMixin


class RoutableTestPage(RoutablePageMixin, Page):
    text = models.TextField()

    @route(r"^$")
    def index_route(self, request):
        return HttpResponse(self.text)


class ShareableRoutableTestPage(ShareableRoutablePageMixin, Page):
    text = models.TextField()

    @route(r"^$")
    def index_route(self, request):
        return HttpResponse(self.text)
