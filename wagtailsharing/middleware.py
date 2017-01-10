from __future__ import unicode_literals

from bs4 import BeautifulSoup
from django.conf import settings
from django.template import loader

from wagtailsharing.request_checks import verify_sharing_request


class WagtailSharingMiddleware(object):
    def process_request(self, request):
        request.is_sharing = verify_sharing_request(request)

    def process_response(self, request, response):
        if getattr(response, 'is_shared', False):
            if getattr(settings, 'WAGTAILSHARING_BANNER', True):
                self.add_response_banner(response)

        return response

    def add_response_banner(self, response):
        html = BeautifulSoup(response.content, 'html.parser')

        banner_template_name = 'wagtailsharing/banner.html'
        banner_template = loader.get_template(banner_template_name)
        banner_html = banner_template.render()

        banner = BeautifulSoup(banner_html, 'html.parser')
        html.body.insert(0, banner)
        response.content = html.prettify()

        return response
