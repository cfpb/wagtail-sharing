from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.db import models
from django.http import Http404
from django.utils.encoding import python_2_unicode_compatible

try:
    from wagtail.core.models import Site
    from wagtail.contrib.routable_page.models import RoutablePageMixin
    from wagtail.core.url_routing import RouteResult
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0
    from wagtail.wagtailcore.models import Site
    from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin
    from wagtail.wagtailcore.url_routing import RouteResult


@python_2_unicode_compatible
class SharingSite(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE,
                                related_name='sharing_site')
    hostname = models.CharField(max_length=255, db_index=True)
    port = models.IntegerField(default=80)

    class Meta:
        unique_together = ('hostname', 'port')

    def __str__(self):
        return(
            self.hostname +
            ('' if self.port == 80 else (':%d' % self.port))
        )

    @classmethod
    def find_for_request(cls, request):
        """
        Find a shared site associated with this HTTP request object. Raises
        Raises SharingSite.DoesNotExist if no appropriate sharing site exists.

        Uses request hostname and port to find matching sharing site.
        """
        try:
            hostname = request.get_host().split(':')[0]
        except KeyError:
            hostname = None

        try:
            port = request.get_port()
        except (AttributeError, KeyError):
            port = request.META.get('SERVER_PORT')

        return cls.objects.get(hostname=hostname, port=port)

    @property
    def root_url(self):
        if self.port == 80:
            return 'http://{}'.format(self.hostname)
        elif self.port == 443:
            return 'https://{}'.format(self.hostname)
        else:
            return 'http://{}:{:d}'.format(self.hostname, self.port)


class ShareableRoutablePageMixin(RoutablePageMixin):

    def route(self, request, path_components):
        """
        Allow subpage URLs in Wagtail routing on the sharing site.
        """
        try:
            SharingSite.find_for_request(request)
        except SharingSite.DoesNotExist:
            return super(ShareableRoutablePageMixin, self).route(
                request, path_components
            )

        try:
            path = '/'
            if path_components:
                path += '/'.join(path_components)
                if settings.APPEND_SLASH:
                    path += '/'

            view, args, kwargs = self.resolve_subpage(path)
            return RouteResult(self, args=(view, args, kwargs))
        except Http404:
            return super(ShareableRoutablePageMixin, self).route(
                request, path_components
            )
