from django.conf import settings

from wagtail.models import Site

import jwt

from wagtailsharing.models import SharingSite


def get_tokenized_sharing_url(sharing_site, page_path):
    share_path = getattr(settings, "WAGTAILSHARING_TOKEN_SHARE_PATH", "share")
    payload = {"path": page_path}
    hash = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return "/".join([sharing_site.root_url, share_path, hash])


def get_sharing_url(page):
    """Get a sharing URL for a page, if available."""

    # Retrieve the version of the page persisted to the database to
    # make sure we're using its routable path.
    if page.pk is not None:
        page = page.specific_class.objects.get(pk=page.pk)

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

    if getattr(settings, "WAGTAILSHARING_TOKENIZE_URL", False):
        return get_tokenized_sharing_url(sharing_site, page_path)

    return sharing_site.root_url + page_path
