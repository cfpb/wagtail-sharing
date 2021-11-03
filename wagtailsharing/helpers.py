from wagtail.core.models import Site

from wagtailsharing.models import SharingSite


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

    # patch root url such that (wrong) port is removed
    len_port = len(str(sharing_site.port)) + 1
    patched_root_url = sharing_site.root_url[:-len_port]
    
    return patched_root_url + page_path
