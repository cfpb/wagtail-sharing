from __future__ import absolute_import, unicode_literals

from wagtailsharing.models import SharingSite


try:
    from wagtail.core.models import Site
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0
    from wagtail.wagtailcore.models import Site


def get_sharing_url(page):
    """Get a sharing URL for the latest revision of a page, if available."""
    url_parts = page.get_url_parts()

    if url_parts is None:
        # Page is not routable.
        return None

    site_id, root_url, page_path = url_parts

    site = Site.objects.get(id=site_id)

    try:
        sharing_site = site.sharing_site
    except SharingSite.DoesNotExist:
        # Site is not shared.
        return None

    return sharing_site.root_url + page_path
