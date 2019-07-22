from django.http import HttpResponse

from wagtailsharing.models import ShareableRoutablePageMixin

try:
    from wagtail.core.models import Page
    from wagtail.contrib.routable_page.models import route
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0
    from wagtail.wagtailcore.models import Page
    from wagtail.contrib.wagtailroutablepage.models import route


class ShareableRoutablePageModel(ShareableRoutablePageMixin, Page):
    @route(r'^subpage-url/$')
    def subpage_url(self, request):
        return HttpResponse('SUBPAGE URL')

    @route(r'^subpage-url-without-slash$')
    def subpage_url_without_slash(self, request):
        return HttpResponse('SUBPAGE URL WITHOUT SLASH')
