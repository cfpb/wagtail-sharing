from __future__ import unicode_literals

import inspect

from django.http import Http404, HttpResponse
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.views import serve as wagtail_serve


def serve(request, path):
    if request.is_sharing:
        return serve_shared(request, path)
    else:
        return wagtail_serve(request, path)


def serve_shared(request, path):
    if not request.site:
        raise Http404

    path_components = [component for component in path.split('/') if component]

    try:
        page, args, kwargs = request.site.root_page.route(
            request,
            path_components
        )
    except Http404:
        exception_source = inspect.trace()[-1]
        stack_frame = exception_source[0]

        page = stack_frame.f_locals['self']
        path_components = stack_frame.f_locals['path_components']

        if path_components:
            raise

        args = []
        kwargs = {}

    page = page.get_latest_revision_as_page()

    for fn in hooks.get_hooks('before_serve_page'):
        result = fn(page, request, args, kwargs)
        if isinstance(result, HttpResponse):
            return result

    response = page.serve(request, *args, **kwargs)
    response.is_shared = True

    return response
