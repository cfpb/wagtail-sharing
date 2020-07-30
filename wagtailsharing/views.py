import inspect

from django.conf import settings
from django.http import Http404, HttpResponse
from django.views.generic import View

import jwt
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.core import hooks
from wagtail.core.url_routing import RouteResult
from wagtail.core.views import serve as wagtail_serve
from wagtailsharing.models import SharingSite


class ServeView(View):
    def dispatch(self, request, path):
        if request.method.upper() != "GET":
            return wagtail_serve(request, path)

        try:
            sharing_site = SharingSite.find_for_request(request)
        except SharingSite.DoesNotExist:
            sharing_site = None

        if not sharing_site:
            return wagtail_serve(request, path)

        page, args, kwargs = self.route(sharing_site.site, request, path)

        return self.serve(page, request, args, kwargs)

    @staticmethod
    def route(site, request, path):
        """Retrieve a page from a site given a request and path.

        This method uses the standard `wagtail.core.Page.route` method to
        retrieve a page using its path from the given site root.

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
            component for component in path.split("/") if component
        ]

        try:
            return site.root_page.route(request, path_components)
        except Http404:
            exception_source = inspect.trace()[-1]
            stack_frame = exception_source[0]

            page = stack_frame.f_locals["self"]
            path_components = stack_frame.f_locals["path_components"]

            if isinstance(page, RoutablePageMixin):
                # This mimics the way that RoutablePageMixin uses the
                # RouteResult to store the page route view to call.
                path = "/"
                if path_components:
                    path += "/".join(path_components) + "/"

                view, args, kwargs = page.resolve_subpage(path)
                return RouteResult(page, args=(view, args, kwargs))
            elif path_components:
                raise

            return RouteResult(page)

    @staticmethod
    def serve(page, request, args, kwargs):
        # Call the before_serve_page hook.
        for fn in hooks.get_hooks("before_serve_page"):
            result = fn(page, request, args, kwargs)
            if isinstance(result, HttpResponse):
                return result

        # Get the latest revision for the requested page.
        page = page.get_latest_revision_as_page()

        # Call the before_serve_shared_page hook.
        for fn in hooks.get_hooks("before_serve_shared_page"):
            result = fn(page, request, args, kwargs)
            if isinstance(result, HttpResponse):
                return result

        # Generate the page response.
        response = page.serve(request, *args, **kwargs)

        # Call the after_serve_shared_page hook.
        for fn in hooks.get_hooks("after_serve_shared_page"):
            result = fn(page, response)
            if isinstance(result, HttpResponse):
                return result

        return response


class TokenServeView(ServeView):
    def dispatch(self, request, path):
        from pudb import set_trace

        set_trace()
