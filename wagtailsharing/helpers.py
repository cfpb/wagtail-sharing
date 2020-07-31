from django.conf import settings

import jwt
from wagtail.core.models import Site

from wagtailsharing.models import SharingSite


def get_tokenized_sharing_url(sharing_site, page_path):
    share_path = getattr(settings, "WAGTAILSHARING_TOKEN_SHARE_PATH", "share")
    payload = {"path": page_path}
    return "/".join(
        [
            sharing_site.root_url,
            share_path,
            jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256").decode(
                "utf-8"
            ),
        ]
    )


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

    if getattr(settings, "WAGTAILSHARING_TOKENIZE_URL", False):
        return get_tokenized_sharing_url(sharing_site, page_path)

    return sharing_site.root_url + page_path
