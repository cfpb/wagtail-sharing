from django.utils.deprecation import MiddlewareMixin

from wagtail.wagtailcore.models import Site
from wagtailsharing.models import SharingSite

class SiteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        Set request.site to contain the Site object responsible for handling this request,
        according to hostname matching rules.
        """

        # request.site must exist before we can do anything
        if not hasattr(request, 'site'):
            raise Exception("request has no `site` attribute, make sure you define the wagtailsharing middleware after wagtail core middleware")

        if request.site == None:
            try:
                request.site = SharingSite.find_for_request(request).site
            except SharingSite.DoesNotExist:
                request.site = None
