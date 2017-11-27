from __future__ import absolute_import, unicode_literals

import inspect

from django.http import Http404, HttpResponse
from django.views.generic import View
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.views import serve as wagtail_serve

from wagtailsharing.models import SharingSite


class ServeView(View):
    def dispatch(self, request, path):
        if request.method.upper() != 'GET':
            return wagtail_serve(request, path)

        try:
            sharing_site = SharingSite.find_for_request(request)
        except SharingSite.DoesNotExist:
            return wagtail_serve(request, path)

        page, args, kwargs = self.get_requested_page(
            sharing_site.site,
            request,
            path
        )

        return self.serve_latest_revision(page, request, args, kwargs)

    @staticmethod
    def get_requested_page(site, request, path):
        """Retrieve a page from a site given a request and path.

        This method uses the standard `wagtail.wagtailcore.Page.route` method
        to retrieve a page using its path from the given site root.

        If a requested page exists and is published, the result of `Page.route`
        can be returned directly.

        If the page exists but is not yet published, `Page.route` raises an
        `Http404`, which this method tries to catch and handle. `Page.route`
        raises `Http404` in two cases: if no page with the given path exists
        and if a page exists but is unpublished. This method catches both
        cases, and, if they fall into the latter category, returns the
        requested page back to the caller despite its draft status.
        """
        path_components = [
            component for component in path.split('/') if component
        ]

        try:
            return site.root_page.route(request, path_components)
        except Http404:
            exception_source = inspect.trace()[-1]
            stack_frame = exception_source[0]

            page = stack_frame.f_locals['self']
            path_components = stack_frame.f_locals['path_components']

            if path_components:
                raise

            return page, [], {}

    @classmethod
    def serve_latest_revision(cls, page, request, args, kwargs):
        # Call the before_serve_page hook.
        for fn in hooks.get_hooks('before_serve_page'):
            result = fn(page, request, args, kwargs)
            if isinstance(result, HttpResponse):
                return result

        # Get the latest revision for the requested page.
        page = page.get_latest_revision_as_page()

        # Call the before_serve_shared_page hook.
        for fn in hooks.get_hooks('before_serve_shared_page'):
            result = fn(page, request, args, kwargs)
            if isinstance(result, HttpResponse):
                return result

        # Generate the page response.
        response = page.serve(request, *args, **kwargs)

        # Call the after_serve_shared_page hook.
        for fn in hooks.get_hooks('after_serve_shared_page'):
            result = fn(page, response)
            if isinstance(result, HttpResponse):
                return result

        return response
