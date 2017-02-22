from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from wagtail.wagtailcore.models import Site


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
