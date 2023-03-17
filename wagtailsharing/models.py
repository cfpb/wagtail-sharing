from django.db import models

import wagtail
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.models import Site


class SharingSite(models.Model):
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, related_name="sharing_site"
    )
    hostname = models.CharField(max_length=255, db_index=True)
    port = models.IntegerField(default=80)

    class Meta:
        unique_together = ("hostname", "port")

    def __str__(self):
        return self.hostname + ("" if self.port == 80 else (":%d" % self.port))

    @classmethod
    def find_for_request(cls, request):
        """
        Find a shared site associated with this HTTP request object. Raises
        Raises SharingSite.DoesNotExist if no appropriate sharing site exists.

        Uses request hostname and port to find matching sharing site.
        """
        try:
            hostname = request.get_host().split(":")[0]
        except KeyError:
            hostname = None

        try:
            port = request.get_port()
        except (AttributeError, KeyError):
            port = request.META.get("SERVER_PORT")

        return cls.objects.get(hostname=hostname, port=port)

    @property
    def root_url(self):
        if self.port == 80:
            return "http://{}".format(self.hostname)
        elif self.port == 443:
            return "https://{}".format(self.hostname)
        else:
            return "http://{}:{:d}".format(self.hostname, self.port)


class ShareableRoutablePageMixin(RoutablePageMixin):
    def route(self, request, path_components):
        if getattr(request, "routed_by_wagtail_sharing", False):
            if wagtail.VERSION >= (4,):
                page = self.get_latest_revision_as_object()
            else:
                page = self.get_latest_revision_as_page()

            # This call to RoutablePageMixin's route() is so that the  method
            # gets called with the latest-revision-as-page object as self,
            # rather than the page object that is current self in this context.
            # This ensures that, if we're being routed by wagtail sharing, we
            # serve the latest revision.
            return RoutablePageMixin.route(page, request, path_components)
        return super().route(request, path_components)
