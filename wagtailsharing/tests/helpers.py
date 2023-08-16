from django.utils.text import slugify

from wagtail.test.routablepage.models import RoutablePageTest

from wagtailsharing.tests.shareable_routable_testapp.models import TestPage


def create_draft_page(site, title):
    page = TestPage(title=title, slug=slugify(title), live=False)
    site.root_page.add_child(instance=page)
    return page


def create_draft_routable_page(site, title):
    page = RoutablePageTest(title=title, live=False)
    site.root_page.add_child(instance=page)
    return page
