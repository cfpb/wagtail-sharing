from django.utils.text import slugify
from wagtail.tests.testapp.models import SimplePage


def create_draft_page(site, title):
    page = SimplePage(
        title=title,
        slug=slugify(title),
        content='content',
        live=False
    )

    site.root_page.add_child(instance=page)
    return page
